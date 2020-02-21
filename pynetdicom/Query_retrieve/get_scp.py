import os
from os.path import dirname

from pydicom import dcmread
from pydicom.data import get_testdata_file

from pynetdicom import AE, StoragePresentationContexts, evt
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelGet

def handle_get(event):
    """Handle a C-GET request event."""
    ds = event.identifier
    if 'QueryRetrieveLevel' not in ds:
        # Failure
        yield 0xC000, None
        return
    print(ds)
    instances = []
    matching = []
    fname = get_testdata_file('CT_small.dcm')
    fdir = dirname(fname)
    for fpath in os.listdir(fdir):
        if fpath.endswith('.dcm'):
            instances.append(dcmread(os.path.join(fdir, fpath), force=True))

    print('PatientID 없는 instances 제거 전: ', len(instances))
    instances = [inst for inst in instances if inst.get('PatientID', '') != '']
    print('PatientID 없는 instances 제거 후: ', len(instances))

    if ds.QueryRetrieveLevel == 'SERIES':
        if 'PatientID' in ds:
            matching = [
                inst for inst in instances if inst.PatientID == ds.PatientID
            ]

        # Skip the other possible attributes...

    # Skip the other QR levels...
    len(matching)
    yield len(instances)

    for instance in matching:
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        # Pending
        yield (0xFF00, instance)

handlers = [(evt.EVT_C_GET, handle_get)]

ae = AE()
ae.supported_contexts = StoragePresentationContexts

for cx in ae.supported_contexts:
    cx.scp_role = True
    cx.scu_role = False

ae.add_supported_context(PatientRootQueryRetrieveInformationModelGet)

ae.start_server(('', 11112), evt_handlers=handlers)
