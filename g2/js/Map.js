import { TILE_SIZE, MAP_WIDTH, MAP_HEIGHT, TILE_TYPES, MAP_DATA } from './Constants.js';
import { gridToPixel } from './Utils.js';

class Map {
    constructor() {
        this.tileSize = TILE_SIZE;
        this.width = MAP_WIDTH;
        this.height = MAP_HEIGHT;
        this.tiles = [];
        this.baseDestroyed = false;
        
        this.init();
    }
    
    /**
     * 初始化地图
     */
    init() {
        // 深拷贝地图数据
        this.tiles = JSON.parse(JSON.stringify(MAP_DATA));
        this.baseDestroyed = false;
    }
    
    /**
     * 重置地图到初始状态
     */
    reset() {
        this.init();
    }
    
    /**
     * 获取指定位置的瓦片类型
     * @param {number} gridX - 网格X坐标
     * @param {number} gridY - 网格Y坐标
     * @returns {number} - 瓦片类型
     */
    getTile(gridX, gridY) {
        if (gridX < 0 || gridX >= this.width || gridY < 0 || gridY >= this.height) {
            return TILE_TYPES.STEEL; // 边界视为钢铁墙
        }
        return this.tiles[gridY][gridX];
    }
    
    /**
     * 设置指定位置的瓦片类型
     * @param {number} gridX - 网格X坐标
     * @param {number} gridY - 网格Y坐标
     * @param {number} type - 瓦片类型
     */
    setTile(gridX, gridY, type) {
        if (gridX < 0 || gridX >= this.width || gridY < 0 || gridY >= this.height) {
            return;
        }
        
        // 检查是否是基地
        const oldType = this.tiles[gridY][gridX];
        if (oldType === TILE_TYPES.BASE && type === TILE_TYPES.EMPTY) {
            this.baseDestroyed = true;
        }
        
        this.tiles[gridY][gridX] = type;
    }
    
    /**
     * 检查瓦片是否可以通过（坦克可以移动）
     * @param {number} gridX - 网格X坐标
     * @param {number} gridY - 网格Y坐标
     * @returns {boolean} - 是否可以通过
     */
    isWalkable(gridX, gridY) {
        const tile = this.getTile(gridX, gridY);
        return tile === TILE_TYPES.EMPTY || tile === TILE_TYPES.GRASS;
    }
    
    /**
     * 检查瓦片是否可以被子弹穿透
     * @param {number} gridX - 网格X坐标
     * @param {number} gridY - 网格Y坐标
     * @returns {boolean} - 是否可以穿透
     */
    isPenetrable(gridX, gridY) {
        const tile = this.getTile(gridX, gridY);
        return tile === TILE_TYPES.EMPTY || tile === TILE_TYPES.GRASS;
    }
    
    /**
     * 检查瓦片是否可以被摧毁
     * @param {number} gridX - 网格X坐标
     * @param {number} gridY - 网格Y坐标
     * @returns {boolean} - 是否可以被摧毁
     */
    isDestructible(gridX, gridY) {
        const tile = this.getTile(gridX, gridY);
        return tile === TILE_TYPES.BRICK || tile === TILE_TYPES.BASE;
    }
    
    /**
     * 检查基地是否被摧毁
     * @returns {boolean} - 基地是否被摧毁
     */
    isBaseDestroyed() {
        return this.baseDestroyed;
    }
    
    /**
     * 摧毁指定位置的瓦片
     * @param {number} gridX - 网格X坐标
     * @param {number} gridY - 网格Y坐标
     * @param {number} power - 子弹威力
     * @returns {boolean} - 是否成功摧毁
     */
    destroyTile(gridX, gridY, power = 1) {
        const tile = this.getTile(gridX, gridY);
        
        if (tile === TILE_TYPES.BRICK) {
            this.setTile(gridX, gridY, TILE_TYPES.EMPTY);
            return true;
        }
        
        if (tile === TILE_TYPES.BASE) {
            this.setTile(gridX, gridY, TILE_TYPES.EMPTY);
            return true;
        }
        
        // 钢铁墙需要更大的威力才能摧毁（这里简化处理，钢铁墙不可摧毁）
        if (tile === TILE_TYPES.STEEL) {
            return false;
        }
        
        return false;
    }
    
    /**
     * 渲染地图
     * @param {CanvasRenderingContext2D} ctx - 画布上下文
     */
    render(ctx) {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const tile = this.tiles[y][x];
                const pos = gridToPixel(x, y);
                
                this.renderTile(ctx, pos.x, pos.y, tile);
            }
        }
    }
    
    /**
     * 渲染单个瓦片
     * @param {CanvasRenderingContext2D} ctx - 画布上下文
     * @param {number} x - 像素X坐标
     * @param {number} y - 像素Y坐标
     * @param {number} type - 瓦片类型
     */
    renderTile(ctx, x, y, type) {
        const size = this.tileSize;
        
        switch (type) {
            case TILE_TYPES.BRICK:
                // 砖墙 - 橙红色砖块纹理
                ctx.fillStyle = '#CD853F';
                ctx.fillRect(x, y, size, size);
                
                // 砖块纹理
                ctx.strokeStyle = '#8B4513';
                ctx.lineWidth = 1;
                
                // 水平砖块线
                ctx.beginPath();
                ctx.moveTo(x, y + size/2);
                ctx.lineTo(x + size, y + size/2);
                ctx.stroke();
                
                // 垂直砖块线（交错排列）
                ctx.beginPath();
                ctx.moveTo(x + size/2, y);
                ctx.lineTo(x + size/2, y + size/2);
                ctx.stroke();
                
                ctx.beginPath();
                ctx.moveTo(x + size/4, y + size/2);
                ctx.lineTo(x + size/4, y + size);
                ctx.stroke();
                
                ctx.beginPath();
                ctx.moveTo(x + 3*size/4, y + size/2);
                ctx.lineTo(x + 3*size/4, y + size);
                ctx.stroke();
                break;
                
            case TILE_TYPES.STEEL:
                // 钢铁墙 - 灰色金属纹理
                ctx.fillStyle = '#808080';
                ctx.fillRect(x, y, size, size);
                
                // 金属光泽效果
                ctx.fillStyle = '#A9A9A9';
                ctx.fillRect(x + 2, y + 2, size/2 - 4, size/2 - 4);
                ctx.fillRect(x + size/2 + 2, y + size/2 + 2, size/2 - 4, size/2 - 4);
                
                // 边框
                ctx.strokeStyle = '#696969';
                ctx.lineWidth = 2;
                ctx.strokeRect(x + 1, y + 1, size - 2, size - 2);
                break;
                
            case TILE_TYPES.WATER:
                // 河流 - 蓝色波浪纹理
                ctx.fillStyle = '#1E90FF';
                ctx.fillRect(x, y, size, size);
                
                // 波浪效果
                ctx.strokeStyle = '#00BFFF';
                ctx.lineWidth = 2;
                ctx.beginPath();
                for (let i = 0; i < size; i += 10) {
                    ctx.moveTo(x + i, y + size/3 + Math.sin(i * 0.2) * 5);
                    ctx.lineTo(x + i + 10, y + size/3 + Math.sin((i + 10) * 0.2) * 5);
                }
                ctx.stroke();
                
                ctx.beginPath();
                for (let i = 0; i < size; i += 10) {
                    ctx.moveTo(x + i, y + 2*size/3 + Math.sin(i * 0.2 + 1) * 5);
                    ctx.lineTo(x + i + 10, y + 2*size/3 + Math.sin((i + 10) * 0.2 + 1) * 5);
                }
                ctx.stroke();
                break;
                
            case TILE_TYPES.GRASS:
                // 草地 - 绿色，坦克可以隐藏在后面
                ctx.fillStyle = '#228B22';
                ctx.fillRect(x, y, size, size);
                
                // 草地纹理
                ctx.strokeStyle = '#32CD32';
                ctx.lineWidth = 1;
                for (let i = 0; i < 5; i++) {
                    const gx = x + Math.random() * size;
                    const gy = y + Math.random() * size;
                    ctx.beginPath();
                    ctx.moveTo(gx, gy + 8);
                    ctx.lineTo(gx, gy);
                    ctx.stroke();
                }
                break;
                
            case TILE_TYPES.BASE:
                // 基地 - 老鹰图标
                ctx.fillStyle = '#DAA520';
                ctx.fillRect(x, y, size, size);
                
                // 老鹰简化图标
                ctx.fillStyle = '#8B4513';
                ctx.beginPath();
                ctx.moveTo(x + size/2, y + 5);
                ctx.lineTo(x + size - 5, y + size/2);
                ctx.lineTo(x + size/2, y + size - 5);
                ctx.lineTo(x + 5, y + size/2);
                ctx.closePath();
                ctx.fill();
                
                // 边框
                ctx.strokeStyle = '#FFD700';
                ctx.lineWidth = 2;
                ctx.strokeRect(x + 2, y + 2, size - 4, size - 4);
                break;
                
            case TILE_TYPES.EMPTY:
            default:
                // 空地 - 黑色背景
                ctx.fillStyle = '#000000';
                ctx.fillRect(x, y, size, size);
                break;
        }
    }
}

export default Map;
