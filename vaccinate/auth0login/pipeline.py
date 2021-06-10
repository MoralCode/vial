from core.models import Reporter
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import Group

AUTH0_ROLES_STAFF = {
    "Reports QA",
    "VIAL admin",
    "VIAL data corrections",
    "VIAL service account",
    "VIAL WB limited",
    "VIAL super-user",
    "Vaccinate CA Staff",
}

AUTH0_STAFF_ROLES_TO_LOCAL_GROUP = {}
if settings.STAGING:
    AUTH0_STAFF_ROLES_TO_LOCAL_GROUP = {
        name + " STAGING": name for name in AUTH0_ROLES_STAFF
    }
else:
    AUTH0_STAFF_ROLES_TO_LOCAL_GROUP = {name: name for name in AUTH0_ROLES_STAFF}


def get_roles_by_env(role):
    if settings.STAGING:
        return "STAGING" in role
    else:
        return "STAGING" not in role


def provide_admin_access_based_on_auth0_role(backend, user, response, *args, **kwargs):
    if backend.name == "auth0":
        users_roles = kwargs.get("details", {}).get("roles", {}) or []
        local_roles = list(filter(get_roles_by_env, users_roles))
        groups = {
            name: Group.objects.get_or_create(name=name)[0] for name in local_roles
        }
        should_be_staff = any(
            auth0_role in users_roles
            for auth0_role in AUTH0_STAFF_ROLES_TO_LOCAL_GROUP.keys()
        )

        if should_be_staff != user.is_staff:
            user.is_staff = should_be_staff
            user.save()

        # Update user's group membership
        # TODO: Update groups using a webhook - see Issue #663
        user_groups = user.groups.all()
        user.groups.clear()

        for group in user_groups:
            if group in local_roles:
                group.user_set.add(user)
            else:
                group.user_set.remove(user)

        # Note: Not all users are reporters
        reporter = Reporter.objects.filter(user=user)[0]

        # Update auth0 roles on Reporter
        if reporter:
            reporter.auth0_role_names = " ".join(users_roles)
            reporter.save()

        # Stash the id_token as 'jwt' in the session
        kwargs["request"].session["jwt"] = response["id_token"]


def social_user_or_logout(backend, uid, user=None, *args, **kwargs):
    provider = backend.name
    social = backend.strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            logout(backend.strategy.request)
        elif not user:
            user = social.user
    return {
        "social": social,
        "user": user,
        "is_new": user is None,
        "new_association": False,
    }
