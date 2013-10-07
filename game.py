#!/usr/bin/env python2.7
#-* coding:UTF-8 -*

import pygame
from sys import exit
from pygame.locals import *
import copy

from shapes import *
from common import *

SCREEN = None
SCORE = 0

def init_game():
    global SCREEN
    pygame.init()  
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)  
    SCREEN.fill(BACKGROUND_COLOR)  
    pygame.key.set_repeat(200, 2)
    pygame.display.set_caption("Cool Tetris")
 
def draw(block_data, start_point, map_data, SCREEN, next_block_data=None, game_over=False):  
    _map_data = copy.deepcopy(map_data)  
    _map_start_point = MAP_BEGIN_POINT[:]  
    #更新地图对应的数组数据  
    update_map_data(block_data, start_point, _map_data, next_block_data)
    begin_x = _map_start_point[0]   
    for line in _map_data:  
        for block in line:  
            rect = pygame.Rect(_map_start_point, RECT_SIZE)  
            if block == 1:
                pygame.draw.rect(SCREEN, BLOCK_COLOR, rect) 
                pygame.draw.rect(SCREEN, BLOCK_EDGE_COLOR, rect, 1)
            if block == 2:
                pygame.draw.rect(SCREEN, OUTER_WALL_COLOR, rect)
            _map_start_point[0] += RECT_SIZE[0]  
        _map_start_point[1] += RECT_SIZE[1]  
        _map_start_point[0] = begin_x

    _start_point = SCORE_START_POINT[:]
    _rect_size = RECT_SIZE[:]
    font = pygame.font.Font(None, 32)
    text = font.render("Score: "+str(SCORE), True, [0,0,0])
    SCREEN.blit(text, [_start_point[0]*_rect_size[0], _start_point[1]*_rect_size[1]])

    if game_over:
        text = font.render("Game Over", True, [0,0,0])
        SCREEN.blit(text, [_start_point[0]*_rect_size[0], (_start_point[1]+3)*_rect_size[1]]) 

'''
    更新地图数据(各个方块的值)
'''		
def update_map_data(block_data, start_point, map_data, next_block_data):    
    _start_x, _start_y = start_point[0], start_point[1]   
    for y in range(len(block_data)):  
        for x in range(len(block_data[0])):   
            if _start_x + x <= WALL_WIDTH - 1 or _start_x + x >= MAX_X - WALL_WIDTH:  
                continue  
            if map_data[_start_y + y][_start_x + x] == 0:  
                map_data[_start_y + y][_start_x + x] = block_data[y][x]

    # 更新下一个方块对应的地图数组值
    if next_block_data:
        _lt_point = NEXT_BLOCK_START_POINT[:]
        _start_x, _start_y = _lt_point[0], _lt_point[1]
        for y in range(4):  
            for x in range(4):
                map_data[_start_y + y][_start_x + x] = 2
        for y in range(len(next_block_data)):  
            for x in range(len(next_block_data[0])):
                if next_block_data[y][x] == 1:
                    map_data[_start_y + y][_start_x + x] = 1

'''
    判断方块在地图里面是否发生相撞
'''   
def can_move(block_data, start_point, map_data):  
   _start_x, _start_y = start_point[0], start_point[1]  
   for y in range(len(block_data)):  
       for x in range(len(block_data[0])):  
           if _start_y>=WALL_HEIGHT and block_data[y][x] and map_data[_start_y + y][_start_x + x]:  
                return False  
   return True

def is_game_over(block_data, start_point, map_data, can_move):
    _start_x, _start_y = start_point[0], start_point[1]
    if not can_move and _start_y < WALL_HEIGHT:
        for x in block_data[0]:
           if x==1:
               return True
    return False
 
'''
    判断哪些行可以进行消除，返回可以消除的最底行的y坐标
''' 
def get_max_full_line(map_data):    
    full_line_y = -1  
    #从最底部开始向上扫描，如果发现整行都为1, 则可以消除该行  
    for y in range(MAX_Y-WALL_HEIGHT-1, WALL_HEIGHT, -1):
        if len([x for x in map_data[y] if x == 1 ]) == (MAX_X - WALL_WIDTH*2):  
            full_line_y = y
            break
        elif y == 1:
            break    
    return full_line_y  
 
'''
   循环遍历满格行，数组值依次下移
''' 
def delete_full_lines(map_data):
    global SCORE
    full_line_y = get_max_full_line(map_data)
    while full_line_y >= 0:
        SCORE += 100
        for y in range(full_line_y, WALL_HEIGHT, -1):  
            for x in range(WALL_WIDTH, MAX_X - WALL_WIDTH):
                if y >= 1:
                    map_data[y][x] = map_data[y - 1][x]
                else:
                    for x in range(WALL_WIDTH, MAX_X - WALL_WIDTH):
                        map_data[0][x] = 0
    
        full_line_y = get_max_full_line(map_data)
 
def start_game():  
    init_game()

    _running = True
    _pause = False
    _game_over = False
    _score = 0
    _clock = pygame.time.Clock()  
    _time_passed = 0  
    _map_data = copy.deepcopy(MAP_DATA)  
    _block_data = get_shape()
    _next_block_data = get_shape()
    _block_lt = get_start_point(_block_data) 
	
    draw(_block_data, _block_lt, _map_data, SCREEN, _next_block_data, False)  
    pygame.display.flip()  

    try:  
        while _running:
            if not _pause:
                _time_passed += (_clock.tick(FPS) / 1000.0)
                
                if not _game_over and int(round(_time_passed))/FALL_PER_SECONDS >= 1:  
                    #向下移动一个距离，如不能移动则生成新方块，更新地图
                    _block_lt_x = _block_lt[0]  
                    _block_lt_y = _block_lt[1]  
                    _block_lt_y += SPEED
                    print _block_lt_y
                    if can_move(_block_data,[_block_lt_x,_block_lt_y],_map_data):  
                        _block_lt[1] = _block_lt_y  
                    else:
                        if is_game_over(_block_data, _block_lt, _map_data, False):
                            _game_over = True
                            draw(_block_data, _block_lt, _map_data, SCREEN, next_block_data=None, game_over=True)
                            pygame.display.update()
                        else:
                            update_map_data(_block_data, _block_lt, _map_data, _next_block_data)  
                            delete_full_lines(_map_data)  
                            _block_data = _next_block_data  
                            _next_block_data = get_shape()
                            _block_lt = get_start_point(_block_data)
                            
                    _time_passed = 0
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    _running = False  
                if event.type == pygame.KEYDOWN and not _game_over:
                    if event.key == pygame.K_SPACE:
                        _pause = not _pause
                    if _pause: continue
                    _block_lt_x = _block_lt[0]  
                    _block_lt_y = _block_lt[1]  
                    if event.key == pygame.K_DOWN:
                        if can_move(_block_data, [_block_lt_x, _block_lt_y + 1], _map_data):
                            _block_lt[1] += 1
                    elif event.key == pygame.K_LEFT:  
                        if can_move(_block_data, [_block_lt_x - 1, _block_lt_y], _map_data):  
                            _block_lt[0] -= 1  
                    elif event.key == pygame.K_RIGHT:  
                        if can_move(_block_data, [_block_lt_x + 1, _block_lt_y], _map_data):  
                            _block_lt[0] += 1  
                    elif event.key == pygame.K_UP:  
                        test_rorate = rotate_shape(_block_data)  
                        if can_move(test_rorate, _block_lt, _map_data):  
                            _block_data = test_rorate                    
 
            SCREEN.fill(BACKGROUND_COLOR)  
            draw(_block_data, _block_lt, _map_data, SCREEN, _next_block_data)
            pygame.display.update()  
    finally:
        pygame.quit()
            
 
if __name__ == '__main__':  
    start_game()

