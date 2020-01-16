#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :opcv2048.py
# @Time      :2020/1/15 15:03
# @Author    :Raink


import cv2
import numpy as np
import random


# 用于随机产生新元素 为了方便调整概率以列表形式创建
new_nums = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]
new_vals = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 4]
# 4x4的游戏数据
data = np.array([[0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]])
# 用于记录鼠标滑动的数据： 开始（按下） 和结束（抬起）
m_start = [0, 0]
m_end = [0, 0]


# 创建背景图
def create_back():
    color = (255, 255, 255)
    img = np.array([[color for i in range(450)]for j in range(450)], dtype=np.uint8)
    return img


# 创建色块
def create_block(num):
    # 获取数字位数
    index = len(str(num))
    # 16个格最大数字不会超过2的16次方 也就是65536，也就是5位数，
    # 根据数字长度来确定块的颜色、文字大小、粗细、位置
    greens = [180, 162, 144, 126, 108]
    font_sizes = [2.75, 1.75, 1.25, 1, 0.875]
    thickness_s = [6, 5, 4, 3, 2]
    color = (54, greens[index - 1], 60)
    font_size = font_sizes[index-1]
    thickness = thickness_s[index - 1]
    pos = (int(24 - (3.3 * index)), int(85 - (6.5 * index)))
    # 创建数字块
    img = np.array([[color for i in range(100)] for j in range(100)], dtype=np.uint8)
    if num > 0:
        #  大于0的数字进行绘制
        cv2.putText(img, str(num), pos, cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), thickness)
    return img


# 产生新元素
def new_elements():
    pos_list_t = np.where(data == 0)
    pos_list = [(pos_list_t[0][i], pos_list_t[1][i]) for i in range(len(pos_list_t[0]))]
    # 随机一个新元素的个数
    nums = random.choice(new_nums)
    if nums >= len(pos_list):
        nums = 1
    # 随机一个新元素的位置
    new_poss = random.sample(pos_list, nums)
    for pos in new_poss:
        # 随机一个新元素的数值
        data[pos[0]][pos[1]] = random.choice(new_vals)


# 向左滑动
def to_left():
    for i in range(4):
        index = 0
        t = [0, 0, 0, 0]
        for x in range(3):
            if data[i][x] > 0:
                t[index] = data[i][x]
                data[i][x] = 0
                n = x + 1
                while data[i][n] == 0 and n < 3:
                    n = n + 1
                if t[index] == data[i][n]:
                    t[index], data[i][n] = t[index] + data[i][n], 0
                    x += 1
                index += 1
        t[index] = data[i][3]
        data[i] = t


# 向右
def to_right():
    for i in range(4):
        index = 3
        t = [0, 0, 0, 0]
        for x in range(3, 0, -1):
            if data[i][x] > 0:
                t[index] = data[i][x]
                data[i][x] = 0
                n = x - 1
                while data[i][n] == 0 and n >= 0:
                    n = n - 1
                if t[index] == data[i][n]:
                    t[index], data[i][n] = t[index] + data[i][n], 0
                    x -= 1
                index -= 1
        t[index] = data[i][0]
        data[i] = t


# 向上
def to_top():
    for i in range(4):
        index = 0
        t = [0, 0, 0, 0]
        for x in range(3):
            if data[x][i] > 0:
                t[index] = data[x][i]
                data[x][i] = 0
                n = x + 1
                while data[n][i] == 0 and n < 3:
                    n = n + 1
                if t[index] == data[n][i]:
                    t[index], data[n][i] = t[index] + data[n][i], 0
                    x += 1
                index += 1
        t[index] = data[3][i]
        data[:, i] = t


# 向下
def to_bottom():
    for i in range(4):
        index = 3
        t = [0, 0, 0, 0]
        for x in range(3, 0, -1):
            if data[x][i] > 0:
                t[index] = data[x][i]
                data[x][i] = 0
                n = x - 1
                while data[n][i] == 0 and n >= 0:
                    n = n - 1
                if t[index] == data[n][i]:
                    t[index], data[n][i] = t[index] + data[n][i], 0
                    x -= 1
                index -= 1
        t[index] = data[0][i]
        data[:, i] = t


# 生成当前画面
def game_image():
    img = create_back()
    for i in range(4):
        for j in range(4):
            x_start = 10 + 110 * i
            y_start = 10 + 110 * j
            x_end = x_start + 100
            y_end = y_start + 100
            block = create_block(data[i][j])
            img[x_start:x_end, y_start:y_end] = block
    return img


# 鼠标事件
def mouse_event(event, x, y, flags, param):
    global m_start, m_end
    if event == cv2.EVENT_LBUTTONDOWN:
        m_start = [x, y]
    if event == cv2.EVENT_LBUTTONUP:
        m_end = [x, y]
        dx = m_end[0] - m_start[0]
        dy = m_end[1] - m_start[1]
        if abs(dx) > abs(dy):
            if dx > 0:
                to_right()
            else:
                to_left()
        else:
            if dy > 0:
                to_bottom()
            else:
                to_top()
        img = game_image()
        cv2.imshow("2048", img)
        cv2.waitKey(100)  # 滑动后更新画面，停顿一下再插入新的数字使有动画的感觉
        new_elements()
        img = game_image()
        cv2.imshow("2048", img)
        m_start = [0, 0]
        m_end = [0, 0]


# 初始化游戏界面
def game_run():
    cv2.namedWindow("2048", cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback("2048", mouse_event)
    new_elements()
    img = game_image()
    cv2.imshow("2048", img)
    cv2.waitKey(0)


if __name__ == "__main__":
    game_run()