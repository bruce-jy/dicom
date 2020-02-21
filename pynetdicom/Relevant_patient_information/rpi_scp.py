import os
from os.path import dirname

from pydicom import dcmread
from pydicom.data import get_testdata_file
from pydicom.dataset import Dataset

from pynetdicom import AE, evt
from pynetdicom.sop_class import GeneralRelevantPatientInformationQuery

def create_template(match, dset):
    dset.update(match)
    # for elem in enumerate(match.elements):
    #     dset.add(elem)
    return dset

def handle_find(event):
    """Handle a C-FIND service request"""
    ds = event.identifier

    instances = []
    fname = get_testdata_file('CT_small.dcm')
    fdir = dirname(fname)
    for fpath in os.listdir(fdir):
        if fpath.endswith('.dcm'):
            instances.append(dcmread(os.path.join(fdir, fpath), force=True))

    print('PatientID 없는 instances 제거 전: ', len(instances))
    instances = [inst for inst in instances if inst.get('PatientID', '') != '']
    print('PatientID 없는 instances 제거 후: ', len(instances))

    matching = [
        inst for inst in instances if inst.PatientID == ds.PatientID
    ]

    if len(matching) == 1:
        identifier = create_template(matching[0], ds)
        yield (0xFF00, identifier)
    elif len(matching) > 1:
        yield (0xC100, None)

handlers = [(evt.EVT_C_FIND, handle_find)]

ae = AE()
ae.add_supported_context(GeneralRelevantPatientInformationQuery)
ae.start_server(('', 11112), evt_handlers=handlers)
