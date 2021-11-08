import os


pwd = os.path.abspath('.')
root = os.listdir(pwd)
for i in root:
    with open(f"{pwd}/formats.txt") as file:
        for line in file:
            if i.endswith(line.strip().lower()) or i.endswith(".part"):
                os.remove(pwd + "/" + i)
