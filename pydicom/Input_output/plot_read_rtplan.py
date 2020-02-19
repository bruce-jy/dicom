"""
Read RTPLAN DICOM and list information
RTPLAN(Radiation treatment planning) DICOM 파일의 beams 안에 있는 기본 정보를 list로 보여주기
"""
from __future__ import print_function

import pydicom
from pydicom.data import get_testdata_files

print(__doc__)


def list_beams(plan_dataset):
    """Summarizes the RTPLAN beam information in the dataset."""
    print("BeamSequence Data : \n{}".format(plan_dataset.BeamSequence))
    lines = ["{name:^13s} {num:^8s} {gantry:^8s} {ssd:^11s}".format(
        name="Beam name", num="Number", gantry="Gantry", ssd="SSD (cm)"
    )]
    for beam in plan_dataset.BeamSequence:
        cp0 = beam.ControlPointSequence[0]
        SSD = float(cp0.SourceToSurfaceDistance / 10)
        lines.append("{b.BeamName:^13s} {b.BeamNumber:^8d} {gantry:^8.1f} {ssd:^8.1f}".
                     format(b=beam, gantry=cp0.GantryAngle, ssd=SSD))

    return "\n".join(lines)

filename = get_testdata_files('rtplan.dcm')[0]
dataset = pydicom.dcmread(filename)
print(list_beams(dataset))