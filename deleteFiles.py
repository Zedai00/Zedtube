import os
import sys


def delete_files():
    formats = ["MP4", "MOV", "FLV", "AVI", "WEBM", "MKV"]
    if len(sys.argv) > 1:
        pwd = sys.argv[1]
    else:
        pwd = os.path.abspath(".")
    root = os.listdir(pwd)
    for i in root:
        for line in formats:
            if i.endswith(line.strip().lower()) or i.endswith(".part"):
                os.remove(pwd + "/" + i)


if __name__ == "__main__":
    delete_files()
