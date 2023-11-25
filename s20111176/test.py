from datetime import datetime

abcd = datetime.now()
abcd.date = datetime.now().date()

print(abcd)