# 🔹 Bài 4: Flatten Nested List

# Yêu cầu:
# Cho list lồng nhau, flatten thành list 1 chiều
def flatten(lst):
    res = []
    for x in lst:
        if isinstance(x, list):
            res.extend(flatten(x))
        else:
            res.append(x)
    return res

print(flatten([1, [2, [3, 4, 5], 5], 6]))