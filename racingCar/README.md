# 赛车游戏 - Racing Car

一款使用Python和Pygame开发的2D赛车游戏。

## 游戏特点

- 自下而上滚动的赛车视角
- 三条车道的公路设计
- 随机切换的场景：海滨、城镇、沙漠
- 多种车辆类型：跑车、SUV、货车、障碍物
- 碰撞5次游戏结束
- 分数和速度显示
- 生命值（心形图标）显示

## 控制方式

- **W** - 加速
- **S** - 减速（长按可刹停）
- **A** - 向左移动
- **D** - 向右移动
- **R** - 游戏结束后重新开始

## 安装和运行

### 安装依赖

```bash
pip install pygame
```

或者：

```bash
pip3 install -r requirements.txt
```

### 运行游戏

```bash
python main.py
```

或者：

```bash
python3 main.py
```

## 项目结构

```
racingCar/
├── config.py       # 游戏配置和常量
├── player.py       # 玩家赛车类
├── vehicles.py     # 其他车辆和障碍物类
├── scenery.py      # 场景生成器
├── ui.py           # UI界面管理
├── game.py         # 游戏主循环
├── main.py         # 程序入口
└── requirements.txt # 依赖包
```

## 游戏玩法

1. 启动游戏后，按任意键开始
2. 使用WASD控制赛车
3. 躲避公路上的其他车辆和障碍物
4. 每成功躲避车辆可获得分数
5. 碰撞5次后游戏结束
6. 按R键可重新开始游戏

祝你游戏愉快！
