import re
import json
from datetime import datetime as dt

import requests
from bs4 import BeautifulSoup

from company import JobDescription, Document
from company import STYLE_H2, STYLE_H1


class MicrosoftJobDescription(JobDescription):

    def __init__(self, url):
        response = requests.get(url)
        string = re.search('{"siteConfig"(.+?)}};', response.text).group(0)
        self.content = json.loads(string[:-1])

    @property
    def title(self):
        return self.content['jobDetail']['data']['job']['title']

    @property
    def location(self):
        return self.content['jobDetail']['data']['job']['location']

    @property
    def id(self):
        return self.content['jobDetail']['data']['job']['jobId']

    @property
    def date(self):
        posted_date = self.content['jobDetail']['data']['job']['postedDate']
        return dt.fromisoformat(posted_date)
    @property
    def travel(self):
        return self.content['jobDetail']['data']['job']['requisitionTravelPercentage']

    @property
    def profession(self):
        return self.content['jobDetail']['data']['job']['category']

    @property
    def role_type(self):
        return self.content['jobDetail']['data']['job']['requisitionRoleType']

    @property
    def employment_type(self):
        return self.content['jobDetail']['data']['job']['employmentType']

    @property
    def summary(self):
        summary = self.content['jobDetail']['data']['job']['jobSummary']
        soup = BeautifulSoup(summary, 'html.parser')
        return '\n'.join([s.strip() for s in soup.strings if s])

    @property
    def responsibilities(self):
        responsibilities = self.content['jobDetail']['data']['job']['jobResponsibilities']
        soup = BeautifulSoup(responsibilities, 'html.parser')
        return '\n'.join([s.strip() for s in soup.strings if s])

    @property
    def qualifications(self):
        qualifications = self.content['jobDetail']['data']['job']['jobQualifications']
        soup = BeautifulSoup(qualifications, 'html.parser')
        return '\n'.join([s.strip() for s in soup.strings if s])

    @property
    def benefits(self):
        benefits = self.content['jobDetail']['data']['job']['benefits_and_perks']
        return [b['displayName'] for b in benefits]

    @property
    def meta(self):
        job = self.content['jobDetail']['data']['job']
        return [
            ('level', job['careerStage']),
            ('requires_university', job['isReqTypeUniversity']),
            ('job_posting_id', job['jobPostingId']),
            ('primary_recruiter', job['primaryRecruiter']),
            ('requisition_admin_contact', job['requisitionAdminContact']),
            ('requisition_hiring_manager', job['requisitionHiringManager']),
            ('internal_category_id', job['internalCategoryId'])
        ]


class MicrosoftDocument(Document):

    def __init__(self, url):
        self.job_description = MicrosoftJobDescription(url)
        super().__init__()

    def get_filename(self):
        return '-'.join([
            'microsoft',
            self.job_description.title.lower().replace(' ', '-'),
            self.job_description.id
        ])

    def build(self):
        # TITLE
        self.add_heading(self.job_description.title, STYLE_H1)

        self.add_body(self.job_description.location)

        # TABLE
        data = [
            ['Job Number', self.job_description.id, 'Date Posted', self.job_description.date],
            ['Travel', self.job_description.travel, 'Profession', self.job_description.role_type],
            ['Role Type', self.job_description.role_type, 'Employment Type', self.job_description.employment_type]
        ]
        self.add_table(data)
        self.add_body(self.job_description.summary)

        self.add_heading('Responsibilities', STYLE_H2)
        self.add_body(self.job_description.responsibilities)

        self.add_heading('Qualifications', STYLE_H2)
        self.add_body(self.job_description.qualifications)

        self.add_heading('Benefits and Perks', STYLE_H2)
        self.add_unordered_list(self.job_description.benefits)

        # META
        self.add_table(self.job_description.meta)

        self.doc.build(self.story)

    def debug(self):
        with open('%s.json' % self.get_filename(), 'w') as outfile:
            json.dump(self.job_description.content, outfile, indent=True, sort_keys=True)

