import os
import pydicom
import csv


def find_first_dicom_file(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dcm"):
                return os.path.join(root, file)
    return None


def read_dicom_tags(file_path):
    dataset = pydicom.dcmread(file_path)
    print(dataset)
    for element in dataset:
        print(f"{element.tag} {element.description()} : {element.value}")


def list_directories_root_level(directory_path):
    directories = [
        d
        for d in os.listdir(directory_path)
        if os.path.isdir(os.path.join(directory_path, d))
    ]
    return directories


def extract_relevant_tags(file_path):
    relevant_tags = [
        "PatientID",
        "StudyDate",
        "StudyTime",
        "AccessionNumber",
        "Modality",
        "Manufacturer",
        "StudyDescription",
        "SeriesDescription",
        "PatientName",
        "PatientBirthDate",
        "PatientSex",
        "BodyPartExamined",
        "SliceThickness",
        "KVP",
        "DistanceSourceToDetector",
        "DistanceSourceToPatient",
        "GantryDetectorTilt",
        "TableHeight",
        "RotationDirection",
        "XRayTubeCurrent",
        "CountryOfResidence",
        "PatientIdentityRemoved",
        "PatientPosition",
    ]

    dataset = pydicom.dcmread(file_path)

    extracted_tags = {}

    for tag in relevant_tags:
        if hasattr(dataset, tag):
            extracted_tags[tag] = getattr(dataset, tag)
        else:
            extracted_tags[tag] = None

    return extracted_tags


def get_all_dicom_files(directory):
    dicom_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dcm"):
                dicom_files.append(os.path.join(directory, file))
    return dicom_files


directories = list_directories_root_level("./")
tags = extract_relevant_tags(find_first_dicom_file(directories[0]))

with open("tags_and_paths.csv", "w", newline="") as csvfile:
    fieldnames = ["items"] + list(tags.keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for directory in directories:
        find_first_dicom_file(directory)
        tags = extract_relevant_tags(find_first_dicom_file(directory))
        paths = get_all_dicom_files(directory)

        # Write tags and paths to a CSV file

        row = {"items": paths}
        row.update(tags)
        writer.writerow(row)
