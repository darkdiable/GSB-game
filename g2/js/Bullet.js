import { DIRECTIONS, TANK_TYPES, TANK_CONFIGS } from './Constants.js';
import { directionToVelocity } from './Utils.js';

class Bullet {
    constructor(x, y, direction, owner, config = {}) {
        this.x = x;
        this.y = y;
        this.direction = direction;
        this.owner = owner;
        
        // 子弹尺寸
        this.width = config.width || 8;
        this.height = config.height || 8;
        
        // 子弹属性
        this.speed = config.speed || 5;
        this.power = config.power || 1;
        this.isEnemy = config.isEnemy || false;
        
        // 状态
        this.active = true;
        this.velocity = directionToVelocity(direction, this.speed);
    }
    
    /**
     * 更新子弹位置
     */
    update() {
        if (!this.active) return;
        
        this.x += this.velocity.x;
        this.y += this.velocity.y;
    }
    
    /**
     * 销毁子弹
     */
    destroy() {
        this.active = false;
    }
    
    /**
     * 渲染子弹
     * @param {CanvasRenderingContext2D} ctx - 画布上下文
     */
    render(ctx) {
        if (!this.active) return;
        
        // 根据方向调整子弹位置，使其居中
        let renderX = this.x;
        let renderY = this.y;
        let renderWidth = this.width;
        let renderHeight = this.height;
        
        // 根据方向调整子弹形状
        switch (this.direction) {
            case DIRECTIONS.UP:
            case DIRECTIONS.DOWN:
                // 垂直方向：子弹更细长
                renderWidth = 4;
                renderHeight = 8;
                renderX = this.x + (this.width - renderWidth) / 2;
                break;
            case DIRECTIONS.LEFT:
            case DIRECTIONS.RIGHT:
                // 水平方向：子弹更细长
                renderWidth = 8;
                renderHeight = 4;
                renderY = this.y + (this.height - renderHeight) / 2;
                break;
        }
        
        // 子弹颜色：玩家子弹为黄色，敌方子弹为红色
        ctx.fillStyle = this.isEnemy ? '#FF0000' : '#FFFF00';
        ctx.fillRect(renderX, renderY, renderWidth, renderHeight);
        
        // 子弹发光效果
        ctx.shadowColor = this.isEnemy ? '#FF0000' : '#FFFF00';
        ctx.shadowBlur = 5;
        ctx.fillRect(renderX, renderY, renderWidth, renderHeight);
        ctx.shadowBlur = 0;
    }
    
    /**
     * 从坦克创建子弹
     * @param {Object} tank - 坦克对象
     * @returns {Bullet} - 新创建的子弹
     */
    static createFromTank(tank) {
        const config = TANK_CONFIGS[tank.type];
        const isEnemy = tank.type !== TANK_TYPES.PLAYER;
        
        // 计算子弹初始位置（坦克炮口位置）
        let bulletX = tank.x + tank.width / 2 - 4;
        let bulletY = tank.y + tank.height / 2 - 4;
        
        // 根据方向调整子弹位置
        switch (tank.direction) {
            case DIRECTIONS.UP:
                bulletY = tank.y - 8;
                break;
            case DIRECTIONS.DOWN:
                bulletY = tank.y + tank.height;
                break;
            case DIRECTIONS.LEFT:
                bulletX = tank.x - 8;
                break;
            case DIRECTIONS.RIGHT:
                bulletX = tank.x + tank.width;
                break;
        }
        
        return new Bullet(
            bulletX,
            bulletY,
            tank.direction,
            tank,
            {
                speed: config.bulletSpeed,
                power: config.bulletPower,
                isEnemy: isEnemy
            }
        );
    }
}

export default Bullet;
