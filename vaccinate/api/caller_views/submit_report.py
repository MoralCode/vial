import os
import random
from datetime import date, datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

import beeline
import orjson
import pytz
import requests
from api.models import ApiLog
from api.utils import deny_if_api_is_disabled, jwt_auth, log_api_requests
from core.import_utils import derive_appointment_tag, resolve_availability_tags
from core.models import AppointmentTag, CallRequest, Location, Report, Reporter
from dateutil import parser
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pydantic import BaseModel, Field, ValidationError, validator

ALLOWED_VACCINE_VALUES = "Moderna", "Pfizer", "Johnson & Johnson", "Other"


class ReportValidator(BaseModel):
    location: str = Field(alias="Location")
    appointment_details: Optional[str] = Field(
        alias="Appointment scheduling instructions"
    )
    appointments_by_phone: Optional[bool] = Field(alias="Appointments by phone?")
    availability: List[str] = Field(alias="Availability")
    public_notes: Optional[str] = Field(alias="Notes")
    internal_notes: Optional[str] = Field(alias="Internal Notes")
    do_not_call_until: Optional[datetime] = Field(alias="Do not call until")
    web_banked: Optional[bool]
    is_pending_review: Optional[bool] = Field(alias="is_pending_review")
    pending_review_because: Optional[str]
    restriction_notes: Optional[str]
    vaccines_offered: Optional[List[str]]
    web: Optional[str]
    website: Optional[str]
    address: Optional[str]
    full_address: Optional[str]
    hours: Optional[str]
    planned_closure: Optional[date]

    @validator("vaccines_offered")
    def validate_vaccines(cls, vaccines):
        for item in vaccines:
            assert item in ALLOWED_VACCINE_VALUES, "{} is not one of {}".format(
                item, ALLOWED_VACCINE_VALUES
            )
        return vaccines

    @validator("location")
    def location_must_exist(cls, v):
        try:
            return Location.objects.get(public_id=v)
        except Location.DoesNotExist:
            raise ValueError("Location '{}' does not exist".format(v))


@csrf_exempt
@beeline.traced(name="submit_report")
@log_api_requests
@deny_if_api_is_disabled
@jwt_auth(required_permissions=["caller"])
def submit_report(
    request: HttpRequest, on_request_logged: Callable[[Callable[[ApiLog], None]], None]
):
    try:
        post_data = orjson.loads(request.body)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)
    try:
        report_data = ReportValidator(**post_data).dict()
    except ValidationError as e:
        return JsonResponse({"error": e.errors()}, status=400)
    # Now we add the report
    appointment_tag_string, appointment_details = derive_appointment_tag(
        report_data["appointments_by_phone"], report_data["appointment_details"]
    )
    availability_tags = resolve_availability_tags(report_data["availability"])
    kwargs = dict(
        location=report_data["location"],
        report_source="wb" if report_data.get("web_banked") else "ca",
        appointment_tag=AppointmentTag.objects.get(slug=appointment_tag_string),
        appointment_details=appointment_details,
        public_notes=report_data["public_notes"],
        internal_notes=report_data["internal_notes"],
        reported_by=request.reporter,  # type: ignore[attr-defined]
        website=report_data["website"] or report_data["web"],
        vaccines_offered=report_data["vaccines_offered"],
        restriction_notes=report_data["restriction_notes"],
        full_address=report_data["full_address"] or report_data["address"],
        hours=report_data["hours"],
        planned_closure=report_data["planned_closure"],
    )

    # Baseline these as not pending review, since the
    # originally_pending_review field is nullable, so we know which
    # reports were before we started logging.
    kwargs["originally_pending_review"] = False
    if report_data["is_pending_review"]:
        kwargs["originally_pending_review"] = True
        kwargs["pending_review_because"] = report_data.get(
            "pending_review_because", "Unknown"
        )
    else:
        should_review, why = user_should_have_reports_reviewed(
            request.reporter, report_data  # type: ignore[attr-defined]
        )
        if should_review:
            kwargs["originally_pending_review"] = True
            kwargs["pending_review_because"] = why

    kwargs["is_pending_review"] = kwargs["originally_pending_review"]

    if bool(request.GET.get("test")) and request.GET.get("fake_timestamp"):
        fake_timestamp = parser.parse(request.GET["fake_timestamp"])
        if fake_timestamp.tzinfo is None:
            # Assume this is UTC
            fake_timestamp = pytz.UTC.localize(fake_timestamp)
        kwargs["created_at"] = fake_timestamp

    beeline.add_context({"availability_tag_count": len(availability_tags)})
    report = Report.objects.create(**kwargs)
    report.availability_tags.add(*availability_tags)

    # Refresh Report from DB to get .public_id
    report.refresh_from_db()

    report.location.derive_availability_and_inventory(save=True)

    tags_to_requeue = set(
        [
            "skip_call_back_later",  # XXX: Change this to allow other tags to re-enqueue
        ]
    )
    tag_slugs = set([tag.slug for tag in availability_tags])
    if report_data["do_not_call_until"] and not tags_to_requeue & tag_slugs:
        report_data["do_not_call_until"] = None

    CallRequest.mark_completed_by(
        report, enqueue_again_at=report_data["do_not_call_until"]
    )

    def log_created_report(log):
        log.created_report = report
        log.save()

        # Send it to Zapier too
        if os.environ.get("ZAPIER_REPORT_URL"):
            with beeline.tracer(name="zapier"):
                requests.post(
                    os.environ["ZAPIER_REPORT_URL"],
                    json={
                        "report_url": request.build_absolute_uri(
                            "/admin/core/report/{}/change/".format(report.pk)
                        ),
                        "report_public_notes": report.public_notes,
                        "report_internal_notes": report.internal_notes,
                        "location_name": report.location.name,
                        "location_full_address": report.location.full_address,
                        "location_state": report.location.state.abbreviation,
                        "reporter_name": report.reported_by.name,
                        "reporter_id": report.reported_by.external_id,
                        "reporter_role": report.reported_by.auth0_role_names,
                        "availability_tags": list(
                            report.availability_tags.values_list("name", flat=True)
                        ),
                    },
                    timeout=5,
                )

    on_request_logged(log_created_report)

    return JsonResponse(
        {
            "admin_url": "/admin/core/report/{}/change/".format(report.pk),
            "created": [report.public_id],
            "appointment_tag_string": appointment_tag_string,
            "appointment_details": appointment_details,
            "availability_tags": [str(a) for a in availability_tags],
            "report": str(report),
        }
    )


def user_should_have_reports_reviewed(
    user: Reporter, report: Dict[str, Any]
) -> Tuple[bool, str]:
    data_corrections = "VIAL data corrections" + (
        " STAGING" if settings.STAGING else ""
    )
    roles = [r.strip() for r in user.auth0_role_names.split(",") if r.strip()]
    if "Trainee" in roles:
        return True, "Trainee; selected 100% for review"
    elif "Journeyman" in roles:
        if random.random() < 0.15:
            return True, "Journeyman; selected 15% for review"
    elif report.get("web_banked") and data_corrections in roles:
        # Data corrections never get flagged
        return False, ""
    elif random.random() < 0.02:
        return True, "Randomly selected 2% for review"
    return False, ""
