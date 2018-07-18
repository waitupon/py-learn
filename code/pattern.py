import re

flag = re.match('www', '2.123')

print(flag)


print(re.search('www', 'www.runoob.com').span())  # 在起始位置匹配
print(re.search('com', 'www.runoob.com').span())