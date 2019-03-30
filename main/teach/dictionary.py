girl = {"name": "sweet", "age": 18, "job": "test", "like": "cat"}
girl1 = {"name": "tian", "age": 30, "job": "test", "like": "??"}

test_group = [girl, girl1]
for i in test_group:
    if i["name"] == "sweet":
        print(520)
    else:
        girl1["like"] = "test"
print(test_group)


#
# print(test_group)
#
# print(girl["name"])
# print(girl["age"])
# print(girl["job"])
# print(girl)
#
# girl["like"] = "dog"
# print(girl["like"])
#
# del girl["like"]
# print(girl)
#
# girl["name"]
# girl.get("name")
# print(girl.keys())
# print(girl.values())

