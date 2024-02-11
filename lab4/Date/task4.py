import datetime

x = datetime.datetime(2005, 11, 17)
y = datetime.datetime(2005, 11, 22)

difference = abs(x - y)
print(difference.total_seconds())