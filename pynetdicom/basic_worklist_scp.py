import os
from os.path import dirname

from pydicom import dcmread
from pydicom.data import get_testdata_file
from pydicom.dataset import Dataset

from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityWorklistInformationFind

filepath = get_testdata_file('badVR.dcm')
print('Path to the DICOM directory: ', filepath)

base_dir = dirname(filepath)
print('Path to the base_dir: ', base_dir)

# Implement the handler for evt.EVT_C_FIND
def handle_find(event):
    """Handle a C-FIND request event."""
    ds = event.identifier

    instances = []
    fdir = base_dir
    for fpath in os.listdir(fdir):
        print(fpath, ' --> ', fpath.endswith('.dcm'))
        if fpath.endswith('.dcm'):
            instances.append(dcmread(os.path.join(fdir, fpath), force=True))
    print(instances[0])
    if 'QueryRetrieveLevel' not in ds:
        yield 0xC000, None
        return

    if ds.QueryRetrieveLevel == 'PATIENT':
        if 'PatientName' in ds:
            if ds.PatientName not in ['*', '', '?']:
                matching = [
                    inst for inst in instances if inst.PatientName == ds.PatientName
                ]

    for instance in matching:
        if event.is_cancelled:
            yield (0xFE00, None)
            return

        identifier = Dataset()
        identifier.PatientName = instance.PatientName
        identifier.QueryRetrieveLevel = ds.QueryRetrieveLevel

        yield (0xFF00, identifier)

handlers = [(evt.EVT_C_FIND, handle_find)]

# Initialise the Application Entity and specify the listen port
ae = AE()

# Add the supported presentation context
ae.add_supported_context(ModalityWorklistInformationFind)

# Start listening for incoming association requests
ae.start_server(('', 11112), evt_handlers=handlers)
print(ae.ae_title)
print(ae.active_associations)
print('ae start server on {}:{}')
