import pydicom
from pydicom.data import get_testdata_file

filename = get_testdata_file("rtplan.dcm")
ds = pydicom.dcmread(filename)
print(ds.PatientName)
print(ds.dir("setup"))
print('ds')
print(ds.PatientSetupSequence[0])
ds.PatientSetupSequence[0].PatientPosition = 'HFP'

ds.save_as("rtplan2.dcm")
print('ds2')
ds2 = pydicom.dcmread('c:/Users/vuno/PycharmProjects/dicom/pydicom/rtplan2.dcm')
print(ds2.PatientSetupSequence[0])

