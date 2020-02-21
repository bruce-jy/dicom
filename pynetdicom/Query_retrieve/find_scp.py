import os
from os.path import dirname

from pydicom import dcmread
from pydicom.data import get_testdata_file
from pydicom.dataset import Dataset

from pynetdicom import AE, evt
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

# evt.EVT_C_FIND
def handle_find(event):
    """Handle a C-FIND request event"""
    ds = event.identifier
    print(ds)
    instances = []
    fname = get_testdata_file('CT_small.dcm')
    fdir = dirname(fname)
    # fdir = '../Modality_performed_procedure_step'
    for fpath in os.listdir(fdir):
        if fpath.endswith('.dcm'):
            instances.append(dcmread(os.path.join(fdir, fpath), force=True))
    print('PatientName 없는 instances 제거 전: ', len(instances))
    instances = [inst for inst in instances if inst.get('PatientName', '') != '']
    print('PatientName 없는 instances 제거 후: ', len(instances))
    if 'QueryRetrieveLevel' not in ds:
        yield 0xC000, None
        return

    if ds.QueryRetrieveLevel == 'PATIENT':
        if 'PatientName' in ds:
            if ds.PatientName not in ['*', '', '?']:
                matching = [
                    inst for inst in instances if inst.PatientName == ds.PatientName
                ]
            # Skip the other possible values...
        # Skip the other possible attributes...
    # Skip the other QR levels...

    for instances in matching:
        # Check if C-CANCEL has been received
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        identifier = Dataset()
        identifier.PatientName = instances.PatientName
        identifier.QueryRetrieveLevel = 'PATIENT' #instances.QueryRetrieveLevel

        # Pending
        yield (0xFF00, identifier)

handlers = [(evt.EVT_C_FIND, handle_find)]

# Initialize the Application Entity and specify the listen port
ae = AE()

ae.add_supported_context(PatientRootQueryRetrieveInformationModelFind)

ae.start_server(('', 11112), evt_handlers=handlers)
