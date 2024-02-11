import datetime

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)
print(yesterday.strftime("%c") + "\n" + today.strftime("%c")+ "\n"+tomorrow.strftime("%c"))