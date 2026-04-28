// 游戏常量
export const TILE_SIZE = 40;
export const MAP_WIDTH = 13;
export const MAP_HEIGHT = 13;
export const CANVAS_WIDTH = MAP_WIDTH * TILE_SIZE;
export const CANVAS_HEIGHT = MAP_HEIGHT * TILE_SIZE;

// 方向常量
export const DIRECTIONS = {
    UP: 'up',
    DOWN: 'down',
    LEFT: 'left',
    RIGHT: 'right'
};

// 地图瓦片类型
export const TILE_TYPES = {
    EMPTY: 0,
    BRICK: 1,
    STEEL: 2,
    WATER: 3,
    GRASS: 4,
    BASE: 5
};

// 坦克类型
export const TANK_TYPES = {
    PLAYER: 'player',
    BASIC: 'basic',
    FAST: 'fast',
    HEAVY: 'heavy'
};

// 游戏状态
export const GAME_STATES = {
    IDLE: 'idle',
    PLAYING: 'playing',
    PAUSED: 'paused',
    GAME_OVER: 'game_over',
    LEVEL_COMPLETE: 'level_complete'
};

// 坦克属性配置
export const TANK_CONFIGS = {
    [TANK_TYPES.PLAYER]: {
        speed: 2,
        bulletSpeed: 5,
        bulletPower: 1,
        maxBullets: 1,
        color: '#4CAF50',
        score: 0
    },
    [TANK_TYPES.BASIC]: {
        speed: 1,
        bulletSpeed: 3,
        bulletPower: 1,
        maxBullets: 1,
        color: '#F44336',
        score: 100
    },
    [TANK_TYPES.FAST]: {
        speed: 3,
        bulletSpeed: 4,
        bulletPower: 1,
        maxBullets: 2,
        color: '#FF9800',
        score: 200
    },
    [TANK_TYPES.HEAVY]: {
        speed: 0.8,
        bulletSpeed: 3,
        bulletPower: 2,
        maxBullets: 1,
        color: '#9C27B0',
        score: 300
    }
};

// 地图数据
export const MAP_DATA = [
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 0, 0]
];
