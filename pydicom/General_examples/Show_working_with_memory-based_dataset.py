from __future__ import print_function

from io import BytesIO

from pydicom import dcmread, dcmwrite
from pydicom.filebase import DicomFileLike

print(__doc__)

usage = "Usage: python General_examples/Show_working_with_memory-based_dataset.py rtplan2.dcm"


def write_dataset_to_bytes(dataset):
    # 버퍼를 생성한다.
    with BytesIO() as buffer:
        # Dataset의 속성들을 담을 DicomFileLike 객체를 만든다.
        memory_dataset = DicomFileLike(buffer)
        # Dataset을 DicomFileLike 객체에 write 한다.
        dcmwrite(memory_dataset, dataset)
        # 객체에서 읽어오기 위해 rewind 한다.
        memory_dataset.seek(0)
        # 바이트로 읽어서 리턴한다.
        return memory_dataset.read()

def adapt_dataset_from_bytes(blob):
    # bytearr에서 읽어온다.
    dataset = dcmread(BytesIO(blob))
    dataset.is_little_endian = False
    dataset.PatientName = 'Bond^James'
    dataset.PatientID = '007'
    return dataset

class DummyDataBase(object):
    def __init__(self):
        self._blobs = {}

    def save(self, name, blob):
        self._blobs[name] = blob

    def load(self, name):
        return self._blobs[name]


if __name__ == '__main__':
    import sys
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Please supply a dicom file name:\n")
        print(usage)
        sys.exit(-1)
    file_path = sys.argv[1]
    db = DummyDataBase()

    dataset = dcmread(file_path)
    print(dataset)
    ds_bytes = write_dataset_to_bytes(dataset)
    db.save('dataset', ds_bytes)

    read_bytes = db.load('dataset')
    read_dataset = adapt_dataset_from_bytes(read_bytes)
    print(read_bytes)
    dcmwrite(file_path + '_new', read_dataset)
