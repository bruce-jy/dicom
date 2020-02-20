from pydicom.dataset import Dataset
from pydicom.uid import generate_uid

from pynetdicom import AE
from pynetdicom.sop_class import (
    ModalityPerformedProcedureStepSOPClass,
    CTImageStorage
)
from pynetdicom.status import code_to_category

"""
Modality Performed Procedure Step Management Service CREATE SCU
"""
print('Modality Performed Procedure Step Management Service CREATE SCU', '='*30)
print()
ct_study_uid = generate_uid()
mpps_instance_uid = generate_uid()

# Our N-CREATE *Attribute List* 생성할 속성들
def build_attr_list():
    ds = Dataset()
    # Performed Procedure Step Relationship
    ds.ScheduledStepAttributesSequence = [Dataset()]
    step_seq = ds.ScheduledStepAttributesSequence
    step_seq[0].StudyInstanceUID = ct_study_uid
    step_seq[0].ReferencedStudySequence = []
    step_seq[0].AccessionNumber = '1'
    step_seq[0].RequestedProcedureID = "1"
    step_seq[0].RequestedProcedureDescription = 'Some procedure'
    step_seq[0].ScheduledProcedureStepID = "1"
    step_seq[0].ScheduledProcedureStepDescription = 'Some procedure step'
    step_seq[0].ScheduledProcedureProtocolCodeSequence = []
    ds.PatientName = 'Test^Test'
    ds.PatientID = '123456'
    ds.PatientBirthDate = '20000101'
    ds.PatientSex = 'O'
    ds.ReferencedPatientSequence = []
    # Performed Procedure Step Information
    ds.PerformedProcedureStepID = "1"
    ds.PerformedStationAETitle = 'SOMEAE'
    ds.PerformedStationName = 'Some station'
    ds.PerformedLocation = 'Some location'
    ds.PerformedProcedureStepStartDate = '20000101'
    ds.PerformedProcedureStepStartTime = '1200'
    ds.PerformedProcedureStepStatus = 'IN PROGRESS'
    ds.PerformedProcedureStepDescription = 'Some description'
    ds.PerformedProcedureTypeDescription = 'Some type'
    ds.PerformedProcedureCodeSequence = []
    ds.PerformedProcedureStepEndDate = None
    ds.PerformedProcedureStepEndTime = None
    # Image Acquisition Results
    ds.Modality = 'CT'
    ds.StudyID = "1"
    ds.PerformedProtocolCodeSequence = []
    ds.PerformedSeriesSequence = []

    return ds

# Initialise the Application Entity
ae = AE()

# Add a requested presentation context
ae.add_requested_context(ModalityPerformedProcedureStepSOPClass)

# Associate with peer AE at IP 127.0.0.1 and port 11112
assoc = ae.associate('127.0.0.1', 11112)

if assoc.is_established:
    # Use the N-CREATE service to send a request to create a SOP Instance
    # should return the Instance itself
    status, attr_list = assoc.send_n_create(
        build_attr_list(),
        ModalityPerformedProcedureStepSOPClass,
        mpps_instance_uid
    )

    # Check the status of the display system request
    if status:
        print('N-CREATE request status: 0x{0:04x}'.format(status.Status))

        # If the MPPS request succeeded the status category may
        # be either Success or Warning
        category = code_to_category(status.Status)
        if category in ['Warning', 'Success']:
            # `attr_list` is a pydicom Dataset containing attribute values
            print(attr_list)
    else:
        print('Connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()
else:
    print('Association rejected, aborted or never connected')

"""
Modality Performed Procedure Step Management Service SET SCU
"""
print()
print()
print('Modality Performed Procedure Step Management Service SET SCU', '='*30)
print()
# CT 이미지 인스턴스 uid를 10개 만든다.
# SOP Instances is generated
ct_series_uid = generate_uid()
ct_instance_uids = [generate_uid() for ii in range(10)]

# Our N-SET *Modification List*
def build_mod_list(series_instance, sop_instances):
    ds = Dataset()
    ds.PerformedSeriesSequence = [Dataset()]

    series_seq = ds.PerformedSeriesSequence
    series_seq[0].PerformingPhysicianName = None
    series_seq[0].ProtocolName = "Some protocol"
    series_seq[0].OperatorName = None
    series_seq[0].SeriesInstanceUID = series_instance
    series_seq[0].SeriesDescription = "some description"
    series_seq[0].RetrieveAETitle = None
    series_seq[0].ReferencedImageSequence = []

    img_seq = series_seq[0].ReferencedImageSequence
    for uid in sop_instances:
        img_ds = Dataset()
        img_ds.ReferencedSOPClassUID = CTImageStorage
        img_ds.ReferencedSOPInstanceUID = uid
        img_seq.append(img_ds)

    series_seq[0].ReferencedNonImageCompositeSOPInstanceSequence = []

    return ds

# Our final N-SET *Modification List*
final_ds = Dataset()
final_ds.PerformedProcedureStepStatus = "COMPLETED"
final_ds.PerformedProcedureStepEndDate = "20000101"
final_ds.PerformedProcedureStepEndTime = "1300"

# Associate with peer again
assoc = ae.associate('127.0.0.1', 11112)

if assoc.is_established:
    # Use the N-SET service to update the SOP Instance
    # CT 이미지 인스턴스 10개 추가한거 SET
    status, attr_list = assoc.send_n_set(
        build_mod_list(ct_series_uid, ct_instance_uids),
        ModalityPerformedProcedureStepSOPClass,
        mpps_instance_uid
    )

    if status:
        print('N-SET request status: 0x{0:04x}'.format(status.Status))
        category = code_to_category(status.Status)
        if category in ['Warning', 'Success']:
            # Send completion Complete 됐다고 Set 하는 부분
            status, attr_list = assoc.send_n_set(
                final_ds,
                ModalityPerformedProcedureStepSOPClass,
                mpps_instance_uid
            )
            print(attr_list)
            if status:
                print('Final N-SET request status: 0x{0:04x}'.format(status.Status))
    else:
        print('Connection timed out, was aborted or received invalid response')

    assoc.release()
