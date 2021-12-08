
# from pandas.io import json
# temp_all = {1}
# val = [*range(0, 500, 1)]
# for i in range(0, 500):
#     val[i] = i

# print(val)
# temp_all.update(val)
# print(len(val))
# js = json.dumps(temp_all)
# file = open('static/json/label.json', 'w')
# file.write(js)
# file.close()

l = [[1, 2, 3, 4], [12, 2, 3, 4], [13, 2, 3, 4]]
key = ["0", "1", "3"]
d = {}
for k in key:
    for v in l:
        d[k] = v
    l.remove(v)

print(d)
