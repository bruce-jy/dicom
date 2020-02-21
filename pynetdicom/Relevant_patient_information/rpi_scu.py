from pydicom.dataset import Dataset

from pynetdicom import AE
from pynetdicom.sop_class import GeneralRelevantPatientInformationQuery

ae = AE()

ae.add_requested_context(GeneralRelevantPatientInformationQuery)

ds = Dataset()
ds.PatientName = ''
ds.PatientID = '123456'
ds.ContentTemplateSequence = [Dataset()]
ds.ContentTemplateSequence[0].MappaingResource = 'DCMR'
ds.ContentTemplateSequence[0].TemplateItendifier = '9007'

assoc = ae.associate('127.0.0.1', 11112)

if assoc.is_established:
    responses = assoc.send_c_find(ds, GeneralRelevantPatientInformationQuery)

    for (status, identifier) in responses:
        if status:
            print('C-FIND query status: 0x{0:04x}'.format(status.Status))

            if status.Status in (0xFF00, 0xFF01):
                print(identifier)
        else:
            print('Connection timed out, was aborted or received invalid response')

    assoc.release()
else:
    print('Association rejected, aborted or never connected')
