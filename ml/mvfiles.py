import shutil
import os

test_files = [i for i in open("test_files.txt").read().split(",")]
valid_files = [i for i in open("valid_files.txt").read().split(",")]
train_files = [i for i in open("train_files.txt").read().split(",")]

origin = "W:\\WGU\\C964_Capstone\\project\\ml\\dataset\\images"
target = "W:\\tmp\\mltrain"

for item in test_files + valid_files + train_files:
  item = item[:-1] if item[len(item)-1:] == "\n" else item
  from_loc = os.path.join(origin, item)
  to_loc = os.path.join(target, item)
  shutil.copyfile(from_loc, to_loc)
