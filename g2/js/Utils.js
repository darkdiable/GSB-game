import { DIRECTIONS, TILE_SIZE } from './Constants.js';

// 工具函数模块

/**
 * 方向到角度的转换
 * @param {string} direction - 方向常量
 * @returns {number} - 角度值（弧度）
 */
export function directionToAngle(direction) {
    switch (direction) {
        case DIRECTIONS.UP:
            return -Math.PI / 2;
        case DIRECTIONS.DOWN:
            return Math.PI / 2;
        case DIRECTIONS.LEFT:
            return Math.PI;
        case DIRECTIONS.RIGHT:
            return 0;
        default:
            return 0;
    }
}

/**
 * 方向到速度向量的转换
 * @param {string} direction - 方向常量
 * @param {number} speed - 速度大小
 * @returns {Object} - 包含x和y分量的速度向量
 */
export function directionToVelocity(direction, speed) {
    switch (direction) {
        case DIRECTIONS.UP:
            return { x: 0, y: -speed };
        case DIRECTIONS.DOWN:
            return { x: 0, y: speed };
        case DIRECTIONS.LEFT:
            return { x: -speed, y: 0 };
        case DIRECTIONS.RIGHT:
            return { x: speed, y: 0 };
        default:
            return { x: 0, y: 0 };
    }
}

/**
 * 矩形碰撞检测
 * @param {Object} rect1 - 第一个矩形 {x, y, width, height}
 * @param {Object} rect2 - 第二个矩形 {x, y, width, height}
 * @returns {boolean} - 是否碰撞
 */
export function rectCollision(rect1, rect2) {
    return rect1.x < rect2.x + rect2.width &&
           rect1.x + rect1.width > rect2.x &&
           rect1.y < rect2.y + rect2.height &&
           rect1.y + rect1.height > rect2.y;
}

/**
 * 将像素坐标转换为地图网格坐标
 * @param {number} x - 像素x坐标
 * @param {number} y - 像素y坐标
 * @returns {Object} - 包含gridX和gridY的坐标对象
 */
export function pixelToGrid(x, y) {
    return {
        gridX: Math.floor(x / TILE_SIZE),
        gridY: Math.floor(y / TILE_SIZE)
    };
}

/**
 * 将地图网格坐标转换为像素坐标
 * @param {number} gridX - 网格x坐标
 * @param {number} gridY - 网格y坐标
 * @returns {Object} - 包含x和y的像素坐标对象
 */
export function gridToPixel(gridX, gridY) {
    return {
        x: gridX * TILE_SIZE,
        y: gridY * TILE_SIZE
    };
}

/**
 * 生成随机整数
 * @param {number} min - 最小值（包含）
 * @param {number} max - 最大值（包含）
 * @returns {number} - 随机整数
 */
export function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * 从数组中随机选择一个元素
 * @param {Array} array - 输入数组
 * @returns {*} - 随机选择的元素
 */
export function randomChoice(array) {
    if (array.length === 0) return null;
    return array[randomInt(0, array.length - 1)];
}

/**
 * 计算两点之间的距离
 * @param {number} x1 - 第一个点的x坐标
 * @param {number} y1 - 第一个点的y坐标
 * @param {number} x2 - 第二个点的x坐标
 * @param {number} y2 - 第二个点的y坐标
 * @returns {number} - 两点之间的距离
 */
export function distance(x1, y1, x2, y2) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    return Math.sqrt(dx * dx + dy * dy);
}

/**
 * 检查一个点是否在矩形内
 * @param {number} px - 点的x坐标
 * @param {number} py - 点的y坐标
 * @param {Object} rect - 矩形 {x, y, width, height}
 * @returns {boolean} - 点是否在矩形内
 */
export function pointInRect(px, py, rect) {
    return px >= rect.x && px <= rect.x + rect.width &&
           py >= rect.y && py <= rect.y + rect.height;
}

/**
 * 限制一个值在指定范围内
 * @param {number} value - 输入值
 * @param {number} min - 最小值
 * @param {number} max - 最大值
 * @returns {number} - 限制后的值
 */
export function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
}
