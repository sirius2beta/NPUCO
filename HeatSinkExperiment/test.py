import matplotlib.pyplot as plt
import numpy as np

# 生成數據
x = np.linspace(0, 10, 100)
y = np.sin(x)

# 畫圖
plt.figure()
plt.plot(x, y)

# 隱藏座標軸
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)

# 顯示圖表
plt.show()
