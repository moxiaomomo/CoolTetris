#!/usr/bin/env python2.7
#-*- encoding:utf-8 -*-

# 初始化地图，并为活动空间外墙壁赋值
def init_map(max_x, max_y, wall_widith, wall_height):  
    maps = [[0 for col in range(max_x)]for cell in range(max_y)]  
    for y in range(max_y):  
        for x in range(max_x):  
            if x < wall_widith or x > max_x - wall_widith - 1 or y > max_y - wall_height-1 or y < WALL_HEIGHT:  
                    maps[y][x] = 2 
    return maps

# 获取新方块的起始位置  
def get_start_point(shape):
    h = len(shape)
    return [CENTER_X, WALL_HEIGHT-h]

SCREEN_SIZE = WIDTH, HEIGHT = [760, 560]
BACKGROUND_COLOR = (33, 124, 33)  
BLOCK_COLOR = (123, 22, 33)  
BLOCK_EDGE_COLOR = (200, 233, 200)
OUTER_WALL_COLOR = (51, 51, 51) 
 
WALL_WIDTH = 11 
WALL_HEIGHT = 3  
#地图从(0,0)坐标开始画  
MAP_BEGIN_POINT = [0, 0]  
#地图的最大行数和列数  
MAX_X, MAX_Y = 38, 28 
#方块的边长  
RECT_SIZE = [WIDTH/MAX_X, HEIGHT/MAX_Y]  
#屏幕中央的x坐标  
CENTER_X = int(MAX_X / 2) - 3
#地图的数据  
MAP_DATA = init_map(MAX_X, MAX_Y, WALL_WIDTH, WALL_HEIGHT)  
# 展示下一方块的区域起始位置
NEXT_BLOCK_START_POINT = [WALL_HEIGHT, WALL_HEIGHT]
# 展示分数的区域起始位置
SCORE_START_POINT = [MAX_X - WALL_WIDTH + 1, WALL_HEIGHT]
#每秒的帧数  
FPS = 40  
#方块的下落速度  
SPEED = 1  
#方块自由体积下落的时间间隔  
FALL_PER_SECONDS = 1  
