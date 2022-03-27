# Parses the given file name to the folder it should go to
# It is assumed that file given through here will always be a KOSP file

from typing import List


def parse_kosp(file_name: str) -> str:
    print(file_name)
    if "KOSP" not in file_name:
        raise Exception("This is not a KOSP file")
    elif "user-OFFICIAL" not in file_name:
        raise Exception(
            "This build isn't official. You are not allowed to upload")

    parts: List[str] = file_name.split("-")[1:]
    android_version = "A" + str(10 + int(float(parts[0])))
    device_name = parts[1]
    return android_version + "/" + device_name