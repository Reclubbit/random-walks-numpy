# -*- coding: utf-8 -*-
"""
@Module Name: random_walks.py
@Module Docstring: 使用numpy模拟晶格型任意维随机漫步，并对三维随机漫步绘制路线图
@Author: Reclubbit
@Version: 0.1.0
@License: MIT  本项目遵循MIT协议开源，可以自由使用、修改、发布，包括闭源和商用，但需保留作者署名和协议声明
"""
import numpy as np
np.set_printoptions(threshold=10, edgeitems=5)  # 设定numpy数组输出显示数量


def validate_int(x: int | np.integer) -> None:
    """ 检测输入参数是否为正整数。 """
    if isinstance(x, bool):
        raise TypeError(f"参数不能为布尔值，当前类型：{type(x)}")
    if not (isinstance(x, int) or isinstance(x, np.integer)):
        raise TypeError(f"参数必须为 int 或 numpy 整数类型，当前类型：{type(x)}")
    if x <= 0:
        raise ValueError(f"参数必须为正整数，当前值：{x}")

class RandomWalk:
    """
    一个 N 维随机漫步模拟器。
    
    属性：
        dim (int): 随机漫步的维度，必须为正整数。
        seed (int, optional): 随机数种子（默认None，若设置，可保证随机过程的可复现性）。
        
    方法：
        append_steps: 给当前的所有随机漫步全部增加 n 步。
        append_runs: 增加 n 个与当前漫步相同步数的随机漫步。
    
    """
    def __init__(self, dim: int, seed: int = None):
        self.dim = dim   # 维度
        self.seed = seed  # 随机种子
        
        # 参数检测
        validate_int(self.dim)
        if self.seed is not None:
            validate_int(self.seed)
        
        self.rng = np.random.default_rng(seed=self.seed)  # numpy随机数生成器
        self.pos = np.zeros((1, 1, self.dim))  # 漫步初始位置
    
    def append_steps(self,
                     nsteps : int | np.integer = 1) -> np.ndarray:
        """
        给当前的所有随机漫步全部增加 n 步。
        
        参数：
            nsteps(int): 当前每次漫步的新增步数，必须为正整数，默认为 1
        """
        
        # 参数检测
        validate_int(nsteps)
        
        RUNS = self.pos.shape[0]  # 当前漫步次数，在该方法内保持不变
        
        # 随机每次每步的移动维度和距离
        dim_indices = self.rng.integers(0, self.dim, size=(RUNS, nsteps))
        move_distances = np.random.choice((1, -1), size=(RUNS, nsteps))
        
        # 生成次数轴和步数轴的索引，使用数组索引对位移向量数组的两个轴进行全遍历，并对维度轴索引，在指定位置替换为移动距离
        walks = np.arange(RUNS)
        steps = np.arange(nsteps)
        walk_indices = np.repeat(walks, nsteps).reshape(RUNS, nsteps)
        step_indices = np.tile(steps, (RUNS, 1))
        
        displacement_vectors = np.zeros((RUNS, nsteps, self.dim))  # 初始化位移向量
        displacement_vectors[walk_indices, step_indices, dim_indices] = move_distances  # 位移向量
        displacement_vectors[:, 0:1] =  self.pos[:, -1:, :] + displacement_vectors[:, 0:1, :]
        # 累加位移向量，获得每次每步的位置
        pos_without_start = displacement_vectors.cumsum(axis=1)
        # 将每步位置插入在当前已有漫步之后
        self.pos = np.concatenate((self.pos, pos_without_start), axis=1)
    
    def append_runs(self,
                    runs : int | np.integer = 1) -> np.ndarray:
        """
        增加 n 个与当前漫步相同步数的随机漫步。

        参数：
            runs(int): 新增的漫步数量，必须为正整数，默认为 1
        """
        # 参数检测
        validate_int(runs)
        
        NSTEPS = self.pos.shape[1] - 1 # 当前漫步步数，在该方法内保持不变
        # 如果当前漫步停留在初始位置，则新增 n 个在起始位置的漫步。
        if NSTEPS == 0:
            self.pos = np.concatenate((self.pos, np.zeros((runs, NSTEPS, self.dim))), axis=0)
            return
        
        # 随机每次每步的移动维度和距离
        dim_indices = self.rng.integers(0, self.dim, size=(runs, NSTEPS))
        move_distances = np.random.choice((1, -1), size=(runs, NSTEPS))
        
        # 生成次数轴和步数轴的索引，使用数组索引对位移向量数组的两个轴进行全遍历，并对维度轴索引，在指定位置替换为移动距离
        walks = np.arange(runs)
        steps = np.arange(NSTEPS)
        walk_indices = np.repeat(walks, NSTEPS).reshape(runs, NSTEPS)
        step_indices = np.tile(steps, (runs, 1))
        
        displacement_vectors = np.zeros((runs, NSTEPS, self.dim))  # 初始化位移向量
        displacement_vectors[walk_indices, step_indices, dim_indices] = move_distances  # 位移向量
        # 累加位移向量，获得每次每步的位置
        pos_without_start = displacement_vectors.cumsum(axis=1)
        # 将每步位置插入在当前已有漫步之后
        start_pos = np.zeros((runs, 1, self.dim))
        pos_with_start = np.concatenate([start_pos, pos_without_start], axis=1)
        self.pos = np.concatenate((self.pos, pos_with_start), axis=0)


mywalk = RandomWalk(dim=4)
print(f'当前有{mywalk.pos.shape[0]}个{mywalk.pos.shape[1]}步{mywalk.pos.shape[2]}维随机漫步')
mywalk.append_steps()
print(f'增加了1步，当前有{mywalk.pos.shape[0]}个{mywalk.pos.shape[1]}步{mywalk.pos.shape[2]}维随机漫步')
mywalk.append_steps(nsteps=4)
print(f'增加了4步，当前有{mywalk.pos.shape[0]}个{mywalk.pos.shape[1]}步{mywalk.pos.shape[2]}维随机漫步')
mywalk.append_runs()
print(f'添加了1次漫步，当前有{mywalk.pos.shape[0]}个{mywalk.pos.shape[1]}步{mywalk.pos.shape[2]}维随机漫步')
mywalk.append_runs(4)
print(f'添加了4次漫步，当前有{mywalk.pos.shape[0]}个{mywalk.pos.shape[1]}步{mywalk.pos.shape[2]}维随机漫步')
mywalk.append_steps(2)
print(f'增加了2步，当前有{mywalk.pos.shape[0]}个{mywalk.pos.shape[1]}步{mywalk.pos.shape[2]}维随机漫步')
mywalk.append_runs(2)
print(mywalk.pos)
