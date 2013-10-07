#!/usr/bin/env python2.7
#-* coding:UTF-8 -*
import random

NT_SHAPES = [
    [
        [1,1,0],
        [0,1,0],
        [0,1,0]
    ],
    [
        [1,1,0],
        [0,1,1],
        [0,0,0]
    ],
    [
        [0,1,1],
        [1,1,0],
        [0,0,0]
    ],
    [
        [1,1,1],
        [0,1,0],
        [0,0,0]
    ],
    [
        [0,0,0,0],
        [1,1,1,1],
        [0,0,0,0],
        [0,0,0,0]
    ],
    [
        [0,1,1],
        [0,1,0],
        [0,1,0]
    ],
    [
        [1,1],
        [1,1]
    ]
]

# 随机生成方块
def get_shape():
    shape = random.choice(NT_SHAPES)
    rotate_cnt = random.randint(0,3)
    for i in range(0,rotate_cnt):
    	shape = rotate_shape(shape)
    return shape

# 90°旋转方块
def rotate_shape(shape):
    h = len(shape)
    w = len(shape[0])

    new_shape = [[0 for col in range(w)] for row in range(h)]
    for x in range(w):
        for y in range(h-1, -1, -1):
            new_shape[x][y] = shape[y][h-1-x]

    return new_shape

