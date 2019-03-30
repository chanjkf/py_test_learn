# 循环语句
# py中所有的计数都是从0开始的
# for i in range(10):
#     print(i)

lists = [9, 8, 6, 7, 15, 3, 5, 6, 3, 4, 6, 3]
a = 0
for i in lists:

    if i == 6:
        del lists[a]
    a = a + 1

print(lists)
# count = 10
#
# while count < 0:
#     count = count - 1
#     print(count)

# 打印：0123456789

# 打印：0 2 4 6 8 10
# a = 0
# while a <= 10:
#     print(a)
#     a = a + 2


