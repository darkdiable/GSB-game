import { DIRECTIONS, TANK_TYPES, GAME_STATES, TILE_SIZE, MAP_WIDTH, MAP_HEIGHT } from './Constants.js';
import { PlayerTank, EnemyTank } from './Tank.js';
import Map from './Map.js';
import Collision from './Collision.js';
import { randomInt, randomChoice } from './Utils.js';

class Game {
    constructor(canvas, callbacks = {}) {
        // 画布设置
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        
        // 回调函数
        this.callbacks = {
            onScoreUpdate: callbacks.onScoreUpdate || (() => {}),
            onLivesUpdate: callbacks.onLivesUpdate || (() => {}),
            onLevelUpdate: callbacks.onLevelUpdate || (() => {}),
            onGameOver: callbacks.onGameOver || (() => {}),
            onLevelComplete: callbacks.onLevelComplete || (() => {})
        };
        
        // 游戏状态
        this.state = GAME_STATES.IDLE;
        this.score = 0;
        this.lives = 3;
        this.level = 1;
        
        // 游戏对象
        this.map = null;
        this.collision = null;
        this.playerTank = null;
        this.enemyTanks = [];
        this.bullets = [];
        
        // 敌方坦克生成
        this.maxEnemyTanks = 4;
        this.enemySpawnTimer = 0;
        this.enemySpawnInterval = 5000; // 5秒
        this.enemiesRemaining = 10; // 每关需要消灭的敌方坦克数量
        
        // 动画循环
        this.lastTime = 0;
        this.animationId = null;
        
        // 键盘事件绑定
        this.bindKeyEvents();
        
        // 初始化游戏
        this.init();
    }
    
    /**
     * 初始化游戏
     */
    init() {
        // 创建地图
        this.map = new Map();
        
        // 创建碰撞检测
        this.collision = new Collision(this.map);
        
        // 重置游戏状态
        this.resetGameState();
    }
    
    /**
     * 重置游戏状态
     */
    resetGameState() {
        // 重置地图
        this.map.reset();
        
        // 创建玩家坦克
        this.createPlayerTank();
        
        // 清空敌方坦克和子弹
        this.enemyTanks = [];
        this.bullets = [];
        
        // 重置敌方生成计时器
        this.enemySpawnTimer = 0;
        this.enemiesRemaining = 10 + (this.level - 1) * 2; // 每关增加敌方数量
        
        // 生成初始敌方坦克
        this.spawnInitialEnemies();
    }
    
    /**
     * 创建玩家坦克
     */
    createPlayerTank() {
        // 玩家初始位置：地图底部中间偏左
        const startX = TILE_SIZE * 2;
        const startY = TILE_SIZE * (MAP_HEIGHT - 2);
        
        this.playerTank = new PlayerTank(startX, startY, DIRECTIONS.UP);
    }
    
    /**
     * 生成初始敌方坦克
     */
    spawnInitialEnemies() {
        // 生成2-3个初始敌方坦克
        const initialCount = Math.min(3, this.enemiesRemaining);
        
        for (let i = 0; i < initialCount; i++) {
            this.spawnEnemyTank();
        }
    }
    
    /**
     * 生成敌方坦克
     */
    spawnEnemyTank() {
        if (this.enemiesRemaining <= 0) return;
        if (this.enemyTanks.length >= this.maxEnemyTanks) return;
        
        // 生成位置：地图顶部三个位置
        const spawnPositions = [
            { x: TILE_SIZE * 0, y: TILE_SIZE * 0 },
            { x: TILE_SIZE * 6, y: TILE_SIZE * 0 },
            { x: TILE_SIZE * 12, y: TILE_SIZE * 0 }
        ];
        
        // 选择一个可用的生成位置
        const availablePositions = spawnPositions.filter(pos => {
            // 检查位置是否被占用
            for (const tank of this.enemyTanks) {
                if (Math.abs(tank.x - pos.x) < TILE_SIZE && 
                    Math.abs(tank.y - pos.y) < TILE_SIZE) {
                    return false;
                }
            }
            return true;
        });
        
        if (availablePositions.length === 0) return;
        
        const position = randomChoice(availablePositions);
        
        // 随机选择敌方坦克类型
        const tankTypes = [TANK_TYPES.BASIC, TANK_TYPES.FAST, TANK_TYPES.HEAVY];
        // 根据关卡调整重型坦克出现概率
        const weights = this.level < 3 ? [0.6, 0.3, 0.1] : [0.4, 0.3, 0.3];
        
        let tankType;
        const rand = Math.random();
        if (rand < weights[0]) {
            tankType = TANK_TYPES.BASIC;
        } else if (rand < weights[0] + weights[1]) {
            tankType = TANK_TYPES.FAST;
        } else {
            tankType = TANK_TYPES.HEAVY;
        }
        
        // 创建敌方坦克
        const enemyTank = new EnemyTank(
            position.x,
            position.y,
            DIRECTIONS.DOWN,
            tankType
        );
        
        this.enemyTanks.push(enemyTank);
        this.enemiesRemaining--;
    }
    
    /**
     * 绑定键盘事件
     */
    bindKeyEvents() {
        document.addEventListener('keydown', (e) => {
            if (this.playerTank && this.state === GAME_STATES.PLAYING) {
                this.playerTank.handleKeyDown(e.key);
            }
            
            // 阻止空格键和方向键的默认行为（页面滚动）
            if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
                e.preventDefault();
            }
        });
        
        document.addEventListener('keyup', (e) => {
            if (this.playerTank) {
                this.playerTank.handleKeyUp(e.key);
            }
        });
    }
    
    /**
     * 开始游戏
     */
    start() {
        if (this.state === GAME_STATES.PLAYING) return;
        
        this.state = GAME_STATES.PLAYING;
        this.lastTime = performance.now();
        
        // 启动游戏循环
        this.gameLoop();
    }
    
    /**
     * 暂停游戏
     */
    pause() {
        if (this.state !== GAME_STATES.PLAYING) return;
        
        this.state = GAME_STATES.PAUSED;
        
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
    }
    
    /**
     * 重置游戏
     */
    reset() {
        this.pause();
        
        this.score = 0;
        this.lives = 3;
        this.level = 1;
        
        this.updateUI();
        this.resetGameState();
        
        this.state = GAME_STATES.IDLE;
    }
    
    /**
     * 下一关
     */
    nextLevel() {
        this.pause();
        
        this.level++;
        this.updateUI();
        this.resetGameState();
        
        this.state = GAME_STATES.IDLE;
    }
    
    /**
     * 更新UI
     */
    updateUI() {
        this.callbacks.onScoreUpdate(this.score);
        this.callbacks.onLivesUpdate(this.lives);
        this.callbacks.onLevelUpdate(this.level);
    }
    
    /**
     * 游戏主循环
     */
    gameLoop() {
        const currentTime = performance.now();
        const deltaTime = currentTime - this.lastTime;
        this.lastTime = currentTime;
        
        // 更新游戏逻辑
        this.update(deltaTime);
        
        // 渲染游戏
        this.render();
        
        // 继续循环
        if (this.state === GAME_STATES.PLAYING) {
            this.animationId = requestAnimationFrame(() => this.gameLoop());
        }
    }
    
    /**
     * 更新游戏逻辑
     * @param {number} deltaTime - 时间增量（毫秒）
     */
    update(deltaTime) {
        // 更新玩家坦克
        this.updatePlayerTank(deltaTime);
        
        // 更新敌方坦克
        this.updateEnemyTanks(deltaTime);
        
        // 更新子弹
        this.updateBullets(deltaTime);
        
        // 检测碰撞
        this.checkCollisions();
        
        // 生成敌方坦克
        this.updateEnemySpawning(deltaTime);
        
        // 检查游戏状态
        this.checkGameState();
    }
    
    /**
     * 更新玩家坦克
     * @param {number} deltaTime - 时间增量
     */
    updatePlayerTank(deltaTime) {
        if (!this.playerTank || !this.playerTank.active) return;
        
        // 获取所有其他坦克
        const otherTanks = [...this.enemyTanks];
        
        // 更新玩家坦克
        const newBullet = this.playerTank.updatePlayer(deltaTime, this.collision, otherTanks);
        
        if (newBullet) {
            this.bullets.push(newBullet);
        }
    }
    
    /**
     * 更新敌方坦克
     * @param {number} deltaTime - 时间增量
     */
    updateEnemyTanks(deltaTime) {
        // 获取所有坦克（用于碰撞检测）
        const allTanks = [this.playerTank, ...this.enemyTanks].filter(t => t && t.active);
        
        for (let i = this.enemyTanks.length - 1; i >= 0; i--) {
            const enemyTank = this.enemyTanks[i];
            
            if (!enemyTank.active) {
                // 移除不活跃的坦克
                this.enemyTanks.splice(i, 1);
                continue;
            }
            
            // 获取其他坦克
            const otherTanks = allTanks.filter(t => t !== enemyTank);
            
            // 更新AI
            const newBullet = enemyTank.updateAI(
                deltaTime,
                this.collision,
                otherTanks,
                this.playerTank
            );
            
            if (newBullet) {
                this.bullets.push(newBullet);
            }
        }
    }
    
    /**
     * 更新子弹
     * @param {number} deltaTime - 时间增量
     */
    updateBullets(deltaTime) {
        for (let i = this.bullets.length - 1; i >= 0; i--) {
            const bullet = this.bullets[i];
            
            if (!bullet.active) {
                this.bullets.splice(i, 1);
                continue;
            }
            
            bullet.update();
        }
    }
    
    /**
     * 更新敌方坦克生成
     * @param {number} deltaTime - 时间增量
     */
    updateEnemySpawning(deltaTime) {
        this.enemySpawnTimer += deltaTime;
        
        if (this.enemySpawnTimer >= this.enemySpawnInterval) {
            this.spawnEnemyTank();
            this.enemySpawnTimer = 0;
        }
    }
    
    /**
     * 检测碰撞
     */
    checkCollisions() {
        // 所有坦克
        const allTanks = [this.playerTank, ...this.enemyTanks].filter(t => t && t.active);
        
        // 检测子弹碰撞
        for (let i = this.bullets.length - 1; i >= 0; i--) {
            const bullet = this.bullets[i];
            
            if (!bullet.active) continue;
            
            // 检测子弹与地图碰撞
            const mapCollision = this.collision.checkBulletMapCollision(bullet);
            
            if (mapCollision.collided) {
                bullet.destroy();
                
                // 如果摧毁了基地，游戏结束
                if (this.collision.isBaseDestroyed()) {
                    this.gameOver();
                }
                continue;
            }
            
            // 检测子弹与坦克碰撞
            const tankCollision = this.collision.checkBulletTankCollision(bullet, allTanks);
            
            if (tankCollision.collided && tankCollision.hitTank) {
                bullet.destroy();
                
                // 击中坦克
                const hitTank = tankCollision.hitTank;
                hitTank.destroy();
                
                // 如果击中的是敌方坦克，加分
                if (hitTank !== this.playerTank) {
                    this.score += hitTank.score;
                    this.updateUI();
                } else {
                    // 玩家被击中
                    this.playerHit();
                }
            }
            
            // 检测子弹与子弹碰撞
            for (let j = i + 1; j < this.bullets.length; j++) {
                const otherBullet = this.bullets[j];
                
                if (this.collision.checkBulletBulletCollision(bullet, otherBullet)) {
                    bullet.destroy();
                    otherBullet.destroy();
                }
            }
        }
    }
    
    /**
     * 玩家被击中
     */
    playerHit() {
        this.lives--;
        this.updateUI();
        
        if (this.lives <= 0) {
            this.gameOver();
        } else {
            // 重新生成玩家坦克
            this.createPlayerTank();
        }
    }
    
    /**
     * 检查游戏状态
     */
    checkGameState() {
        // 检查是否所有敌方坦克都被消灭
        const activeEnemies = this.enemyTanks.filter(t => t.active).length;
        
        if (activeEnemies === 0 && this.enemiesRemaining === 0) {
            this.levelComplete();
        }
        
        // 检查基地是否被摧毁
        if (this.collision.isBaseDestroyed()) {
            this.gameOver();
        }
    }
    
    /**
     * 游戏结束
     */
    gameOver() {
        this.state = GAME_STATES.GAME_OVER;
        this.pause();
        this.callbacks.onGameOver();
    }
    
    /**
     * 关卡完成
     */
    levelComplete() {
        this.state = GAME_STATES.LEVEL_COMPLETE;
        this.pause();
        this.callbacks.onLevelComplete();
    }
    
    /**
     * 渲染游戏
     */
    render() {
        // 清空画布
        this.ctx.fillStyle = '#000000';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // 渲染地图
        if (this.map) {
            this.map.render(this.ctx);
        }
        
        // 渲染坦克
        // 先渲染敌方坦克
        for (const enemyTank of this.enemyTanks) {
            if (enemyTank.active) {
                enemyTank.render(this.ctx);
            }
        }
        
        // 再渲染玩家坦克
        if (this.playerTank && this.playerTank.active) {
            this.playerTank.render(this.ctx);
        }
        
        // 渲染子弹
        for (const bullet of this.bullets) {
            if (bullet.active) {
                bullet.render(this.ctx);
            }
        }
    }
}

export default Game;
