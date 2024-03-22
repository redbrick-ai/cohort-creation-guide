# A script for converting from CSV to a JSON file for uploading to RedBrick AI
import csv
import json


def csv_to_list_of_dicts(filename):
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data


# Use the function
cases = csv_to_list_of_dicts("tags_and_paths.csv")


def item_to_redbrick_usable_url(item: str) -> str:
    """
    Convert the item stored in the csv file to something that RedBrick can use.

    This will vary depending on where your images are stored. In this case, images are stored
    at a public url. Yours is probably stored in an S3 bucket and your paths will be generated differently.

    Check docs.redbrickai.com for more information.
    """
    return "https://datasets.redbrickai.com/chest_ct_lidc_idri/" + item


upload_format = []
for case_ in cases:
    # ['LIDC-IDRI-0195/1-102.dcm', 'LIDC-IDRI-0195/1-103.dcm', ...]
    items = case_["items"]

    # parse the way items were stored in the csv file
    items = json.loads(items.replace("'", '"'))
    del case_["items"]

    metadata = case_

    upload_format.append(
        {
            "items": [item_to_redbrick_usable_url(item) for item in items],
            "metaData": metadata,
        }
    )


# Write to a JSON file
with open("upload_format.json", "w+") as file:
    json.dump(upload_format, file, indent=2)
