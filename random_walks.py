# -*- coding: utf-8 -*-
"""
@Module Name: random_walks.py
@Module Docstring: 使用numpy模拟晶格型任意维随机漫步，并对三维随机漫步绘制路线图
@Author: Reclubbit
@Version: 0.1.0
@License: MIT  本项目遵循MIT协议开源，可以自由使用、修改、发布，包括闭源和商用，但需保留作者署名和协议声明
@Environment
    python = 3.12.9
    numpy = 2.0.1
    matplotlib = 3.10.0
"""
import numpy as np
np.set_printoptions(threshold=10, edgeitems=5)  # 设定numpy数组输出显示数量
import matplotlib.pyplot as plt

def simulate_random_walks(N=1000, nsteps=5000, dim=3):
    """
    模拟随机漫步。
    参数：
        N: 漫步次数
        nsteps: 每次漫步的步数
        dim: 空间维度
    """
    if type(N) is not int or type(nsteps) is not int or type(dim) is not int:
        print('参数中请输入整数')
        return
    if N <= 0 or nsteps <= 0 or dim <= 0:
        print('参数中请输入正整数')
        return
    
    # 随机每次每步的移动维度和距离
    rng = np.random.default_rng()
    dim_indices = rng.integers(0, dim, size=(N, nsteps))
    distances = np.random.choice((1, -1), size=(N, nsteps))
    
    # 生成次数轴和步数轴的索引，使用数组索引对位移向量数组的两个轴进行全遍历，并对维度轴索引，在指定位置替换为移动距离
    walks = np.arange(N)
    steps = np.arange(nsteps)
    walk_indices = np.repeat(walks, nsteps).reshape(N, nsteps)
    step_indices = np.tile(steps, N).reshape(N, nsteps)
    displacement_vectors = np.zeros((N, nsteps, dim))  #初始化位移向量
    displacement_vectors[walk_indices, step_indices, dim_indices] = distances
    
    # 累加位移向量，获得每次每步的位置
    pos_without_start = displacement_vectors.cumsum(axis=1)
    
    # 在每次漫步前插入初始位置
    start_pos = np.zeros((N, 1, dim))
    pos = np.concatenate((start_pos, pos_without_start), axis=1)
    
    return pos

def calculate_average_minimum_arrive_time(random_walks, arrive = 30):
    """
    基于欧氏距离，计算随机漫步的最小抵达时间。
    参数：
        random_walks: 随机漫步的模拟数据
        arrive: 目标距离
    """
    # 计算每次每步的当前位置与原点的欧氏距离
    euclidean_distance = np.linalg.norm(random_walks, ord=2, axis=2)

    # 计算欧氏距离达到目标距离的漫步的数量
    arrive_walks = (euclidean_distance >= arrive).any(axis=1)  # 返回布尔数组，表示哪些漫步抵达过目标距离
    arrive_walks_amount = arrive_walks.sum()
    
    # 计算每个抵达过目标距离的漫步的最小抵达时间，和所有漫步的平均最小抵达时间
    arrive_time = (euclidean_distance[arrive_walks] >= arrive).argmax(axis=1)
    mean_arrive_time = arrive_time.mean()
    
    return mean_arrive_time

def draw_3drandom_walk(random_walks, selected_amount=10):
    """
    随机选取指定数量的三维随机漫步，并绘制路线图，保存为svg矢量图
    参数：
        random_walks: 随机漫步的模拟数据
        selected_amount: 用于绘图的漫步数量
    """
    if random_walks.shape[2] != 3:
        print('当前漫步无法绘制，请输入3维随机漫步')
        return
    
    # 随机选取指定数量的漫步
    selected_indices = np.random.choice(random_walks.shape[0], size=selected_amount, replace=False)
    selected_walks = random_walks[selected_indices]
    
    fig = plt.figure(figsize=(20, 16), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    
    for walk in selected_walks:
        x = walk[:, 0]  # x坐标序列
        y = walk[:, 1]  # y坐标序列
        z = walk[:, 2]  # z坐标序列
        ax.plot(x, y, z, alpha=0.3, lw=0.8, color='blue')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('三维随机漫步（选取10次）')
    ax.grid(True, alpha=0.2)  # 浅色网格线
    ax.view_init(elev=30, azim=45)  # 调整视角（仰角30°，方位角45°）
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False
    
    plt.savefig('random_walks_image.svg', format='svg')


# 模拟3维随机漫步
pos3d = simulate_random_walks()
print(pos3d)
minmum_3darrive30_time = calculate_average_minimum_arrive_time(pos3d)
minmum_3darrive20_time = calculate_average_minimum_arrive_time(pos3d, arrive=20)
print(minmum_3darrive30_time)
print(minmum_3darrive20_time)
draw_3drandom_walk(pos3d)

# 模拟4维随机漫步
pos4d = simulate_random_walks(dim=4)
print(pos4d)
minmum_4darrive30_time = calculate_average_minimum_arrive_time(pos4d)
print(minmum_4darrive30_time)
draw_3drandom_walk(pos4d)

errorpos = simulate_random_walks(dim=-1)
errorpos = simulate_random_walks(dim='维度')