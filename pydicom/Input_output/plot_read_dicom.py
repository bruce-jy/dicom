"""
Read DICOM and ploting using matplotlib
본 예제는 matplotlib을 통해 DICOM 파일을 시각화하고, 몇가지 정보를 print하는 예제입니다.
"""
import matplotlib.pyplot as plt
import pydicom
from pydicom.data import get_testdata_files

print(__doc__)

filename = get_testdata_files('CT_small.dcm')[0]
dataset = pydicom.dcmread(filename)

print()
print("Filename...................:", filename)
print("Storage type...............:", dataset.SOPClassUID)
print()

pat_name = dataset.PatientName
display_name = pat_name.family_name + ', ' + pat_name.given_name
print("Patient's name.............:", display_name)
print("Patient id.................:", dataset.PatientID)
print("Modality...................:", dataset.Modality)
print("Study Date.................:", dataset.StudyDate)

if 'PixelData' in dataset:
    rows = int(dataset.Rows)
    cols = int(dataset.Columns)
    print("Image size.................: {rows:d} x {cols:d}, {size:d} bytes".format(
        rows=rows, cols=cols, size=len(dataset.PixelData)))
    if 'PixelSpacing' in dataset:
        print('Pixel spacing..............:', dataset.PixelSpacing)

print("Slice location.............:", dataset.get('SliceLocation', "(missing)"))

plt.imshow(dataset.pixel_array, cmap=plt.cm.bone)
plt.show()
