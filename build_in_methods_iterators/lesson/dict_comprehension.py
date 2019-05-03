import string

data = {k: v for v, k in enumerate(string.ascii_lowercase, start=1)}

data_keys = [f"Key is : {x}; Value is {y}" for x, y in enumerate(data.items())]

data_keys_1 = [f"Key is : {x}; Value is {y}" for x, y in data.items()]
# this will fail
# data_keys_2 = [f"Key is : {x}; Value is {y}" for x, y, c in enumerate(data.items())]

data = {k: v for v, k in enumerate(string.ascii_lowercase, start=1)}
dict_if_syntax = {k: v for v, k in enumerate(string.ascii_lowercase, start=1) if v % 2 == 0}

print(data_keys)
print(data_keys_1)
print(dict_if_syntax)
