l = []
for i in range(10):
    l.append(i)  # 和下面一樣
print(l)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
L = [i for i in range(10)]  # 這是list comprehenstin
print(L)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# 也可以加條件判斷
l2 = []
for i in range(10):
    if i % 2 == 0:
        l2.append(i)  # 和下面一樣
print(l2)  # [0, 2, 4, 6, 8]
L2 = [
    i for i in range(10) if i % 2 == 0
]  # 這是list comprehenstin(有條件判斷。if要放在最後，因為放在前面會報錯)
print(L2)  # [0, 2, 4, 6, 8]
