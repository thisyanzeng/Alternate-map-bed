import os

import numpy as np
from scipy import interpolate

# 读取二维数据（裁剪应该是在插值之后进行，不然NaN数据影响插值结果）
data = []

with open("RectangleData.txt") as fileObj:
    lines = fileObj.readlines()
    for line in lines:
        data.append(list(map(float, line.split(" "))))

lon = np.linspace(108.75, 114.25, 55)      # 经度55个格点
lat = np.linspace(-30.15, -24.55, 56)      # 维度56个格点
# 纬度每个格点之间的距离为： 110.95 km
# 经度每个格点之间的距离取南北纬度跨度的固定值：(111.314*cos-30.15° + 111.314*cos-24.5°)/2=98.77 km

# 计算插值函数
data = np.array(data)
func = interpolate.interp2d(lon, lat, data, kind='cubic')


target = 1  # 目标1 km
LonCount = int(np.ceil((110.95 / target) * 55))       # 格点个数向上取整
LatCount = int(np.ceil(np.ceil(98.77 / target) * 56))
# 新的坐标系
newLon = np.linspace(108.75, 114.25, LonCount)
newLat = np.linspace(-30.15, -24.55, LatCount)

# 计算插值后的结果
result = func(newLon, newLat)

for i in range(len(result)):
    # 保留6位有效数字
    result[i] = [round(v, 6) for v in result[i]]


with open("result.txt", "w") as fileObj:
    for res in result:
        fileObj.write(" ".join(list(map(str, res))))
        fileObj.write(os.linesep)

