
sol = {1: [1, 2, 3], 2: [1, 2, 3]}
a = {key: value[0:-1] for key, value in sol.items()}
print(a)