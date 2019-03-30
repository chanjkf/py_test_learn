
# t = open("sweet.txt", "w")
# t.writelines("love")
# t.close()

with open("sweet.txt", "w") as file:
    file.writelines("love")
