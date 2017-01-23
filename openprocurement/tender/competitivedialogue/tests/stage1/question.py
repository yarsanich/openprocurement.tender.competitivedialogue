# -*- coding: utf-8 -*-
import unittest

from datetime import datetime, timedelta
from openprocurement.api.models import get_now
from openprocurement.api.tests.base import test_organization
from openprocurement.api.tests.question import (BaseTenderLotQuestionResourceTest,
                                                BaseTenderQuestionResourceTest)

from openprocurement.tender.competitivedialogue.tests.base import (test_tender_data_ua,
                                                                   test_tender_data_eu,
                                                                   test_bids,
                                                                   BaseCompetitiveDialogUAContentWebTest,
                                                                   BaseCompetitiveDialogEUContentWebTest, test_lots)


class BaseCompetitiveDialogUAQuestionResourceTest(object):

    def test_create_tender_question(self):
        """
            Create question
        """
        # Create path for good request
        request_path = '/tenders/{}/questions'.format(self.tender_id)

        # Create question and check response fields, they must match
        response = self.app.post_json(request_path,
                                      {'data': {'title': 'question title',
                                                'description': 'question description',
                                                'author': test_organization}
                                       })
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        question = response.json['data']
        self.assertEqual(question['author']['name'], test_organization['name'])
        self.assertIn('id', question)
        self.assertIn(question['id'], response.headers['Location'])

        self.go_to_enquiryPeriod_end()
        # Try add question after when endquiryPeriod end
        response = self.app.post_json(request_path,
                                      {'data': {'title':
                                                'question title',
                                                'description': 'question description',
                                                'author': test_organization}
                                       }, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['description'], 'Can add question only in enquiryPeriod')

    def test_patch_tender_question(self):
        """
            Test path question
        """

        # Create question
        response = self.app.post_json('/tenders/{}/questions'.format(self.tender_id),
                                      {'data': {'title': 'question title',
                                                'description': 'question description',
                                                'author': test_organization}
                                       })
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        question = response.json['data']

        # Answer on question
        response = self.app.patch_json('/tenders/{}/questions/{}?acc_token={}'.format(
            self.tender_id, question['id'], self.tender_token), {'data': {'answer': 'answer'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['answer'], 'answer')

        # Try answer on question that doesn't exists
        response = self.app.patch_json('/tenders/{}/questions/some_id'.format(self.tender_id),
                                       {'data': {'answer': 'answer'}},
                                       status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'question_id'}
        ])

        # Try answer on question that doesn't exists, and tender too
        response = self.app.patch_json('/tenders/some_id/questions/some_id', {'data': {'answer': 'answer'}}, status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

        # Get answer by tender_id, and question_id
        response = self.app.get('/tenders/{}/questions/{}'.format(self.tender_id, question['id']))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['answer'], 'answer')


class CompetitiveDialogUAQuestionResourceTest(BaseCompetitiveDialogUAContentWebTest,
                                              BaseCompetitiveDialogUAQuestionResourceTest):
    test_tender_data = test_tender_data_ua


class CompetitiveDialogUAQLotQuestionResourceTest(BaseCompetitiveDialogUAContentWebTest,
                                                  BaseTenderLotQuestionResourceTest,
                                                  BaseTenderQuestionResourceTest):
    initial_lots = 2 * test_lots


class BaseCompetitiveDialogUEQuestionResourceTest(object):

    initial_auth = ('Basic', ('broker', ''))

    def test_create_tender_question(self):
        """
          Create question with many posible ways
        """

        # Create question, and check fields match
        response = self.app.post_json('/tenders/{}/questions'.format(self.tender_id),
                                      {'data': {'title': 'question title',
                                                'description': 'question description',
                                                'author': test_bids[0]['tenderers'][0]}
                                       })
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        question = response.json['data']
        self.assertEqual(question['author']['name'], test_bids[0]['tenderers'][0]['name'])
        self.assertIn('id', question)
        self.assertIn(question['id'], response.headers['Location'])

        # Shift time to end of enquiry period
        self.time_shift('enquiryPeriod_ends')

        # Try create question, when enquiry period end
        response = self.app.post_json('/tenders/{}/questions'.format(self.tender_id),
                                      {'data': {'title': 'question title',
                                                'description': 'question description',
                                                'author': test_bids[0]['tenderers'][0]}},
                                      status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['description'], 'Can add question only in enquiryPeriod')

        self.time_shift('active.pre-qualification')  # Shift time to status active.pre-qualification
        self.check_chronograph()

        # Try create question when tender in status active.pre-qualification
        response = self.app.post_json('/tenders/{}/questions'.format(self.tender_id),
                                      {'data': {'title': 'question title',
                                                'description': 'question description',
                                                'author': test_bids[0]['tenderers'][0]}},
                                      status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['description'], 'Can add question only in enquiryPeriod')

    def test_patch_tender_question(self):
        """
          Test the patching questions
        """

        # Create question
        response = self.app.post_json('/tenders/{}/questions'.format(self.tender_id),
                                      {'data': {'title': 'question title',
                                                'description': 'question description',
                                                'author': test_bids[0]['tenderers'][0]}
                                       })
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        question = response.json['data']  # Save question in local namespace

        # Add answer on question which we make
        response = self.app.patch_json('/tenders/{}/questions/{}?acc_token={}'.format(self.tender_id,
                                                                                      question['id'],
                                                                                      self.tender_token),
                                       {'data': {'answer': 'answer'}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['answer'], 'answer')

        # Try add answer, by bad token_id
        response = self.app.patch_json('/tenders/{}/questions/some_id'.format(self.tender_id),
                                       {'data': {'answer': 'answer'}}, status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'question_id'}
        ])

        # Try add answer, by bad token_id, and bad question_id
        response = self.app.patch_json('/tenders/some_id/questions/some_id', {'data': {'answer': 'answer'}}, status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

        # Add answer by good token_id, and question_id
        response = self.app.get('/tenders/{}/questions/{}'.format(self.tender_id, question['id']))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['answer'], 'answer')

        # Shift time to tender status active.pre-qualification
        self.time_shift('active.pre-qualification')
        self.check_chronograph()  # check chronograph

        # Try add question when tender status unsuccessful
        response = self.app.patch_json('/tenders/{}/questions/{}?acc_token={}'.format(self.tender_id,
                                                                                      question['id'],
                                                                                      self.tender_token),
                                       {'data': {'answer': 'answer'}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]['description'], "Can't update question in current (unsuccessful) tender status")

class CompetitiveDialogUEQuestionResourceTest(BaseCompetitiveDialogEUContentWebTest,
                                              BaseCompetitiveDialogUEQuestionResourceTest,
                                              BaseTenderQuestionResourceTest):
    test_tender_data = test_tender_data_eu

class CompetitiveDialogUELotQuestionResourceTest(BaseCompetitiveDialogEUContentWebTest,
                                                 BaseTenderLotQuestionResourceTest):
    initial_lots = 2 * test_lots
    initial_auth = ('Basic', ('broker', ''))


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CompetitiveDialogUAQuestionResourceTest))
    suite.addTest(unittest.makeSuite(CompetitiveDialogUEQuestionResourceTest))
    suite.addTest(unittest.makeSuite(CompetitiveDialogUAQLotQuestionResourceTest))
    suite.addTest(unittest.makeSuite(CompetitiveDialogUELotQuestionResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
