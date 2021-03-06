# -*- coding: utf-8 -*-
from openprocurement.tender.openeu.utils import qualifications_resource
from openprocurement.tender.openeu.views.qualification_complaint_document import TenderEUQualificationComplaintDocumentResource
from openprocurement.tender.competitivedialogue.models import STAGE_2_EU_TYPE


@qualifications_resource(
    name='Competitive Dialogue Stage 2 EU Qualification Complaint Documents',
    collection_path='/tenders/{tender_id}/qualifications/{qualification_id}/complaints/{complaint_id}/documents',
    path='/tenders/{tender_id}/qualifications/{qualification_id}/complaints/{complaint_id}/documents/{document_id}',
    procurementMethodType=STAGE_2_EU_TYPE,
    description="Competitive Dialogue Stage 2 EU qualification complaint documents")
class CompetitiveDialogueStage2EUQualificationComplaintDocumentResource(TenderEUQualificationComplaintDocumentResource):
    pass

