from datetime import datetime, timedelta

from hubstaff import app
from hubstaff.utils import helpers
from hubstaff.tests import helper as test_helper


def test_index_route_defaults_to_previous_day():
    '''Test that index route defaults to previous date'''

    client = app.test_client()

    test_helper.login(client)

    response = client.get('/')

    a_day = 1
    date = helpers.format_date(datetime.now() - timedelta(a_day))

    search_string = f'<span><strong>Current Report Date:</strong> {date}</span>'

    assert response.status_code == 200
    assert response.data.decode('utf-8').find(search_string) != -1

    # verify that it does not produce error message
    assert b'Invalid date string, provide date like' not in response.data


def test_index_with_invalid_date():
    '''Test index route with invalid date'''

    client = app.test_client()

    test_helper.login(client)

    response = client.get('/invalid-date')

    expected_error = b'Invalid date string, provide date like (YYYY-mm-dd) e.g &#34;2019-08-12&#34;'

    assert response.status_code == 200
    assert expected_error in response.data


def test_index_with_valid_date():
    '''Test index route with valid date'''

    client = app.test_client()

    test_helper.login(client)

    date = '2019-08-12'
    response = client.get(f'/{date}')

    search_string = f'<span><strong>Current Report Date:</strong> {date}</span>'

    assert response.status_code == 200
    assert response.data.decode('utf-8').find(search_string) != -1

    # verify that it does not produce error message
    assert b'Invalid date string, provide date like' not in response.data


def test_export_report_with_invalid_date():
    '''Test behaviour of export_report route when called with invalid date'''

    client = app.test_client()

    test_helper.login(client)

    response = client.get('/export-report/invalid-date')

    assert response.status_code == 400


def test_export_report_with_valid_date():
    '''Test export report route when given valid date'''

    client = app.test_client()

    test_helper.login(client)

    response = client.get('/export-report/2019-08-12')

    assert response.status_code == 200

    empty_file_response = b'\r\n'
    non_empty_file_headers = b'project_name,project_id,project_duration,username,\
        user_id,org_id,org_name,org_duration,date'

    # check for empty and non empty because i do not know which date might have data
    assert empty_file_response in response.data or non_empty_file_headers in response.datas
