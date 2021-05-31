# 显示坐标点位
import random
import math
import numpy as np
import check_cross as cc

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

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
    设定目标函数为：
        （已经走过的距离 + 当前位置到终点位置距离） / 整个地图的最大长度
    这个值越小，说明路径越越短。
'''
# sigmod函数的倒数
def reciprocal_sigmod(x):
    return 1 + math.exp(-x)
# 距离公式
def calc_distance(start, end):
    return np.sqrt((end[0]-start[0])*(end[0]-start[0]) + (end[1]-start[1])*(end[1]-start[1]))
# 计算当前点到终点的向量 与 当前点到起点的向量 余弦值
def calc_cosin(vec1 , vec2):
    #return (p[0]*(64-p[0]) + p[1]*(64-p[1]))/(np.sqrt(p[0]*p[0] + p[1]*p[1]) + np.sqrt((64-p[0])*(64-p[0]) + (64-p[1])*(64-p[1])))
    return (vec1[0]*vec2[0] + vec1[1]*vec2[1])/(np.sqrt(vec1[0]**2 + vec1[1]**2)+ np.sqrt(vec2[0]**2 + vec2[1]**2))
def calc_score(traveled_distance, to_des_distance, cosin):
#     return (traveled_distance + to_des_distance) / (64 * 1.414)
    return traveled_distance + to_des_distance + reciprocal_sigmod(cosin)
#    return traveled_distance + to_des_distance

'''
    进化算法主体部分
'''
# 种群个体数量
N = 10
# 亲本参数
parents = np.zeros((4,N)).astype(int)
# 亲本对应走过的路径
path = np.array([Point(0,0) for i in range(N)])
passed_distance = np.array([0.0 for i in range(N)])

# sigma>0
sigma = np.random.normal(loc=1, scale=1, size=2)
while (sigma > 0).sum() != 2 :
    sigma = np.random.normal(loc=1, scale=1, size=2)
print('sigma: {}'.format(sigma))

# 终止条件，已有个体到达终点
to_des = True

while to_des:
    
    # 迭代产生子体
    i = 0
    # 子体参数
    sons = np.zeros((4,N)).astype(int)
    # 子体走过的路径
    sons_path = np.array([p for p in path], dtype=object)
    sons_passed_distance = np.array([0.0 for i in range(N)])
    while i < N:
        # 0. 此亲本已经到达终点，不再对此亲本变异
    #    print('parents[:2,i]: {}'.format(parents[:2,i]))
        if all(parents[:2,i] == [64, 64]):
            i += 1
            continue
            
        # 1. 亲本变异出子本
        var = np.array(parents[:2,i] + np.sqrt(sigma)*np.random.normal(loc=2, scale=1, size=2)).astype(int)
#         var.astype(int)
        
#        print('var : {}'.format(var))
        
        # 2. 子本是否可用，即一步可达或没有越界
        if var[0]>=0 and var[0]<=64 and var[1]>=0 and var[1]<=64 :
            ob_num = 0
            # 查看子体位置是否一步可达
            for ob in obstacles:
               # print('parents[:2,i]:{} ,var: {} , ob: {}, cc.convert_pos(ob): {}'.format(parents[:2,i], var, ob, cc.convert_pos(ob)))
                if cc.is_cross(parents[:2,i], var, cc.convert_pos(ob)):
                    break
                ob_num += 1
            
            # 若ob_num等于障碍物数量，说明没有相交障碍物
            if ob_num == len(obstacles):
                # 生成当前子体坐标
                sons[:2,i] = var
                # 当前子体上一步位置
                sons[2:,i] = parents[:2,i]
                # 添加子体走过路径
                sons_path[i] = np.append(sons_path[i], Point(sons[0,i],sons[1,i]))
                # 添加子体走过的路径长度
                sons_passed_distance[i] += calc_distance(sons[2:,i], sons[:2,i])
#                print('第{}个新生子体:{}->{}'.format(i+1, parents[:2,i],  var))
                # 下一子体
                i += 1
        # 3. 产生下一个子本的sigma
        sigma = np.random.normal(loc=2, scale=1, size=2)
        if(sigma[0]<0):
            sigma[0] = 1
        if(sigma[1]<0):
            sigma[1] = 1
    
    # 进行挑选步骤
    all_samples = np.hstack((parents, sons))
    all_path = np.hstack((path, sons_path))
    all_distance = np.hstack((passed_distance, sons_passed_distance))
    
#    print('all_samples :\n {}'.format(all_samples))
#     print('all_distance:{}'.format(all_distance))
    
    u = 0
    score = np.array([0.0 for i in range(int(2*N))])
    
#     all_weight = np.array([None for i in range(2*N)])
    
#     for i in range(2*N):
#         traveled_dist = calc_distance(all_samples[2:,i], all_samples[:2,i])
#         to_des_dist =  calc_distance(all_samples[:2,i],[64,64])
#         print('{}-{}traveled_distance:{}, {}->{}to_des_distance:{}'.format(all_samples[2:,i], all_samples[:2,i],
#                                                                      traveled_dist, all_samples[:2,i],[64,64], to_des_dist))
#         all_weight[i] = calc_score(traveled_dist, to_des_dist)
#         print('score:{}'.format(all_weight[i]))
    
    all_weight = np.array([calc_score(all_distance[i], calc_distance(all_samples[:2,i],[64,64]), calc_cosin(all_samples[:2,i]-all_samples[2:,i], [64,64]-all_samples[:2,i])) for i in range(2*N)])
#     print('all_weight: \n{}'.format(all_weight))
    
    while u<2*N:
        # 取样索引
        q_index = np.array(random.sample(range(int(2*N)), int(0.9*N)))
#         print('q_index : \n{}'.format(q_index))
        # 获取对应索引的权重值
        q_weight = all_weight[q_index]
        # 获取比对样本u的植
        u_weight = all_weight[u]

        # 计算样本u的得分
        u_score = 0
        for q_w in q_weight:
            if u_weight <= q_w:
                u_score += 1
        score[u] = u_score
        
#         print('第{}个,u_weight: {}, q_weight : {},u_score:{}'.format(u+1, u_weight, q_weight, u_score))
        u += 1
#    print('score:\n{}'.format(score))
    # 对得分数组进行从小到大排序
    sort_index = np.argsort(score)
#    print('sort_index:\n{}'.format(sort_index))
    next_gen_index = sort_index[N:2*N]
    # 取出前n个值为下一代亲本
    parents = all_samples[:,next_gen_index]
    path = all_path[next_gen_index]
#    print('next_gen_index:\n{}'.format(next_gen_index))
#    print('parents:\n{}'.format(parents))
    
    for ps in path:
        if type(ps) is Point:
            print('({},{})'.format(ps.x,ps.y), end='->')
        else:
            for p in ps:
                print('({},{})'.format(p.x,p.y), end='->')
                if(p.x==64 and p.y==64):
                    to_des = False
        print()

# 将最终结果写入path文件中
with open('path.txt','w') as pf:
    for ps in path:
        for i in range(2):
            for p in ps:
                if(i==0):
                    pf.write('{} '.format(p.x))
                else:
                    pf.write('{} '.format(p.y))
            pf.write('\n')


