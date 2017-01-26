# -*- coding: utf-8 -*-
import unittest
from six import BytesIO
from urllib import quote
from email.header import Header
from openprocurement.api.tests.base import create_classmethod
from openprocurement.tender.competitivedialogue.tests.base import (BaseCompetitiveDialogEUStage2ContentWebTest,
                                                                   BaseCompetitiveDialogUAStage2ContentWebTest)
from openprocurement.api.tests.document_test_utils import (not_found,
                                                           put_tender_document,
                                                           patch_tender_document,
                                                           create_tender_document,
                                                           create_tender_document_json_invalid,
                                                           create_tender_document_json,
                                                           put_tender_document_json)

##########
#  EU
#########


class TenderStage2EUDocumentResourceTest(BaseCompetitiveDialogEUStage2ContentWebTest):
    status = "active.auction"
    docservice = False
    initial_auth = ('Basic', ('broker', ''))

    test_not_found = create_classmethod(not_found)
    test_put_tender_document = create_classmethod(put_tender_document)
    test_patch_tender_document = create_classmethod(patch_tender_document)
    test_create_tender_document = create_classmethod(create_tender_document)


class TenderStage2DocumentWithDSResourceTest(TenderStage2EUDocumentResourceTest):
    docservice = True


##########
#  UA
##########


class TenderStage2UADocumentResourceTest(BaseCompetitiveDialogUAStage2ContentWebTest):
    status = "active.auction"
    docservice = False

    test_not_found = create_classmethod(not_found)
    test_put_tender_document = create_classmethod(put_tender_document)
    test_patch_tender_document = create_classmethod(patch_tender_document)
    test_create_tender_document = create_classmethod(create_tender_document)


class TenderStage2UADocumentWithDSResourceTest(TenderStage2UADocumentResourceTest):
    docservice = True


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderStage2EUDocumentResourceTest))
    suite.addTest(unittest.makeSuite(TenderStage2DocumentWithDSResourceTest))
    suite.addTest(unittest.makeSuite(TenderStage2UADocumentResourceTest))
    suite.addTest(unittest.makeSuite(TenderStage2UADocumentWithDSResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
