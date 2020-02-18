import pydicom
from pydicom.data import get_testdata_files

print(__doc__)

filename = get_testdata_files('MR_small.dcm')[0]
ds = pydicom.dcmread(filename)

data = ds.pixel_array
print('The image has {} x {} voxels'.format(data.shape[0], data.shape[1]))
data_downsampling = data[::8, ::8]
print('The downsampled image has {} x {} voxels'.format(
    data_downsampling.shape[0], data_downsampling.shape[1]))

ds.PixelData = data_downsampling.tobytes()
ds.Rows, ds.Columns = data_downsampling.shape

print('The information of the data set after downsampling: \n')
print(ds)
