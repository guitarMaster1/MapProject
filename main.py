n = int(input())
data = {
    'янв': [],
    'фев': [],
    'мар': [],
    'апр': [],
    'май': [],
    'июн': [],
    "июл": [],
    "авг": [],
    "сен": [],
    "окт": [],
    "ноя": [],
    "дек": []
}
for z in range(n):
    s = input().split()
    if s[2] in data:
        data[s[2]].append(s[0])
q = int(input())
for z in range(q):
    s = input()
    month_bithd = data[s]
    month_bithd.sort()
    print(' '.join(month_bithd))
