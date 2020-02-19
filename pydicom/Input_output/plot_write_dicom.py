"""
Write DICOM data
이 예제는 pydicom을 사용하여 DICOM 파일을 처음부터 작성하는 방법을 보여줍니다.
이 예제는 작성된 DICOM 표준 호환 파일을 생성하지 않으므로 UID를 유효한 값으로 변경하고
필요한 모든 DICOM 데이터 요소를 추가해야합니다.
"""

import os
import tempfile
import datetime

import pydicom
from pydicom.dataset import Dataset, FileDataset

suffix = '.dcm'
filename_little_endian = tempfile.NamedTemporaryFile(suffix=suffix).name
filename_big_endian = tempfile.NamedTemporaryFile(suffix=suffix).name

print("Setting file meta information")
file_meta = Dataset()
file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
file_meta.MediaStorageSOPInstanceUID = '1.2.3'
file_meta.ImplementationClassUID = '1.2.3.4'

print("Setting dataset values...")
ds = FileDataset(filename_little_endian, {}, file_meta=file_meta, preamble=b'\0' * 128)

ds.PatientName = 'Test^Firstname'
ds.PatientID = '123456'

ds.is_little_endian = True
ds.is_implicit_VR = True

dt = datetime.datetime.now()
ds.ContentDate = dt.strftime('%Y%m%d')
timeStr = dt.strftime('%H%M%S.%f')
ds.ContentTime = timeStr

print('Writing test file', filename_little_endian)
ds.save_as(filename_little_endian)
print('file saved')

ds.file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRBigEndian
ds.is_little_endian = False
ds.is_implicit_VR = False

print("Writing test file as Big Endian Explicit VR", filename_big_endian)
ds.save_as(filename_big_endian)

for filename in (filename_little_endian, filename_big_endian):
    print('Load file {} ...'.format(filename))
    ds = pydicom.dcmread(filename)
    print(ds)

    print('Remove file {} ...'.format(filename))
    os.remove(filename)
