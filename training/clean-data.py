import pandas as pd
import os

BASE_DIR = "W:/WGU/C964_Capstone/project/dataset/"
img_metadata_loc = BASE_DIR + "Data_Entry_2017.csv"
unusable_img_loc = BASE_DIR + "cxr14_bad_labels.csv"
dx_labels_loc = BASE_DIR + "dx_labels.csv"
out_usable_loc = BASE_DIR + "usable_img_metadata.csv"


def main():
    print("Reading csv")
    img_metadata = pd.read_csv(img_metadata_loc)
    print("Renaming columns")
    img_metadata.rename(columns={
        "Image Index"   : "img_filename",
        "Patient ID"    : "pt_id",
        "Patient Age"   : "pt_age",
        "Patient Gender": "pt_sex",
        "View Position" : "view_position",
        "Image Width"   : "img_width",
        "Image Height"  : "img_height",
        "Spacing X"     : "x_spacing",
        "Spacing Y"     : "y_spacing"}, inplace=True)
    print("Reading unusable csv")
    unusable_imgs = pd.read_csv(unusable_img_loc)
    finding_labels = get_finding_labels(img_metadata)
    save_labels_to_csv(finding_labels)
    img_metadata = remap_labels(img_metadata, finding_labels)
    img_metadata = drop_known_unusable(img_metadata, unusable_imgs)
    img_metadata = add_dx_array(img_metadata, finding_labels)
    save_usable_to_csv(img_metadata)
    print("Finished.")


def get_finding_labels(img_metadata):
    print("Getting finding labels")
    finding_labels = set()
    for labels in pd.unique(img_metadata["Finding Labels"]):
        for label in labels.split("|"):
            finding_labels.add(label.lower().replace(" ", "_"))

    finding_labels = list(finding_labels)
    finding_labels.sort()
    return finding_labels


def save_labels_to_csv(finding_labels):
    print("Saving finding labels to file.")
    pd.Series(finding_labels).to_csv(dx_labels_loc,
                                     index=False,
                                     header=["dx_labels"])


def has_label(label, row):
    return 1 if label in row["Finding Labels"] \
        .lower() \
        .replace(" ", "_") \
        .split("|") \
        else 0


def remap_labels(img_metadata, finding_labels):
    print("Remapping labels")
    for label in finding_labels:
        img_metadata[label] = img_metadata.apply(
                lambda row: has_label(label, row), axis=1)

    img_metadata = img_metadata.drop(["Finding Labels", "Follow-up #"], axis=1)
    return img_metadata


def add_dx_array(img_metadata, finding_labels):
    print("Adding dx array as col")
    img_metadata["dx_labels"] = img_metadata \
        .apply(lambda row: [row[finding_labels].values], 1) \
        .map(lambda vals: vals[0])
    return img_metadata


def drop_known_unusable(img_metadata, unusable_images):
    print("Dropping unusable")
    to_drop = []
    unusable_list = unusable_images["File label"].tolist()
    for index, row in img_metadata.iterrows():
        if row["img_filename"] in unusable_list:
            to_drop.append(index)

    usable_imgs = img_metadata.drop(to_drop, axis=0)
    return usable_imgs[usable_imgs["pt_age"] < 100]


def save_usable_to_csv(img_metadata):
    print("Saving usable to file.")
    img_metadata.to_csv("../dataset/usable_img_metadata.csv", index=False)


if __name__ == "__main__":
    main()
