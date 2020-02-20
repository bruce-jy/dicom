from pydicom.dataset import Dataset

from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityPerformedProcedureStepSOPClass

managed_instances = {}

# evt.EVT_N_CREATE handler를 Implement
def handle_create(event):
    # MPPS의 N-CREATE 요청은 *Affected SOP Instance UID*를 꼭 가지고 있어야 한다.
    req = event.request
    if req.AffectedSOPInstanceUID is None:
        # Failed - 필수 attr이 없음
        return 0x0106, None

    # SOP Instance는 중복생성할 수 없다.
    if req.AffectedSOPInstanceUID in managed_instances:
        # Failed - SOP Instance 중복 생성
        return 0x0111, None

    # N-CREATE 요청의 attribute list를 가져온다.
    attr_list = event.attribute_list

    # Performed Procedure Step Status는 attribute list에 있어야 하고 꼭 'IN PROGRESS' 여야 한다.
    if 'PerformedProcedureStepStatus' not in attr_list:
        # Failed - attribute가 빠짐
        return 0x0120, None
    if attr_list.PerformedProcedureStepStatus.upper() != 'IN PROGRESS':
        return 0x0106, None

    # Skip other tests...

    # Modality Performed Procedure Step SOP Class Instance 생성
    # DICOM 표준, Part 3, Annex B.17
    ds = Dataset()

    # SOP Common module element를 추가한다 (Annex C.12.1)
    ds.SOPClassUID = ModalityPerformedProcedureStepSOPClass
    ds.SOPInstanceUID = req.AffectedSOPInstanceUID

    # requst attribute list로 dataset을 update 한다.
    ds.update(attr_list)

    # managed_instance 리스트에 SOP Instance를 추가한다.
    managed_instances[ds.SOPInstanceUID] = ds

    # 성공 상태값과 dataset을 리턴한다.
    return 0x0000, ds

# evt.EVT_N_SET handler를 Implement
def handle_set(event):
    req = event.request
    if req.RequestedSOPInstanceUID not in managed_instances:
        # Failed - SOP Instance 등록 안되어있음
        return 0x0112, None

    ds = managed_instances[req.RequestedSOPInstanceUID]

    # N-SET 요청의 *Modification List*(수정사항) dataset
    mod_list = event.attribute_list

    # Skip other tests...

    ds.update(mod_list)

    return 0x0000, ds

handlers = [(evt.EVT_N_CREATE, handle_create), (evt.EVT_N_SET, handle_set)]

ae = AE()
ae.add_supported_context(ModalityPerformedProcedureStepSOPClass)

ae.start_server(('', 11112), evt_handlers=handlers)
