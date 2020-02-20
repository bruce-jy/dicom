from pydicom.dataset import Dataset

from pynetdicom import AE
from pynetdicom.sop_class import ModalityWorklistInformationFind

ae = AE()

ae.add_requested_context(ModalityWorklistInformationFind)

ds = Dataset()
ds.PatientName = '*'
ds.ScheduledProcedureStepSequence = [Dataset()]
item = ds.ScheduledProcedureStepSequence[0]
item.ScheduledStationAETitle = 'CTSCANNER'
item.ScheduledProcedureStepStartDate = '20181005'
item.Modality = 'CT'

# Assciate를 IP 127.0.0.1 and port 11112 인 AE 에 한다.
assoc = ae.associate('127.0.0.1', 11112)

if assoc.is_established:
    # Use the C-FIND service to send the identifier
    responses = assoc.send_c_find(
        ds,
        ModalityWorklistInformationFind
    )

    for (status, identifier) in responses:
        if status:
            print('C-FIND query status: 0x{0:04x}'.format(status.Status))

            # If the status is 'Pending' then identifier is the C-FIND response
            if status.Status in (0xFF00, 0xFF01):
                print(identifier)
        else:
            print('Connection timed out, was aborted or received invalid response')

    # connection을 놓아준다.
    assoc.release()
else:
    print('Association rejected, aborted or never connected')