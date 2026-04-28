import { TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, TILE_TYPES } from './Constants.js';
import { rectCollision, pixelToGrid } from './Utils.js';

class Collision {
    constructor(map) {
        this.map = map;
    }
    
    /**
     * 检查矩形是否与地图边界碰撞
     * @param {Object} rect - 矩形 {x, y, width, height}
     * @returns {boolean} - 是否碰撞
     */
    checkBoundaryCollision(rect) {
        const canvasWidth = MAP_WIDTH * TILE_SIZE;
        const canvasHeight = MAP_HEIGHT * TILE_SIZE;
        
        return rect.x < 0 || 
               rect.x + rect.width > canvasWidth || 
               rect.y < 0 || 
               rect.y + rect.height > canvasHeight;
    }
    
    /**
     * 检查矩形是否与地图瓦片碰撞
     * @param {Object} rect - 矩形 {x, y, width, height}
     * @param {boolean} checkWalkable - 是否检查可通过性（坦克移动用true，子弹用false）
     * @returns {boolean} - 是否碰撞
     */
    checkMapCollision(rect, checkWalkable = true) {
        // 获取矩形四个角的网格坐标
        const corners = [
            { x: rect.x, y: rect.y },
            { x: rect.x + rect.width - 1, y: rect.y },
            { x: rect.x, y: rect.y + rect.height - 1 },
            { x: rect.x + rect.width - 1, y: rect.y + rect.height - 1 }
        ];
        
        // 检查每个角所在的瓦片
        for (const corner of corners) {
            const { gridX, gridY } = pixelToGrid(corner.x, corner.y);
            
            if (checkWalkable) {
                // 坦克移动时检查是否可通过
                if (!this.map.isWalkable(gridX, gridY)) {
                    return true;
                }
            } else {
                // 子弹移动时检查是否可穿透
                if (!this.map.isPenetrable(gridX, gridY)) {
                    return true;
                }
            }
        }
        
        // 额外检查矩形中心点（避免某些边界情况）
        const centerX = rect.x + rect.width / 2;
        const centerY = rect.y + rect.height / 2;
        const { gridX, gridY } = pixelToGrid(centerX, centerY);
        
        if (checkWalkable) {
            if (!this.map.isWalkable(gridX, gridY)) {
                return true;
            }
        } else {
            if (!this.map.isPenetrable(gridX, gridY)) {
                return true;
            }
        }
        
        return false;
    }
    
    /**
     * 检查坦克是否可以移动到指定位置
     * @param {Object} tank - 坦克对象
     * @param {number} newX - 新的X坐标
     * @param {number} newY - 新的Y坐标
     * @param {Array} otherTanks - 其他坦克数组
     * @returns {boolean} - 是否可以移动
     */
    canTankMove(tank, newX, newY, otherTanks = []) {
        const rect = {
            x: newX,
            y: newY,
            width: tank.width,
            height: tank.height
        };
        
        // 检查边界碰撞
        if (this.checkBoundaryCollision(rect)) {
            return false;
        }
        
        // 检查地图瓦片碰撞
        if (this.checkMapCollision(rect, true)) {
            return false;
        }
        
        // 检查与其他坦克的碰撞
        for (const otherTank of otherTanks) {
            if (otherTank !== tank && otherTank.active) {
                const otherRect = {
                    x: otherTank.x,
                    y: otherTank.y,
                    width: otherTank.width,
                    height: otherTank.height
                };
                
                if (rectCollision(rect, otherRect)) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    /**
     * 检查子弹是否与地图碰撞，并处理碰撞
     * @param {Object} bullet - 子弹对象
     * @returns {Object} - 碰撞结果 { collided: boolean, destroyedTiles: Array }
     */
    checkBulletMapCollision(bullet) {
        const rect = {
            x: bullet.x,
            y: bullet.y,
            width: bullet.width,
            height: bullet.height
        };
        
        const result = {
            collided: false,
            destroyedTiles: []
        };
        
        // 检查边界碰撞
        if (this.checkBoundaryCollision(rect)) {
            result.collided = true;
            return result;
        }
        
        // 检查地图瓦片碰撞
        // 获取子弹覆盖的所有瓦片
        const corners = [
            { x: rect.x, y: rect.y },
            { x: rect.x + rect.width - 1, y: rect.y },
            { x: rect.x, y: rect.y + rect.height - 1 },
            { x: rect.x + rect.width - 1, y: rect.y + rect.height - 1 }
        ];
        
        const checkedTiles = new Set();
        
        for (const corner of corners) {
            const { gridX, gridY } = pixelToGrid(corner.x, corner.y);
            const tileKey = `${gridX},${gridY}`;
            
            if (checkedTiles.has(tileKey)) continue;
            checkedTiles.add(tileKey);
            
            const tile = this.map.getTile(gridX, gridY);
            
            if (tile === TILE_TYPES.EMPTY || tile === TILE_TYPES.GRASS) {
                continue;
            }
            
            // 碰到了不可穿透的瓦片
            result.collided = true;
            
            // 尝试摧毁瓦片
            if (this.map.isDestructible(gridX, gridY)) {
                if (this.map.destroyTile(gridX, gridY, bullet.power)) {
                    result.destroyedTiles.push({ gridX, gridY, tile });
                }
            }
        }
        
        return result;
    }
    
    /**
     * 检查子弹是否与坦克碰撞
     * @param {Object} bullet - 子弹对象
     * @param {Array} tanks - 坦克数组
     * @returns {Object} - 碰撞结果 { collided: boolean, hitTank: Object|null }
     */
    checkBulletTankCollision(bullet, tanks) {
        const bulletRect = {
            x: bullet.x,
            y: bullet.y,
            width: bullet.width,
            height: bullet.height
        };
        
        for (const tank of tanks) {
            if (!tank.active) continue;
            
            // 子弹不能击中发射它的坦克
            if (tank === bullet.owner) continue;
            
            const tankRect = {
                x: tank.x,
                y: tank.y,
                width: tank.width,
                height: tank.height
            };
            
            if (rectCollision(bulletRect, tankRect)) {
                return {
                    collided: true,
                    hitTank: tank
                };
            }
        }
        
        return {
            collided: false,
            hitTank: null
        };
    }
    
    /**
     * 检查两个子弹是否碰撞
     * @param {Object} bullet1 - 第一个子弹
     * @param {Object} bullet2 - 第二个子弹
     * @returns {boolean} - 是否碰撞
     */
    checkBulletBulletCollision(bullet1, bullet2) {
        if (!bullet1.active || !bullet2.active) return false;
        if (bullet1 === bullet2) return false;
        
        const rect1 = {
            x: bullet1.x,
            y: bullet1.y,
            width: bullet1.width,
            height: bullet1.height
        };
        
        const rect2 = {
            x: bullet2.x,
            y: bullet2.y,
            width: bullet2.width,
            height: bullet2.height
        };
        
        return rectCollision(rect1, rect2);
    }
    
    /**
     * 检查基地是否被摧毁
     * @returns {boolean} - 基地是否被摧毁
     */
    isBaseDestroyed() {
        return this.map.isBaseDestroyed();
    }
}

export default Collision;
