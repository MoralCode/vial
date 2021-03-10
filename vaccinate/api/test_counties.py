import pytest


@pytest.mark.django_db
def test_counties(client):
    response = client.get("/api/counties/CA")
    assert response.json() == {
        "state_name": "California",
        "state_abbreviation": "CA",
        "state_fips_code": "06",
        "counties": [
            {"county_name": "Glenn", "county_fips_code": 6021},
            {"county_name": "Shasta", "county_fips_code": 6089},
            {"county_name": "Tuolumne", "county_fips_code": 6109},
            {"county_name": "Sonoma", "county_fips_code": 6097},
            {"county_name": "Santa Clara", "county_fips_code": 6085},
            {"county_name": "Madera", "county_fips_code": 6039},
            {"county_name": "Yuba", "county_fips_code": 6115},
            {"county_name": "Humboldt", "county_fips_code": 6023},
            {"county_name": "Monterey", "county_fips_code": 6053},
            {"county_name": "Santa Cruz", "county_fips_code": 6087},
            {"county_name": "Alameda", "county_fips_code": 6001},
            {"county_name": "San Joaquin", "county_fips_code": 6077},
            {"county_name": "Tehama", "county_fips_code": 6103},
            {"county_name": "Mariposa", "county_fips_code": 6043},
            {"county_name": "Yolo", "county_fips_code": 6113},
            {"county_name": "Napa", "county_fips_code": 6055},
            {"county_name": "San Francisco", "county_fips_code": 6075},
            {"county_name": "San Luis Obispo", "county_fips_code": 6079},
            {"county_name": "Butte", "county_fips_code": 6007},
            {"county_name": "San Mateo", "county_fips_code": 6081},
            {"county_name": "Sutter", "county_fips_code": 6101},
            {"county_name": "Mono", "county_fips_code": 6051},
            {"county_name": "Contra Costa", "county_fips_code": 6013},
            {"county_name": "Sierra", "county_fips_code": 6091},
            {"county_name": "Siskiyou", "county_fips_code": 6093},
            {"county_name": "Imperial", "county_fips_code": 6025},
            {"county_name": "Inyo", "county_fips_code": 6027},
            {"county_name": "Kings", "county_fips_code": 6031},
            {"county_name": "Nevada", "county_fips_code": 6057},
            {"county_name": "Los Angeles", "county_fips_code": 6037},
            {"county_name": "Trinity", "county_fips_code": 6105},
            {"county_name": "Orange", "county_fips_code": 6059},
            {"county_name": "Stanislaus", "county_fips_code": 6099},
            {"county_name": "Sacramento", "county_fips_code": 6067},
            {"county_name": "San Benito", "county_fips_code": 6069},
            {"county_name": "Marin", "county_fips_code": 6041},
            {"county_name": "Lake", "county_fips_code": 6033},
            {"county_name": "Ventura", "county_fips_code": 6111},
            {"county_name": "Calaveras", "county_fips_code": 6009},
            {"county_name": "Tulare", "county_fips_code": 6107},
            {"county_name": "Del Norte", "county_fips_code": 6015},
            {"county_name": "Merced", "county_fips_code": 6047},
            {"county_name": "San Bernardino", "county_fips_code": 6071},
            {"county_name": "San Diego", "county_fips_code": 6073},
            {"county_name": "Lassen", "county_fips_code": 6035},
            {"county_name": "Placer", "county_fips_code": 6061},
            {"county_name": "Colusa", "county_fips_code": 6011},
            {"county_name": "Kern", "county_fips_code": 6029},
            {"county_name": "El Dorado", "county_fips_code": 6017},
            {"county_name": "Mendocino", "county_fips_code": 6045},
            {"county_name": "Plumas", "county_fips_code": 6063},
            {"county_name": "Solano", "county_fips_code": 6095},
            {"county_name": "Santa Barbara", "county_fips_code": 6083},
            {"county_name": "Riverside", "county_fips_code": 6065},
            {"county_name": "Modoc", "county_fips_code": 6049},
            {"county_name": "Amador", "county_fips_code": 6005},
            {"county_name": "Alpine", "county_fips_code": 6003},
            {"county_name": "Fresno", "county_fips_code": 6019},
        ],
    }
