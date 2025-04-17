a = [1, 2, 3]
for i, el in enumerate(a):
    if el == 2:
        a.pop(i)

print(a)