#!/bin/bash

export GDRIVE=drive/MyDrive/ml/dataset
export TARGET=/content/dataset

mkdir $TARGET
mkdir $TARGET/images

mkdir /content/logs
mkdir /content/checkpoints
mkdir /content/models
mkdir /content/models/save

cp $GDRIVE/images/mltrain.zip /content/images.zip
unzip /content/images.zip -d $TARGET/images/
mv $TARGET/images/mltrain/* $TARGET/images/

cp $GDRIVE/cxr14_bad_labels.csv $TARGET/cxr14_bad_labels.csv
cp $GDRIVE/Data_Entry_2017.csv $TARGET/Data_Entry_2017.csv
cp $GDRIVE/dx_labels.csv $TARGET/dx_labels.csv
cp $GDRIVE/usable_img_metadata.csv $TARGET/usable_img_metadata.csv