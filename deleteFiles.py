import os
import sys  

def delete_files():
    if sys.argv:
        pwd = sys.argv[1]
    else:
        pwd = os.path.abspath('.')
    root = os.listdir(pwd)
    for i in root:
        with open(f"formats.txt") as file:
            for line in file:
                if i.endswith(line.strip().lower()) or i.endswith(".part"):
                    os.remove(pwd + "/" + i)
