# -*- coding: utf-8 -*-
import unittest
from email.header import Header
from openprocurement.api.tests.base import create_classmethod
from openprocurement.tender.competitivedialogue.tests.base import (BaseCompetitiveDialogUAContentWebTest,
                                                                   BaseCompetitiveDialogEUContentWebTest)
from openprocurement.api.tests.document_test_utils import (not_found,
                                                           put_tender_document,
                                                           patch_tender_document,
                                                           create_tender_document,
                                                           create_tender_document_json_invalid,
                                                           create_tender_document_json,
                                                           put_tender_document_json)

class DialogEUDocumentResourceTest(BaseCompetitiveDialogEUContentWebTest):
    docservice = False
    status = "active.auction"
    initial_auth = ('Basic', ('broker', ''))
    test_not_found = create_classmethod(not_found)
    test_put_tender_document = create_classmethod(put_tender_document)
    test_patch_tender_document = create_classmethod(patch_tender_document)
    test_create_tender_document = create_classmethod(create_tender_document)


class DialogEUDocumentWithDSResourceTest(DialogEUDocumentResourceTest):
    docservice = True


class DialogUADocumentResourceTest(BaseCompetitiveDialogUAContentWebTest):
    docservice = False
    status = "active.auction"
    initial_auth = ('Basic', ('broker', ''))
    test_not_found = create_classmethod(not_found)
    test_put_tender_document = create_classmethod(put_tender_document)
    test_patch_tender_document = create_classmethod(patch_tender_document)
    test_create_tender_document = create_classmethod(create_tender_document)


class DialogUADocumentWithDSResourceTest(DialogUADocumentResourceTest):
    docservice = True


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DialogEUDocumentResourceTest))
    suite.addTest(unittest.makeSuite(DialogEUDocumentWithDSResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
