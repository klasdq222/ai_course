import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as mp

'''
    从文件中读取障碍物位置数据
    lines
        for a in lines:
            number = int(a)
            print(number)
            
        lines = line.split()
'''
print('读取地图数据: ')
print('障碍物数据读取中...')
obstacles = []
with open('obstacle.txt',mode='r') as f:
    for i in range(20):
        line = f.readline()
        lines = [int(l) for l in line.split()]
        obstacles.append(lines)
print(obstacles)
print('障碍物数据读取完成!')
'''
print('地图数据读取中...')
map = []
with open('map.txt',mode='r') as f:
    for i in range(64):
        line = f.readline()
        lines = [int(l) for l in line.split()]
        map.append(lines)
print('地图数据读取完成!')
'''
'''
    创建障碍物区域
'''
rects = [mp.Rectangle(o[:2],o[2],o[3],color='dimgrey') for o in obstacles]

'''
    设置行进路线
'''
path_x = []
path_y = []
with open('path_1.txt','r') as pf:
    for i in range(10):
        x_line = pf.readline()
        y_line = pf.readline()
        temp_x = [int(x) for x in x_line.split()]
        temp_y = [int(y) for y in y_line.split()]
#        print('\n{}\n temp_x:{}\n temp_y:{}'.format(i+1, temp_x, temp_y))
        if(temp_x[-1]==64 and temp_y[-1]==64):
#            temp_x = [x+0.5 for x in temp_x]
#            temp_y = [y+0.5 for y in temp_y]
            path_x.append(temp_x)
            path_y.append(temp_y)


for i in range(len(path_x)):
    for j in range(len(path_x[i])):
        print('({},{})->'.format(path_x[i][j],path_y[i][j]), end='')
    print('')

fig,ax = plt.subplots(figsize=(8,8))
ax.set_ylabel("y")
ax.set_xlabel("x")

# 设置网格发展，使其显示为64*64的网格
ax.minorticks_on()
'''
ax.set_xlim([-1,65])
ax.set_ylim([-1,65])
'''
ax.set_xlim([0,64])
ax.set_ylim([0,64])
minorLocator = MultipleLocator(1)
ax.yaxis.set_minor_locator(minorLocator)
ax.xaxis.set_minor_locator(minorLocator)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
'''
ax.set_xticks([])
ax.set_yticks([])
'''
# 绘制障碍物
for rect in rects:
    ax.add_patch(rect)

# 一次性绘制多个线条
plt.grid(b=True,which="both",c='dodgerblue')

'''
for i in range(len(path_x)):
    ax.plot(path_x[i], path_y[i], color = 'r')
'''
ax.plot(path_x[0], path_y[0], color='r')

# 保存到本地
# plt.axis('off')

plt.show()