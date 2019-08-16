from datetime import datetime, timedelta
import json
import os

import flask
import flask_login

from hubstaff import app
from hubstaff.services.client import HubStaff
from hubstaff.services.report import ReportGenerator, CsvWriter
from hubstaff.utils import helpers


INVALID_DATE_MESSAGE = 'Invalid date string, provide date like (YYYY-mm-dd) e.g "2019-08-12"'
HUBSTAFF_CLIENT_ERROR_MESSAGE = 'An error occurred while fetching report data from HubStaff.'


def fetch_report(date):
    hs_client = HubStaff.create()

    hubstaff_org_id = flask.current_app.config['HUBSTAFF_ORGANIZATION_ID']
    return hs_client.get_report_by_date(
        date,
        date,
        params={'organizations': hubstaff_org_id}
    ).json()


def prepare_error_response(error_msg, error_status_code):
    response = flask.make_response(json.dumps(error_msg), error_status_code)
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/')
@app.route('/<string:date>')
@flask_login.login_required
def index(date=None):
    '''Generates and renders time report in HTML viewl

    Parameters
    ----------
    date : str (optional)
        The date for which report will be generated, formated as "YYYY-mm-dd"

    Returns
    -------
    Response
        Flask response object
    '''

    today = datetime.now()
    if date is None:
        a_day = 1
        # datetime.strftime(datetime.now() - timedelta(a_day), '%Y-%m-%d')
        date = helpers.format_date(today - timedelta(a_day))

    today_str = helpers.format_date(today)
    by_projects = {}
    users = []

    if not helpers.is_valid_date_string(date):
        error = INVALID_DATE_MESSAGE
        app.logger.error(error)
        return flask.render_template(
            'index.html', by_projects=by_projects, users=users, error=error, date=date, today=today_str)

    try:
        report_data = fetch_report(date)

    except BaseException as e:
        app.logger.error(e)
        error = HUBSTAFF_CLIENT_ERROR_MESSAGE
        return flask.render_template(
            'index.html', by_projects=by_projects, users=users, error=error, date=date, today=today_str)

    rg = ReportGenerator()
    report = rg.prepare_for_template(rg.build_report(report_data))

    # if report is not empty unpack report
    if report:
        users, by_projects = report

    return flask.render_template(
        'index.html', by_projects=by_projects, users=users, date=date, today=today_str)


@app.route('/export-report/<string:report_date>')
@flask_login.login_required
def export_report(report_date):
    '''Handles requests to export report for a given date as CSV file

    Parameters
    ----------
    report_date : str
        The date for which report will be generated and exported, formated as "YYYY-mm-dd"

    Returns
    -------
    Response
        Flask response object
    '''

    if not report_date or not helpers.is_valid_date_string(report_date):
        bad_request_code = 400
        app.logger.error(INVALID_DATE_MESSAGE)
        error_response = prepare_error_response(INVALID_DATE_MESSAGE, bad_request_code)
        return flask.abort(error_response)

    try:
        report_data = fetch_report(report_date)

    except BaseException as e:
        app.logger.error(e)
        server_error_code = 500
        error_response = prepare_error_response(HUBSTAFF_CLIENT_ERROR_MESSAGE, server_error_code)
        return flask.abort(error_response)

    rg = ReportGenerator()
    report = rg.build_report(report_data)

    export_filename = f'daily_time_report_for_{report_date}.csv'

    writer = CsvWriter(report)
    temp_file = writer.write_all()

    mimetype = 'Content-Type: text/csv; charset=utf-8'
    response = flask.send_file(temp_file, as_attachment=True,
                               mimetype=mimetype, attachment_filename=export_filename,
                               cache_timeout=1)

    # explicitly clean up temp file
    if os.path.exists(temp_file):
        os.remove(temp_file)

    return response
