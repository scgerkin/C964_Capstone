import shutil
import os

test_files = [i for i in open("analysis/test_files.txt").read().split("\n")]
valid_files = [i for i in open("analysis/valid_files.txt").read().split("\n")]
train_files = [i for i in open("analysis/train_files.txt").read().split("\n")]

origin = "W:\\WGU\\C964_Capstone\\project\\ml\\dataset\\images"
target = "W:\\tmp\\project"

for item in test_files + valid_files + train_files:
  from_loc = os.path.join(origin, item)
  to_loc = os.path.join(target, item)
  shutil.copyfile(from_loc, to_loc)
