phone = [1,2,3,4,5,6,7,8]


user_info_list = []

for i in phone:
    user_info = {}
    user_info["phone"] = i
    user_info["token"] = "sadfa"
    user_info_list.append(user_info)

print(user_info_list)