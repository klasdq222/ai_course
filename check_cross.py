# 区域编码
LEFT_BIT_CODE = 1
RIGHT_BIT_CODE = 2
BOTTOM_BIT_CODE = 4
TOP_BIT_CODE = 8


def convert_pos(pos):
    '''
    convert coordinate
        pos is a list which length is 4.
        pos[0] is the start x of rectangle
        pos[1] is the start y of rectangle
        pos[2] is offset in x,width of rectangle
        pos[3] is offset in y,height of rectangle
        
        new_pos is the position of rectangle in left_bottom and rignt_top
    '''
    new_pos = []
    # left_bottom position of rectangle
    new_pos.append(pos[0])
    new_pos.append(pos[1])
    # right_top position of rectangle
    new_pos.append(pos[0] + pos[2])
    new_pos.append(pos[1] + pos[3])
    return new_pos

def encode(pos, rect):
    code = 0
    if pos[0] < rect[0] :
        code = code | LEFT_BIT_CODE
    if pos[0] > rect[2] :
        code = code | RIGHT_BIT_CODE
    if pos[1] < rect[1] :
        code = code | BOTTOM_BIT_CODE
    if pos[1] > rect[3] :
        code = code | TOP_BIT_CODE
    return code

def is_cross(start, end, rect):
    '''
        start and end is the start point and end point of line segment
        rect is a list including left_bottom and right_top point of rectangle
        
        判断两点形成的线段是否与矩形相交
    '''
    start_code = encode(start, rect)
    end_code = encode(end, rect)
    
  #  print('{}->{}第一次：start_code:{:b}, end_code:{:b}'.format(start, end, start_code, end_code))
    
    # 相或为0 means two point is inner point in rectangle,内部线段也表示相交
    if (start_code | end_code) == 0:
        return True
    # 相与不为0 means two point is at the same external side of rectangle
    if (start_code & end_code) != 0:
       return False
    
    # 垂直线段不在同一侧必相交 , 平行x轴直线不在同一侧也必相交
    if(start[0] == end[0] or start[1] == end[1]):
        return True
    
    # 斜率 , 不为0
    k = (end[1] - start[1]) / (end[0] - start[0]) 
    # 截取坐标
    # 依次检测是否位于 左 右 下 上并截取点位
    if (end_code & LEFT_BIT_CODE) != 0 :
        end[0] = rect[0]
        end[1] = int(start[1] + k * (rect[0] - start[0]))
    if (end_code & RIGHT_BIT_CODE) != 0 :
        end[0] = rect[2]
        end[1] = int(start[1] + k * (rect[2] - start[0]))
    if (end_code & BOTTOM_BIT_CODE) != 0:
        end[0] = int(start[0] + (rect[1] - start[1]) / k)
        end[1] = rect[1]
    if (end_code & TOP_BIT_CODE) != 0:
        end[0] = int(start[0] + (rect[3] - start[1]) / k)
        end[1] = rect[3]
        
    end_code = encode(end, rect)
    
 #   print('{}->{}第二次：start_code:{:b}, end_code:{:b}'.format(start, end, start_code, end_code))
    # 截取坐标之后，两点仍然不在同一侧即为相交
    if (start_code & end_code) != 0:
        return False
    else:
        return True
