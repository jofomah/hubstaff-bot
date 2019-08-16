from abc import ABC, abstractmethod
import csv
import tempfile


class ReportGenerator:

    def collate(self, org, dates):
        '''Flattens dates report data into into rows'''

        return [
            {
                'project_name': project['name'],
                'project_id': project['id'],
                'project_duration': project['duration'],
                'username': user['name'],
                'user_id': user['id'],
                'org_id': org['id'],
                'org_name': org['name'],
                'org_duration': org['duration'],
                'date': date['date']
            }
            for date in dates
            for user in date['users']
            for project in user['projects']
        ]

    def parse_organizations(self, organizations):
        '''Parses organization data returned from report API response'''

        projects = []
        for org in organizations:
            dates = org['dates']
            projects = projects + self.collate(org, dates)

        return projects

    def build_report(self, response_data):
        '''build report from API response data'''

        organizations = response_data.get('organizations')
        user_project_reports = self.parse_organizations(organizations)
        return user_project_reports

    def prepare_for_template(self, user_project_reports):
        '''Transforms build_report() result into format to be rendered by HTMl template'''

        unique_users = []
        by_projects = {}
        for report in user_project_reports:
            if report['username'] not in unique_users:
                unique_users.append(report['username'])

            project_report = by_projects.get(report['project_name'], {})
            project_report.update(
                {report['username']: report['project_duration']})

            by_projects.update({report['project_name']: project_report})

            return unique_users, by_projects


class AbstractWriter(ABC):
    '''Base class for report writers'''

    def __init__(self):
        super().__init__()

    @abstractmethod
    def write_all(self, filename=None):
        pass


class CsvWriter(AbstractWriter):
    '''CSV report writer for writing report to a csv file'''

    def __init__(self, record):
        self.record = record
        super().__init__()

    def get_header(self):
        '''Returns header by scrapping first item  properties'''
        if self.record:
            row = self.record[0]
            titles = [title for title in row.keys()]
            return titles

        return []

    def write_all(self, filename=None):
        '''writes given records to filename or use temp file not given

          Caller of this function should handle the deletion or cleanup of file
        '''
        if not filename:
            file_handler, filename = tempfile.mkstemp()

        header = self.get_header()

        with open(filename, mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()

            for row in self.record:
                writer.writerow(row)

        return filename
