#在使用mongo的情况下 去重
a = [{"b": 1}, {"b": 2}, {"b": 3}, {"b": 4}, {"b": 3}, {"b": 3}, {"b": 4}]

for i in range(len(a)):
    for k in range(i+1, len(a)):
        if a[i]["b"] == a[k]["b"]:
            a[k]["b"]=None

print(a)
