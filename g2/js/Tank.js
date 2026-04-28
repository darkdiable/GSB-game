import { DIRECTIONS, TANK_TYPES, TANK_CONFIGS } from './Constants.js';
import { directionToAngle, randomChoice, randomInt, distance } from './Utils.js';
import Bullet from './Bullet.js';

class Tank {
    constructor(x, y, direction, type, config = {}) {
        this.x = x;
        this.y = y;
        this.direction = direction;
        this.type = type;
        
        // 坦克尺寸
        this.width = config.width || 36;
        this.height = config.height || 36;
        
        // 从配置获取属性
        const tankConfig = TANK_CONFIGS[type] || TANK_CONFIGS[TANK_TYPES.BASIC];
        this.speed = config.speed || tankConfig.speed;
        this.bulletSpeed = config.bulletSpeed || tankConfig.bulletSpeed;
        this.bulletPower = config.bulletPower || tankConfig.bulletPower;
        this.maxBullets = config.maxBullets || tankConfig.maxBullets;
        this.color = config.color || tankConfig.color;
        this.score = config.score || tankConfig.score;
        
        // 状态
        this.active = true;
        this.isMoving = false;
        this.bullets = [];
        
        // 射击冷却
        this.shootCooldown = 0;
        this.shootCooldownTime = 500; // 毫秒
    }
    
    /**
     * 更新坦克状态
     * @param {number} deltaTime - 时间增量（毫秒）
     */
    update(deltaTime) {
        if (!this.active) return;
        
        // 更新射击冷却
        if (this.shootCooldown > 0) {
            this.shootCooldown -= deltaTime;
        }
    }
    
    /**
     * 移动坦克
     * @param {string} direction - 移动方向
     * @param {Collision} collision - 碰撞检测对象
     * @param {Array} otherTanks - 其他坦克数组
     * @returns {boolean} - 是否成功移动
     */
    move(direction, collision, otherTanks = []) {
        if (!this.active) return false;
        
        // 改变方向
        this.direction = direction;
        this.isMoving = true;
        
        // 计算新位置
        let newX = this.x;
        let newY = this.y;
        
        switch (direction) {
            case DIRECTIONS.UP:
                newY -= this.speed;
                break;
            case DIRECTIONS.DOWN:
                newY += this.speed;
                break;
            case DIRECTIONS.LEFT:
                newX -= this.speed;
                break;
            case DIRECTIONS.RIGHT:
                newX += this.speed;
                break;
        }
        
        // 检查碰撞
        if (collision && collision.canTankMove(this, newX, newY, otherTanks)) {
            this.x = newX;
            this.y = newY;
            return true;
        }
        
        return false;
    }
    
    /**
     * 停止移动
     */
    stop() {
        this.isMoving = false;
    }
    
    /**
     * 射击
     * @returns {Bullet|null} - 新创建的子弹，如果无法射击则返回null
     */
    shoot() {
        if (!this.active) return null;
        if (this.shootCooldown > 0) return null;
        
        // 检查当前子弹数量
        const activeBullets = this.bullets.filter(b => b.active);
        if (activeBullets.length >= this.maxBullets) return null;
        
        // 创建子弹
        const bullet = Bullet.createFromTank(this);
        
        // 添加到子弹列表
        this.bullets.push(bullet);
        
        // 设置射击冷却
        this.shootCooldown = this.shootCooldownTime;
        
        return bullet;
    }
    
    /**
     * 销毁坦克
     */
    destroy() {
        this.active = false;
        this.isMoving = false;
    }
    
    /**
     * 渲染坦克
     * @param {CanvasRenderingContext2D} ctx - 画布上下文
     */
    render(ctx) {
        if (!this.active) return;
        
        ctx.save();
        
        // 移动到坦克中心
        const centerX = this.x + this.width / 2;
        const centerY = this.y + this.height / 2;
        
        ctx.translate(centerX, centerY);
        ctx.rotate(directionToAngle(this.direction));
        
        // 绘制坦克主体
        this.drawTankBody(ctx);
        
        // 绘制坦克炮管
        this.drawTankGun(ctx);
        
        ctx.restore();
    }
    
    /**
     * 绘制坦克主体
     * @param {CanvasRenderingContext2D} ctx - 画布上下文
     */
    drawTankBody(ctx) {
        const halfWidth = this.width / 2;
        const halfHeight = this.height / 2;
        
        // 坦克主体
        ctx.fillStyle = this.color;
        ctx.fillRect(-halfWidth + 4, -halfHeight + 4, this.width - 8, this.height - 8);
        
        // 坦克履带
        ctx.fillStyle = '#333';
        // 左履带
        ctx.fillRect(-halfWidth, -halfHeight, 6, this.height);
        // 右履带
        ctx.fillRect(halfWidth - 6, -halfHeight, 6, this.height);
        
        // 履带纹理
        ctx.strokeStyle = '#555';
        ctx.lineWidth = 1;
        for (let i = -halfHeight + 4; i < halfHeight - 4; i += 8) {
            ctx.beginPath();
            ctx.moveTo(-halfWidth, i);
            ctx.lineTo(-halfWidth + 6, i);
            ctx.stroke();
            
            ctx.beginPath();
            ctx.moveTo(halfWidth - 6, i);
            ctx.lineTo(halfWidth, i);
            ctx.stroke();
        }
        
        // 坦克炮塔
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(0, 0, 10, 0, Math.PI * 2);
        ctx.fill();
        
        // 炮塔高光
        ctx.fillStyle = this.lightenColor(this.color, 30);
        ctx.beginPath();
        ctx.arc(-3, -3, 4, 0, Math.PI * 2);
        ctx.fill();
    }
    
    /**
     * 绘制坦克炮管
     * @param {CanvasRenderingContext2D} ctx - 画布上下文
     */
    drawTankGun(ctx) {
        const halfWidth = this.width / 2;
        
        // 炮管
        ctx.fillStyle = '#333';
        ctx.fillRect(0, -3, halfWidth + 4, 6);
        
        // 炮口
        ctx.fillStyle = '#555';
        ctx.fillRect(halfWidth + 4, -4, 4, 8);
    }
    
    /**
     * 加深颜色
     * @param {string} color - 颜色值
     * @param {number} amount - 加深程度
     * @returns {string} - 加深后的颜色
     */
    darkenColor(color, amount) {
        const num = parseInt(color.replace('#', ''), 16);
        const r = Math.max(0, (num >> 16) - amount);
        const g = Math.max(0, ((num >> 8) & 0x00FF) - amount);
        const b = Math.max(0, (num & 0x0000FF) - amount);
        return '#' + (0x1000000 + r * 0x10000 + g * 0x100 + b).toString(16).slice(1);
    }
    
    /**
     * 变亮颜色
     * @param {string} color - 颜色值
     * @param {number} amount - 变亮程度
     * @returns {string} - 变亮后的颜色
     */
    lightenColor(color, amount) {
        const num = parseInt(color.replace('#', ''), 16);
        const r = Math.min(255, (num >> 16) + amount);
        const g = Math.min(255, ((num >> 8) & 0x00FF) + amount);
        const b = Math.min(255, (num & 0x0000FF) + amount);
        return '#' + (0x1000000 + r * 0x10000 + g * 0x100 + b).toString(16).slice(1);
    }
}

class PlayerTank extends Tank {
    constructor(x, y, direction = DIRECTIONS.UP) {
        super(x, y, direction, TANK_TYPES.PLAYER);
        
        // 键盘状态
        this.keys = {
            up: false,
            down: false,
            left: false,
            right: false,
            shoot: false
        };
    }
    
    /**
     * 处理键盘按下事件
     * @param {string} key - 按键名称
     */
    handleKeyDown(key) {
        switch (key) {
            case 'ArrowUp':
            case 'w':
            case 'W':
                this.keys.up = true;
                break;
            case 'ArrowDown':
            case 's':
            case 'S':
                this.keys.down = true;
                break;
            case 'ArrowLeft':
            case 'a':
            case 'A':
                this.keys.left = true;
                break;
            case 'ArrowRight':
            case 'd':
            case 'D':
                this.keys.right = true;
                break;
            case ' ':
            case 'Enter':
                this.keys.shoot = true;
                break;
        }
    }
    
    /**
     * 处理键盘松开事件
     * @param {string} key - 按键名称
     */
    handleKeyUp(key) {
        switch (key) {
            case 'ArrowUp':
            case 'w':
            case 'W':
                this.keys.up = false;
                break;
            case 'ArrowDown':
            case 's':
            case 'S':
                this.keys.down = false;
                break;
            case 'ArrowLeft':
            case 'a':
            case 'A':
                this.keys.left = false;
                break;
            case 'ArrowRight':
            case 'd':
            case 'D':
                this.keys.right = false;
                break;
            case ' ':
            case 'Enter':
                this.keys.shoot = false;
                break;
        }
    }
    
    /**
     * 更新玩家坦克状态
     * @param {number} deltaTime - 时间增量
     * @param {Collision} collision - 碰撞检测对象
     * @param {Array} otherTanks - 其他坦克数组
     * @returns {Bullet|null} - 新创建的子弹
     */
    updatePlayer(deltaTime, collision, otherTanks) {
        if (!this.active) return null;
        
        // 调用父类更新
        this.update(deltaTime);
        
        let moved = false;
        
        // 处理移动
        if (this.keys.up) {
            this.move(DIRECTIONS.UP, collision, otherTanks);
            moved = true;
        } else if (this.keys.down) {
            this.move(DIRECTIONS.DOWN, collision, otherTanks);
            moved = true;
        } else if (this.keys.left) {
            this.move(DIRECTIONS.LEFT, collision, otherTanks);
            moved = true;
        } else if (this.keys.right) {
            this.move(DIRECTIONS.RIGHT, collision, otherTanks);
            moved = true;
        }
        
        if (!moved) {
            this.stop();
        }
        
        // 处理射击
        if (this.keys.shoot) {
            return this.shoot();
        }
        
        return null;
    }
}

class EnemyTank extends Tank {
    constructor(x, y, direction, type) {
        super(x, y, direction, type);
        
        // AI状态
        this.aiState = 'patrol'; // patrol, chase, shoot
        this.patrolDirection = direction;
        this.patrolTimer = 0;
        this.patrolInterval = randomInt(2000, 5000); // 2-5秒
        
        // 射击AI
        this.shootTimer = 0;
        this.shootInterval = randomInt(1000, 3000); // 1-3秒
        
        // 追逐状态
        this.chaseTarget = null;
    }
    
    /**
     * 更新敌方坦克AI
     * @param {number} deltaTime - 时间增量
     * @param {Collision} collision - 碰撞检测对象
     * @param {Array} otherTanks - 其他坦克数组
     * @param {Tank} playerTank - 玩家坦克
     * @returns {Bullet|null} - 新创建的子弹
     */
    updateAI(deltaTime, collision, otherTanks, playerTank) {
        if (!this.active) return null;
        
        // 调用父类更新
        this.update(deltaTime);
        
        let newBullet = null;
        
        // 更新计时器
        this.patrolTimer += deltaTime;
        this.shootTimer += deltaTime;
        
        // 检查玩家是否在视野内
        const playerInSight = this.isPlayerInSight(playerTank);
        
        if (playerInSight) {
            // 玩家在视野内，进入追逐/射击状态
            this.aiState = 'chase';
            
            // 尝试射击
            if (this.shootTimer >= this.shootInterval) {
                newBullet = this.shoot();
                if (newBullet) {
                    this.shootTimer = 0;
                    this.shootInterval = randomInt(1000, 3000);
                }
            }
            
            // 朝向玩家
            const directionToPlayer = this.getDirectionToPlayer(playerTank);
            if (directionToPlayer && directionToPlayer !== this.direction) {
                this.direction = directionToPlayer;
            }
        } else {
            // 玩家不在视野内，巡逻
            this.aiState = 'patrol';
            
            // 定期改变巡逻方向
            if (this.patrolTimer >= this.patrolInterval) {
                this.changePatrolDirection();
                this.patrolTimer = 0;
                this.patrolInterval = randomInt(2000, 5000);
            }
            
            // 尝试移动
            const moved = this.move(this.patrolDirection, collision, otherTanks);
            
            // 如果无法移动，改变方向
            if (!moved) {
                this.changePatrolDirection();
            }
            
            // 随机射击
            if (this.shootTimer >= this.shootInterval) {
                newBullet = this.shoot();
                if (newBullet) {
                    this.shootTimer = 0;
                    this.shootInterval = randomInt(1000, 3000);
                }
            }
        }
        
        return newBullet;
    }
    
    /**
     * 检查玩家是否在视野内
     * @param {Tank} playerTank - 玩家坦克
     * @returns {boolean} - 是否在视野内
     */
    isPlayerInSight(playerTank) {
        if (!playerTank || !playerTank.active) return false;
        
        // 简单的视野检测：检查是否在同一行或同一列，并且在一定距离内
        const dx = Math.abs(this.x - playerTank.x);
        const dy = Math.abs(this.y - playerTank.y);
        
        // 视野范围（像素）
        const sightRange = 200;
        
        // 检查是否在同一行或同一列，并且在视野范围内
        if ((dx < this.width && dy < sightRange) || 
            (dy < this.height && dx < sightRange)) {
            return true;
        }
        
        return false;
    }
    
    /**
     * 获取朝向玩家的方向
     * @param {Tank} playerTank - 玩家坦克
     * @returns {string|null} - 方向，如果不在同一行/列则返回null
     */
    getDirectionToPlayer(playerTank) {
        if (!playerTank || !playerTank.active) return null;
        
        const dx = playerTank.x - this.x;
        const dy = playerTank.y - this.y;
        
        // 检查是否在同一行或同一列
        if (Math.abs(dx) < this.width) {
            // 同一列
            return dy > 0 ? DIRECTIONS.DOWN : DIRECTIONS.UP;
        } else if (Math.abs(dy) < this.height) {
            // 同一行
            return dx > 0 ? DIRECTIONS.RIGHT : DIRECTIONS.LEFT;
        }
        
        return null;
    }
    
    /**
     * 改变巡逻方向
     */
    changePatrolDirection() {
        const directions = [DIRECTIONS.UP, DIRECTIONS.DOWN, DIRECTIONS.LEFT, DIRECTIONS.RIGHT];
        
        // 排除当前方向，增加变化性
        const availableDirections = directions.filter(d => d !== this.patrolDirection);
        
        this.patrolDirection = randomChoice(availableDirections);
    }
}

// 导出类
export { Tank, PlayerTank, EnemyTank };
export default Tank;
