"""
Anonymize DICOM data
본 예제는 DICOM 데이터를 익명화 시키는 시작점이다.
"""

from __future__ import print_function

import tempfile

import pydicom
from pydicom.data import get_testdata_files

print(__doc__)

filename = get_testdata_files('MR_small.dcm')[0]
dataset = pydicom.dcmread(filename)

data_elements = ['PatientID', 'PatientBirthDate']

for de in data_elements:
    print(dataset.data_element(de))

"""
데이터 세트 내 사람 이름에 해당하는 모든 태그를 찾기 위해 콜백 함수를 정의합니다.
곡선 태그를 제거하기위한 콜백 함수를 정의 할 수도 있습니다.
"""
def person_names_callback(dataset, data_element):
    if data_element.VR == 'PN':
        data_element.value = 'anonymous'

def curves_callback(dataset, data_element):
    if data_element.tag.group & 0xFF00 == 0x5000:
        del dataset[data_element.tag]

"""
콜백 함수를 사용하여 환자 이름을 찾아낼 수 있지만, 환자 ID 같이 태그를 직접 사용할 수도 있습니다.
"""
dataset.PatientID = 'id'
dataset.walk(person_names_callback)
dataset.walk(curves_callback)

"""
pydicom은 pirvate tag들을 제거할 수 있는 remove_private_tags 함수를 제공합니다.
"""
dataset.remove_private_tags()

"""
type 3 요소는 del이나 delattr 함수로 쉽게 삭제할 수 있습니다.
"""
if 'OtherPatientIDs' in dataset:
    delattr(dataset, 'OtherPatientIDs')

if 'OtherPatientIDsSequence' in dataset:
    del dataset.OtherPatientIDsSequence

"""
type 2 요소는 빈 string 값을 빈 요소에 할당할 수 있습니다.
"""
tag = 'PatientBirthDate'
if tag in dataset:
    dataset.data_element(tag).value = '19000101'

"""
마지막으로 이미지를 저장할 수 있습니다.
"""
data_elements = ['PatientID', 'PatientBirthDate']

for de in data_elements:
    print(dataset.data_element(de))

output_filename = tempfile.NamedTemporaryFile().name
dataset.save_as(output_filename)
