import pydicom
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
from pydicom.data import get_testdata_file

files = []
filename = get_testdata_file('CT_small.dcm')

# print('glob: {}'.format(sys.argv[1]))
# for fname in glob.glob(sys.argv[1], recursive=False):
print('glob: {}'.format(filename))
for fname in glob.glob(filename, recursive=False):
    print("loading: {}".format(fname))
    files.append(pydicom.dcmread(fname))

print("file count: {}".format(len(files)))

slices = []
skipcount = 0
for f in files:
    if hasattr(f, 'SliceLocation'):
        slices.append(f)
    else:
        skipcount = skipcount + 1

print('skipped, no SliceLocation: {}'.format(skipcount))

slices = sorted(slices, key=lambda s: s.SliceLocation)

ps = slices[0].PixelSpacing
ss = slices[0].SliceThickness
ax_aspect = ps[1]/ps[0]
sag_aspect = ps[1]/ss
cor_aspect = ss/ps[0]

img_shape = list(slices[0].pixel_array.shape)
img_shape.append(len(slices))
img3d = np.zeros(img_shape)

for i, s in enumerate(slices):
    img2d = s.pixel_array
    img3d[:, :, i] = img2d

a1 = plt.subplot(2, 2, 1)
plt.imshow(img3d[:, :, img_shape[2]//2])
a1.set_aspect(ax_aspect)

a2 = plt.subplot(2, 2, 2)
plt.imshow(img3d[:, img_shape[1]//2, :])
a2.set_aspect(sag_aspect)

a3 = plt.subplot(2, 2, 3)
plt.imshow(img3d[img_shape[1]//2, :, :].T)
a3.set_aspect(cor_aspect)

plt.show()
