abcd = "car out 01:54:20 [150/150] : [  1NHG-556| 01:53:25|  ⛈️  08 °C | used: 0:00:55]"
split = abcd.split('|')
print(split)

split2 = split[0].split('[')

print(split[2])

print(split2[1][:3])