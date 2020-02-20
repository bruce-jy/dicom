"""
Working with sequences
본 예제는 시퀀스가 어떻게 작동하는지 보여준다.
"""

from pydicom.sequence import Sequence
from pydicom.dataset import Dataset

block_ds1 = Dataset()
block_ds1.BlockType = 'APERTURE'
block_ds1.BlockName = 'Block1'

block_ds2 = Dataset()
block_ds2.BlockType = 'APERTURE'
block_ds2.BlockName = 'Block2'

beam = Dataset()

plan_ds = Dataset()
plan_ds.BeamSequence = Sequence([beam])
plan_ds.BeamSequence[0].BlockSequence = Sequence([block_ds1, block_ds2])
plan_ds.BeamSequence[0].NumberOfBlocks = 2

beam0 = plan_ds.BeamSequence[0]
print('Number of blocks: ', beam0.BlockSequence)

block_ds3 = Dataset()
block_ds2.BlockType = 'APERTURE'
block_ds2.BlockName = 'Block3'

beam0.BlockSequence.append(block_ds3)
print('Number of blocks: ', beam0.BlockSequence)
del plan_ds.BeamSequence[0].BlockSequence[1]

print('Number of blocks: ', beam0.BlockSequence)
