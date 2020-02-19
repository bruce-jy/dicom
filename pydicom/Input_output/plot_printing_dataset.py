"""
Format the output of the data set printing
본 예제는 사용자가 원하는 포멧으로 데이터셋을 어떻게 보여줄지 테스트 해보는 예제입니다.
"""

from __future__ import print_function

import pydicom
from pydicom.data import get_testdata_files

print(__doc__)

def myprint(dataset, indent=0):
    """Go through all items in the dataset and print them with custom format

    Modelled after Dataset._pretty_str()
    """
    dont_print = ['Pixel Data', 'File Meta Information Version']

    indent_string = "   " * indent
    next_indent_string = "   " * (indent + 1)

    print('origin dataset:\n', dataset)
    print('\n', '-' * 80, '\n')

    for data_element in dataset:
        if data_element.VR == "SQ":
            print(indent_string, data_element.name)
            for sequence_item in data_element.value:
                myprint(sequence_item, indent + 1)
                print(next_indent_string + '-'*10)
        else:
            if data_element.name in dont_print:
                print("""<item not printed -- in the "don't print" list>""")
            else:
                repr_value = repr(data_element.value)
                if len(repr_value) > 50:
                    repr_value = repr_value[:50] + "..."
                print('{0:s} {1:s} = {2:s}'.format(indent_string,
                                                   data_element.name,
                                                   repr_value))

filename = get_testdata_files('MR_small.dcm')[0]
ds = pydicom.dcmread(filename)

myprint(ds)
