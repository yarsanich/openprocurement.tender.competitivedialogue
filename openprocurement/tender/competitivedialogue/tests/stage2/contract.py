# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy
from datetime import timedelta

from openprocurement.api.models import get_now
from openprocurement.tender.competitivedialogue.tests.base import (
    BaseCompetitiveDialogEUStage2ContentWebTest,
    BaseCompetitiveDialogUAStage2ContentWebTest,
    test_bids,
    author,
    test_tender_stage2_data_eu
)
from openprocurement.api.tests.base import create_classmethod
from openprocurement.api.tests.contract_test_utils import (
    create_tender_contract_invalid,
    get_tender_contract,
    get_tender_contracts,
    not_found,
    create_tender_contract_document,
    put_tender_contract_document,
    patch_tender_contract_document
)
from openprocurement.tender.openeu.tests.contract_test_utils import (
    contract_termination,
    create_tender_contract,
    patch_tender_contract_datesigned,
    patch_tender_contract
)

from openprocurement.tender.openua.tests.contract_test_utils import create_tender_contract as create_tender_contract_ua
from openprocurement.tender.openua.tests.contract_test_utils import patch_tender_contract_datesigned as patch_tender_contract_datesigned_ua
from openprocurement.tender.openua.tests.contract_test_utils import patch_tender_contract as patch_tender_contract_ua


test_tender_bids = deepcopy(test_bids[:2])
for test_bid in test_tender_bids:
    test_bid['tenderers'] = [author]


class TenderStage2EUContractResourceTest(BaseCompetitiveDialogEUStage2ContentWebTest):

    initial_status = 'active.qualification'
    initial_bids = test_tender_bids
    initial_auth = ('Basic', ('broker', ''))
    test_create_tender_contract_invalid = create_classmethod(create_tender_contract_invalid)
    test_get_tender_contract = create_classmethod(get_tender_contract)
    test_get_tender_contracts = create_classmethod(get_tender_contracts)
    test_contract_termination = create_classmethod(contract_termination)
    test_create_tender_contract = create_classmethod(create_tender_contract)
    test_patch_tender_contract_datesigned = create_classmethod(patch_tender_contract_datesigned)
    test_patch_tender_contract = create_classmethod(patch_tender_contract)
    def setUp(self):
        super(TenderStage2EUContractResourceTest, self).setUp()
        # Create award
        self.supplier_info = deepcopy(author)
        self.app.authorization = ('Basic', ('token', ''))
        response = self.app.post_json('/tenders/{}/awards'.format(self.tender_id),
                                      {'data': {'suppliers': [self.supplier_info],
                                                'status': 'pending',
                                                'bid_id': self.bids[0]['id'],
                                                'value': {'amount': 500,
                                                          'currency': 'UAH', 'valueAddedTaxIncluded': True},
                                                'items': test_tender_stage2_data_eu['items']}})
        award = response.json['data']
        self.award_id = award['id']
        self.app.authotization = ('Basic', ('broker', ''))
        response = self.app.get('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token))
        print(response.json['data']['tenderPeriod'], response.json['data']['awardPeriod'])
        response = self.app.patch_json('/tenders/{}/awards/{}'.format(self.tender_id, self.award_id),
                                       {'data': {'status': 'active', 'qualified': True, 'eligible': True}})


class TenderStage2EUContractDocumentResourceTest(BaseCompetitiveDialogEUStage2ContentWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_tender_bids
    initial_auth = ('Basic', ('broker', ''))
    status = 'unsuccessful'

    def setUp(self):
        super(TenderStage2EUContractDocumentResourceTest, self).setUp()
        # Create award
        supplier_info = deepcopy(author)
        self.app.authorization = ('Basic', ('token', ''))
        response = self.app.post_json('/tenders/{}/awards'.format(self.tender_id),
                                      {'data': {'suppliers': [supplier_info],
                                                'status': 'pending',
                                                'bid_id': self.bids[0]['id']}})
        award = response.json['data']
        self.award_id = award['id']
        response = self.app.patch_json('/tenders/{}/awards/{}'.format(self.tender_id, self.award_id),
                                       {'data': {'status': 'active', 'qualified': True, 'eligible': True}})
        # Create contract for award
        response = self.app.post_json('/tenders/{}/contracts'.format(self.tender_id),
                                      {'data': {'title': 'contract title',
                                                'description': 'contract description',
                                                'awardID': self.award_id}})
        contract = response.json['data']
        self.contract_id = contract['id']
        self.app.authorization = ('Basic', ('broker', ''))

    test_not_found = create_classmethod(not_found)
    test_create_tender_contract_document = create_classmethod(create_tender_contract_document)
    test_put_tender_contract_document = create_classmethod(put_tender_contract_document)
    test_patch_tender_contract_document = create_classmethod(patch_tender_contract_document)


class TenderStage2UAContractResourceTest(BaseCompetitiveDialogUAStage2ContentWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_tender_bids

    def setUp(self):
        super(TenderStage2UAContractResourceTest, self).setUp()
        # Create award
        authorization = self.app.authorization
        self.app.authorization = ('Basic', ('token', ''))
        response = self.app.post_json('/tenders/{}/awards'.format(self.tender_id),
                                      {'data': {'suppliers': [author], 'status': 'pending',
                                                'bid_id': self.bids[0]['id'], 'value': self.bids[0]['value']}})
        award = response.json['data']
        self.award_id = award['id']
        self.app.authorization = authorization
        self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
            self.tender_id, self.award_id, self.tender_token),
            {'data': {'status': 'active', 'qualified': True, 'eligible': True}})

    test_create_tender_contract_invalid = create_classmethod(create_tender_contract_invalid)
    test_get_tender_contract = create_classmethod(get_tender_contract)
    test_get_tender_contracts = create_classmethod(get_tender_contracts)
    test_create_tender_contract = create_classmethod(create_tender_contract_ua)
    test_patch_tender_contract_datesigned = create_classmethod(patch_tender_contract_datesigned_ua)
    test_patch_tender_contract = create_classmethod(patch_tender_contract_ua)



class TenderStage2UAContractDocumentResourceTest(BaseCompetitiveDialogUAStage2ContentWebTest):
    initial_status = 'active.qualification'
    initial_bids = test_tender_bids
    status = 'unsuccessful'
    def setUp(self):
        super(TenderStage2UAContractDocumentResourceTest, self).setUp()
        # Create award
        auth = self.app.authorization
        self.app.authorization = ('Basic', ('token', ''))
        response = self.app.post_json('/tenders/{}/awards'.format(self.tender_id),
                                      {'data': {'suppliers': [author],
                                                'status': 'pending',
                                                'bid_id': self.bids[0]['id']}})
        award = response.json['data']
        self.award_id = award['id']
        response = self.app.patch_json('/tenders/{}/awards/{}'.format(self.tender_id, self.award_id),
                                       {'data': {'status': 'active', 'qualified': True, 'eligible': True}})
        # Create contract for award
        response = self.app.post_json('/tenders/{}/contracts'.format(self.tender_id),
                                      {'data': {'title': 'contract title',
                                                'description': 'contract description',
                                                'awardID': self.award_id}})
        contract = response.json['data']
        self.contract_id = contract['id']
        self.app.authorization = auth

    test_not_found = create_classmethod(not_found)
    test_create_tender_contract_document = create_classmethod(create_tender_contract_document)
    test_put_tender_contract_document = create_classmethod(put_tender_contract_document)
    test_patch_tender_contract_document = create_classmethod(patch_tender_contract_document)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderStage2EUContractResourceTest))
    suite.addTest(unittest.makeSuite(TenderStage2EUContractDocumentResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
