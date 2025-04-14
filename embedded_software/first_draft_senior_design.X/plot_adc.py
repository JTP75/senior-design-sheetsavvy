import numpy as np
import matplotlib.pyplot as plt

# @np.vectorize
# def fract2float(v: int) -> float:
#     sign = -1 if (v & 0x8000) else 1
#     fraction = 0
#     for i in range(15):
#         fraction += ((v >> (14 - i)) & 1) * (2 ** -(i + 1))
#     return sign * fraction

# print(hex2float("0xC000,"))

# def hex_converter(x):
#     return int(x, 16)

data = np.loadtxt("a5_sqm.csv")

# print(data)


plt.plot(data)
plt.show()