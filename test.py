import check_cross as cc
import numpy as np
'''
start = [10, 10]
print(start == [10, 10])
start.append(10)
print(start)
'''

'''
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y


N = 10
path = np.array([Point(0,0) for i in range(N)])
for p in path:
            print('({},{})'.format(p.x,p.y))

path[0] = np.append(path[0], Point(2,3))
print('path add (2,3) : ')
print(path)

print('sons_path:')
# sons_path = np.array([path[i] for i in range(N)], dtype=object)
sons_path = np.array([p for p in path], dtype=object)
print(sons_path)
sons_path[0] = np.append(sons_path[0], Point(1,2))
print('sons_path add(1,2):')
print(sons_path)
'''
'''
path_x = np.array([None for i in range(10)])
print(path_x)
print(np.append(path_x[0],1))
path_x[0] = np.append(path_x[0],1)
path_x[1] = np.append(path_x[1],[2])
path_x[0,0] = 0
print(path_x)
'''
with open('path.txt','w') as ps:
    ps.write('{} '.format(5))
    ps.write('dfs\n')
