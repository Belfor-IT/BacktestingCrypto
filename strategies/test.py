import numpy as np
import matplotlib.pyplot as plt

x = [0.2, 1.3, 2.1, 2.9, 3.3]
y = [3.3, 3.9, 4.8, 5.5, 6.9]

(m, b) = np.polyfit(x, y, 1)
print(m, b)

yp = np.polyval([m, b], x)
plt.plot(x, yp)
plt.grid(True)
plt.scatter(x,y)
plt.show()