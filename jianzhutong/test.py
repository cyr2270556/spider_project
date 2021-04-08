import re

a = '联系电话：010-58368693'
b = '联系电话：01058368693'

par = re.compile(r'\d+-\d+')
par2 = re.compile(r'\d+')
print(re.findall(par, a)[0])
