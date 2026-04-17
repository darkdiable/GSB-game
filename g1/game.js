// 游戏配置
const CONFIG = {
    CANVAS_WIDTH: 800,
    CANVAS_HEIGHT: 600,
    PLAYER_SPEED: 5,
    PLAYER_MAX_HEALTH: 100,
    BULLET_SPEED: 10,
    ENEMY_SPAWN_RATE: 60,
    PARTICLE_COUNT: 20,
    SKILL_COOLDOWN: 10000
};

// 全局状态（用于跨模块通信）
const GlobalState = {
    frameCount: 0,
    totalEnemiesSpawned: 0,
    bossDefeatedCount: 0
};

// 游戏状态
const GameState = {
    MENU: 0,
    PLAYING: 1,
    PAUSED: 2,
    GAME_OVER: 3
};

// 向量类
class Vector2 {
    constructor(x = 0, y = 0) {
        this.x = x;
        this.y = y;
    }
    
    add(v) {
        return new Vector2(this.x + v.x, this.y + v.y);
    }
    
    subtract(v) {
        return new Vector2(this.x - v.x, this.y - v.y);
    }
    
    multiply(scalar) {
        return new Vector2(this.x * scalar, this.y * scalar);
    }
    
    magnitude() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }
    
    normalize() {
        const mag = this.magnitude();
        if (mag === 0) return new Vector2(0, 0);
        return new Vector2(this.x / mag, this.y / mag);
    }
    
    distance(v) {
        return this.subtract(v).magnitude();
    }
}

// 游戏对象基类
class GameObject {
    constructor(x, y, width, height, color) {
        this.position = new Vector2(x, y);
        this.velocity = new Vector2(0, 0);
        this.width = width;
        this.height = height;
        this.color = color;
        this.rotation = 0;
        this.active = true;
        this.health = 100;
        this.maxHealth = 100;
    }
    
    update(deltaTime) {
        this.position = this.position.add(this.velocity);
    }
    
    render(ctx) {
        ctx.save();
        ctx.translate(this.position.x + this.width / 2, this.position.y + this.height / 2);
        ctx.rotate(this.rotation);
        ctx.fillStyle = this.color;
        ctx.fillRect(-this.width / 2, -this.height / 2, this.width, this.height);
        ctx.restore();
    }
    
    getBounds() {
        return {
            left: this.position.x,
            right: this.position.x + this.width,
            top: this.position.y,
            bottom: this.position.y + this.height
        };
    }
    
    collidesWith(other) {
        const a = this.getBounds();
        const b = other.getBounds();
        return !(a.right < b.left || a.left > b.right || a.bottom < b.top || a.top > b.bottom);
    }
    
    getCenter() {
        return {
            x: this.position.x + this.width,
            y: this.position.y + this.height
        };
    }
}

// 玩家类
class Player extends GameObject {
    constructor(x, y) {
        super(x, y, 50, 50, '#00ffff');
        this.speed = CONFIG.PLAYER_SPEED;
        this.shootCooldown = 0;
        this.shootInterval = 150;
        this.level = 1;
        this.experience = 0;
        this.experienceToNextLevel = 100;
        this.skillCooldown = 0;
        this.skillActive = false;
        this.skillDuration = 0;
        this.weaponLevel = 1;
        this.invulnerable = false;
        this.invulnerableTime = 0;
    }
    
    update(deltaTime, input, game) {
        if (input.keys['KeyW'] || input.keys['ArrowUp']) {
            this.velocity.y = -this.speed;
        } else if (input.keys['KeyS'] || input.keys['ArrowDown']) {
            this.velocity.y = this.speed;
        } else {
            this.velocity.y = 0;
        }
        
        if (input.keys['KeyA'] || input.keys['ArrowLeft']) {
            this.velocity.x = -this.speed;
        } else if (input.keys['KeyD'] || input.keys['ArrowRight']) {
            this.velocity.x = this.speed;
        } else {
            this.velocity.x = 0;
        }
        
        super.update(deltaTime);
        
        this.position.x = Math.max(0, Math.min(CONFIG.CANVAS_WIDTH - this.width, this.position.x));
        this.position.y = Math.max(0, Math.min(CONFIG.CANVAS_HEIGHT - this.height, this.position.y));
        
        if (this.shootCooldown > 0) this.shootCooldown -= deltaTime;
        if (this.skillCooldown > 0) this.skillCooldown -= deltaTime;
        if (this.skillDuration > 0) {
            this.skillDuration -= deltaTime;
            if (this.skillDuration <= 0) {
                this.skillActive = false;
            }
        }
        if (this.invulnerableTime > 0) {
            this.invulnerableTime -= deltaTime;
            if (this.invulnerableTime <= 0) {
                this.invulnerable = false;
            }
        }
        
        if ((input.keys['KeyJ'] || input.keys['Space']) && this.shootCooldown <= 0) {
            this.shoot(game);
        }
        
        if (input.keys['KeyK'] && this.skillCooldown <= 0) {
            this.activateSkill(game);
        }
    }
    
    shoot(game) {
        this.shootCooldown = this.shootInterval;
        
        const centerX = this.position.x + this.width / 2;
        const topY = this.position.y;
        
        if (this.weaponLevel >= 1) {
            game.bullets.push(new Bullet(centerX - 2, topY, 0, -CONFIG.BULLET_SPEED, '#00ffff', true));
        }
        
        if (this.weaponLevel >= 2) {
            game.bullets.push(new Bullet(centerX - 20, topY + 10, 0, -CONFIG.BULLET_SPEED * 0.9, '#00ff00', true));
            game.bullets.push(new Bullet(centerX + 20, topY + 10, 0, -CONFIG.BULLET_SPEED * 0.9, '#00ff00', true));
        }
        
        if (this.weaponLevel >= 3) {
            game.bullets.push(new Bullet(centerX - 30, topY + 20, -1, -CONFIG.BULLET_SPEED * 0.8, '#ff00ff', true));
            game.bullets.push(new Bullet(centerX + 30, topY + 20, 1, -CONFIG.BULLET_SPEED * 0.8, '#ff00ff', true));
        }
        
        game.audio.playShoot();
    }
    
    activateSkill(game) {
        this.skillActive = true;
        this.skillDuration = 5000;
        this.skillCooldown = 0;
        
        for (let i = 0; i < 360; i += 10) {
            const rad = i * Math.PI / 180;
            const vx = Math.cos(rad) * CONFIG.BULLET_SPEED;
            const vy = Math.sin(rad) * CONFIG.BULLET_SPEED;
            game.bullets.push(new Bullet(
                this.position.x + this.width / 2,
                this.position.y + this.height / 2,
                vx,
                vy,
                '#ffff00',
                true,
                true
            ));
        }
        
        game.audio.playSkill();
    }
    
    gainExperience(amount) {
        this.experience += amount;
        if (this.experience >= this.experienceToNextLevel) {
            this.levelUp();
        }
    }
    
    levelUp() {
        this.level++;
        this.experience = this.experienceToNextLevel;
        this.experienceToNextLevel = Math.floor(this.experienceToNextLevel * 1.5);
        this.health = Math.min(this.health + 20, this.maxHealth);
        this.weaponLevel = Math.min(this.weaponLevel + 1, 3);
    }
    
    takeDamage(amount) {
        if (this.invulnerable) return;
        this.health -= amount;
        if (this.health <= 0) {
            this.health = 0;
            this.active = false;
        }
    }
    
    render(ctx) {
        ctx.save();
        ctx.translate(this.position.x + this.width / 2, this.position.y + this.height / 2);
        
        if (this.invulnerable && Math.floor(Date.now() / 100) % 2 === 0) {
            ctx.globalAlpha = 0.5;
        }
        
        ctx.fillStyle = this.skillActive ? '#ffff00' : this.color;
        
        ctx.beginPath();
        ctx.moveTo(0, -this.height / 2);
        ctx.lineTo(-this.width / 2, this.height / 2);
        ctx.lineTo(0, this.height / 2 - 10);
        ctx.lineTo(this.width / 2, this.height / 2);
        ctx.closePath();
        ctx.fill();
        
        ctx.fillStyle = '#0088ff';
        ctx.beginPath();
        ctx.moveTo(-15, this.height / 2 - 5);
        ctx.lineTo(0, this.height / 2 + 15);
        ctx.lineTo(15, this.height / 2 - 5);
        ctx.closePath();
        ctx.fill();
        
        if (this.skillActive) {
            ctx.strokeStyle = '#ffff00';
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(0, 0, this.width, 0, Math.PI * 2);
            ctx.stroke();
        }
        
        ctx.restore();
    }
}

// 子弹类
class Bullet extends GameObject {
    constructor(x, y, vx, vy, color, isPlayerBullet, isSkillBullet = false) {
        super(x, y, isSkillBullet ? 8 : 4, isSkillBullet ? 8 : 10, color);
        this.velocity = new Vector2(vx, vy);
        this.isPlayerBullet = isPlayerBullet;
        this.isSkillBullet = isSkillBullet;
        this.damage = isSkillBullet ? 50 : 10;
    }
    
    update(deltaTime) {
        super.update(deltaTime);
        
        if (this.position.y < -50 || this.position.y > CONFIG.CANVAS_HEIGHT + 50 ||
            this.position.x < -50 || this.position.x > CONFIG.CANVAS_WIDTH + 50) {
            this.active = false;
        }
    }
    
    render(ctx) {
        ctx.save();
        ctx.translate(this.position.x + this.width / 2, this.position.y + this.height / 2);
        
        const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, this.width);
        gradient.addColorStop(0, '#ffffff');
        gradient.addColorStop(0.5, this.color);
        gradient.addColorStop(1, 'transparent');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(0, 0, this.width, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.restore();
    }
}

// 敌人类
class Enemy extends GameObject {
    constructor(x, y, type = 'basic') {
        super(x, y, 40, 40, '#ff0000');
        this.type = type;
        this.shootCooldown = 0;
        this.shootInterval = 2000;
        this.movePattern = 0;
        this.moveTime = 0;
        
        this.setupType();
    }
    
    setupType() {
        switch(this.type) {
            case 'basic':
                this.health = 30;
                this.maxHealth = 30;
                this.speed = 2;
                this.score = 10;
                this.experience = 10;
                this.color = '#ff4444';
                break;
            case 'fast':
                this.health = 20;
                this.maxHealth = 20;
                this.speed = 4;
                this.score = 15;
                this.experience = 15;
                this.color = '#ff8800';
                this.width = 30;
                this.height = 30;
                break;
            case 'tank':
                this.health = 100;
                this.maxHealth = 100;
                this.speed = 1;
                this.score = 30;
                this.experience = 30;
                this.color = '#880000';
                this.width = 60;
                this.height = 60;
                break;
            case 'shooter':
                this.health = 50;
                this.maxHealth = 50;
                this.speed = 1.5;
                this.score = 25;
                this.experience = 25;
                this.color = '#ff00ff';
                this.shootInterval = 1500;
                break;
        }
    }
    
    update(deltaTime, player) {
        this.moveTime += deltaTime;
        
        switch(this.type) {
            case 'basic':
                this.velocity.y = this.speed;
                this.velocity.x = Math.sin(this.moveTime / 500) * 2;
                break;
            case 'fast':
                const dirToPlayer = player.position.subtract(this.position).normalize();
                this.velocity = dirToPlayer.multiply(this.speed);
                break;
            case 'tank':
                this.velocity.y = this.speed * 0.5;
                break;
            case 'shooter':
                if (this.position.y < player.position.y) {
                    this.velocity.y = this.speed * 0.5;
                }
                this.velocity.x = Math.sin(this.moveTime / 1000) * 1.5;
                break;
        }
        
        super.update(deltaTime);
        
        if (this.position.y > CONFIG.CANVAS_HEIGHT + 50) {
            this.active = false;
        }
        
        if (this.type === 'shooter') {
            if (this.shootCooldown > 0) {
                this.shootCooldown -= deltaTime;
            } else {
                this.shoot(player);
                this.shootCooldown = this.shootInterval;
            }
        }
    }
    
    shoot(player) {
        const dir = player.position.subtract(this.position).normalize();
        game.enemyBullets.push(new Bullet(
            this.position.x + this.width,
            this.position.y + this.height,
            dir.x * 5,
            dir.y * 5,
            '#ff00ff',
            false
        ));
    }
    
    render(ctx) {
        ctx.save();
        ctx.translate(this.position.x + this.width / 2, this.position.y + this.height / 2);
        
        ctx.fillStyle = this.color;
        
        switch(this.type) {
            case 'basic':
                ctx.beginPath();
                ctx.moveTo(0, this.height / 2);
                ctx.lineTo(-this.width / 2, -this.height / 2);
                ctx.lineTo(this.width / 2, -this.height / 2);
                ctx.closePath();
                ctx.fill();
                break;
            case 'fast':
                ctx.beginPath();
                ctx.moveTo(0, this.height / 2);
                ctx.lineTo(-this.width / 2, 0);
                ctx.lineTo(0, -this.height / 2);
                ctx.lineTo(this.width / 2, 0);
                ctx.closePath();
                ctx.fill();
                break;
            case 'tank':
                ctx.fillRect(-this.width / 2, -this.height / 2, this.width, this.height);
                ctx.fillStyle = '#ff0000';
                ctx.fillRect(-this.width / 4, -this.height / 4, this.width / 2, this.height / 2);
                break;
            case 'shooter':
                ctx.beginPath();
                ctx.arc(0, 0, this.width / 2, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = '#ffff00';
                ctx.beginPath();
                ctx.arc(0, 0, this.width / 4, 0, Math.PI * 2);
                ctx.fill();
                break;
        }
        
        ctx.restore();
    }
}

// Boss 类
class Boss extends GameObject {
    constructor(x, y, level) {
        super(x, y, 150, 150, '#ff0000');
        this.level = level;
        this.health = 200 * level;
        this.maxHealth = this.health;
        this.speed = 1;
        this.phase = 0;
        this.attackTimer = 0;
        this.moveDirection = 1;
        this.score = 500 * level;
        this.experience = 100 * level;
    }
    
    update(deltaTime, player) {
        this.attackTimer += deltaTime;
        
        if (this.phase === 0) {
            this.position.x += this.speed * this.moveDirection;
            if (this.position.x <= 0 || this.position.x >= CONFIG.CANVAS_WIDTH - this.width) {
                this.moveDirection *= -1;
            }
            
            if (this.health < this.maxHealth * 0.7) {
                this.phase = 1;
            }
        } else if (this.phase === 1) {
            this.position.x += this.speed * 1.5 * this.moveDirection;
            if (this.position.x <= 0 || this.position.x >= CONFIG.CANVAS_WIDTH - this.width) {
                this.moveDirection *= -1;
            }
            
            if (this.attackTimer >= 1000) {
                this.specialAttack(player);
                this.attackTimer = 0;
            }
            
            if (this.health < this.maxHealth * 0.3) {
                this.phase = 2;
            }
        } else {
            const dir = player.position.subtract(this.position).normalize();
            this.velocity = dir.multiply(this.speed * 0.5);
            super.update(deltaTime);
            
            if (this.attackTimer >= 500) {
                this.specialAttack(player);
                this.attackTimer = 0;
            }
        }
    }
    
    specialAttack(player) {
        const centerX = this.position.x + this.width / 2;
        const centerY = this.position.y + this.height / 2;
        
        for (let i = 0; i < 12; i++) {
            const angle = (i / 12) * Math.PI * 2 + this.attackTimer / 1000;
            const vx = Math.cos(angle) * 4;
            const vy = Math.sin(angle) * 4;
            game.enemyBullets.push(new Bullet(centerX, centerY, vx, vy, '#ff00ff', false));
        }
    }
    
    render(ctx) {
        ctx.save();
        ctx.translate(this.position.x + this.width / 2, this.position.y + this.height / 2);
        
        const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, this.width / 2);
        gradient.addColorStop(0, '#ff6666');
        gradient.addColorStop(1, '#ff0000');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(-this.width / 2, -this.height / 2, this.width, this.height);
        
        ctx.fillStyle = '#ffff00';
        ctx.font = '20px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`BOSS Lv.${this.level}`, 0, 10);
        
        const healthPercent = this.health / this.maxHealth;
        ctx.fillStyle = '#ff0000';
        ctx.fillRect(-this.width / 2, -this.height / 2 - 15, this.width, 10);
        ctx.fillStyle = '#00ff00';
        ctx.fillRect(-this.width / 2, -this.height / 2 - 15, this.width * healthPercent, 10);
        
        ctx.restore();
    }
}

// 粒子类
class Particle extends GameObject {
    constructor(x, y, vx, vy, color, lifetime) {
        super(x, y, Math.random() * 4 + 2, Math.random() * 4 + 2, color);
        this.velocity = new Vector2(vx, vy);
        this.lifetime = lifetime;
        this.maxLifetime = lifetime;
        this.alpha = 1;
    }
    
    update(deltaTime) {
        super.update(deltaTime);
        this.lifetime -= deltaTime;
        this.alpha = this.lifetime / this.maxLifetime;
        
        if (this.lifetime <= 0) {
            this.active = false;
        }
    }
    
    render(ctx) {
        ctx.save();
        ctx.globalAlpha = this.alpha;
        ctx.fillStyle = this.color;
        ctx.fillRect(this.position.x, this.position.y, this.width, this.height);
        ctx.restore();
    }
}

// 爆炸效果类
class Explosion {
    constructor(x, y, color, size = 10) {
        this.position = new Vector2(x, y);
        this.color = color;
        this.size = size;
        this.active = true;
        this.lifetime = 500;
        this.maxLifetime = 500;
    }
    
    update(deltaTime) {
        this.lifetime -= deltaTime;
        if (this.lifetime <= 0) {
            this.active = false;
        }
    }
    
    render(ctx) {
        const progress = 1 - (this.lifetime / this.maxLifetime);
        const radius = (progress * this.size * 3);
        const alpha = 1 - progress;
        
        ctx.save();
        ctx.globalAlpha = alpha;
        
        const gradient = ctx.createRadialGradient(
            this.position.x, this.position.y, 0,
            this.position.x, this.position.y, radius
        );
        gradient.addColorStop(0, '#ffffff');
        gradient.addColorStop(0.3, this.color);
        gradient.addColorStop(1, 'transparent');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(this.position.x, this.position.y, radius, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.restore();
    }
}

// 背景星星类
class Star {
    constructor() {
        this.reset();
        this.y = Math.random() * CONFIG.CANVAS_HEIGHT;
    }
    
    reset() {
        this.x = Math.random() * CONFIG.CANVAS_WIDTH;
        this.y = 0;
        this.speed = Math.random() * 2 + 0.5;
        this.size = Math.random() * 2 + 0.5;
        this.brightness = Math.random() * 0.5 + 0.5;
    }
    
    update(deltaTime) {
        this.y += this.speed;
        if (this.y > CONFIG.CANVAS_HEIGHT) {
            this.reset();
        }
    }
    
    render(ctx) {
        ctx.fillStyle = `rgba(255, 255, 255, ${this.brightness})`;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

// 输入处理类
class InputHandler {
    constructor() {
        this.keys = {};
        
        window.addEventListener('keydown', (e) => {
            this.keys[e.code] = true;
            if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) {
                e.preventDefault();
            }
        });
        
        window.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
    }
}

// 音频系统（使用 Web Audio API 生成音效）
class AudioSystem {
    constructor() {
        this.enabled = true;
        this.audioContext = null;
    }
    
    init() {
        if (!this.audioContext) {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
    }
    
    playTone(frequency, duration, type = 'square', volume = 0.1) {
        if (!this.enabled || !this.audioContext) return;
        
        const oscillator = this.audioContext.createOscillator();
        const gainNode = this.audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(this.audioContext.destination);
        
        oscillator.frequency.value = frequency;
        oscillator.type = type;
        
        gainNode.gain.setValueAtTime(volume, this.audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + duration);
        
        oscillator.start(this.audioContext.currentTime);
        oscillator.stop(this.audioContext.currentTime + duration);
    }
    
    playShoot() {
        this.playTone(800, 0.1, 'square', 0.05);
    }
    
    playExplosion() {
        this.playTone(100, 0.3, 'sawtooth', 0.1);
    }
    
    playSkill() {
        for (let i = 0; i < 5; i++) {
            setTimeout(() => {
                this.playTone(400 + i * 200, 0.1, 'sine', 0.1);
            }, i * 50);
        }
    }
    
    playLevelUp() {
        for (let i = 0; i < 8; i++) {
            setTimeout(() => {
                this.playTone(300 + i * 100, 0.15, 'sine', 0.1);
            }, i * 100);
        }
    }
    
    playHit() {
        this.playTone(200, 0.1, 'sawtooth', 0.08);
    }
}

// 关卡系统
class LevelSystem {
    constructor() {
        this.currentLevel = 1;
        this.currentWave = 0;
        this.enemiesPerWave = 5;
        this.waveDelay = 2000;
        this.bossSpawned = false;
    }
    
    update(game) {
        if (game.enemies.length === 0 && !this.bossSpawned) {
            this.currentWave++;
            
            if (this.currentWave % 5 === 0 && !this.bossSpawned) {
                this.spawnBoss(game);
                this.bossSpawned = true;
            } else {
                this.spawnWave(game);
            }
        }
        
        if (game.boss && !game.boss.active) {
            this.currentWave = 0;
        }
    }
    
    spawnWave(game) {
        const count = Math.min(this.enemiesPerWave + this.currentWave, 20);
        
        for (let i = 0; i < count; i++) {
            setTimeout(() => {
                if (game.state === GameState.PLAYING) {
                    const types = ['basic', 'fast', 'tank', 'shooter'];
                    const type = types[Math.floor(Math.random() * types.length)];
                    const x = Math.random() * CONFIG.CANVAS_WIDTH + 100;
                    const enemy = new Enemy(x, -50, type);
                    game.enemies.push(enemy);
                    GlobalState.totalEnemiesSpawned++;
                    
                    if (GlobalState.totalEnemiesSpawned % 50 === 0) {
                        this.enemiesPerWave++;
                    }
                }
            }, i * 500);
        }
    }
    
    spawnBoss(game) {
        const x = (CONFIG.CANVAS_WIDTH - 150) / 2;
        game.boss = new Boss(x, -200, this.currentLevel);
        game.boss.maxHealth = 200 * this.currentLevel;
    }
    
    nextLevel(game) {
        this.currentLevel++;
        this.enemiesPerWave += 2;
        this.bossSpawned = false;
        game.player.gainExperience(50);
        GlobalState.bossDefeatedCount++;
        
        if (GlobalState.bossDefeatedCount % 3 === 0) {
            game.player.weaponLevel = Math.min(game.player.weaponLevel + 1, 3);
        }
    }
}

// 主游戏类
class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.input = new InputHandler();
        this.audio = new AudioSystem();
        this.state = GameState.MENU;
        this.lastTime = 0;
        this.score = 0;
        
        this.player = null;
        this.bullets = [];
        this.enemyBullets = [];
        this.enemies = [];
        this.particles = [];
        this.explosions = [];
        this.stars = [];
        this.boss = null;
        this.levelSystem = new LevelSystem();
        
        this.ui = {
            score: document.getElementById('score-display'),
            health: document.getElementById('health-bar'),
            level: document.getElementById('level-display'),
            wave: document.getElementById('wave-display'),
            exp: document.getElementById('exp-bar'),
            startScreen: document.getElementById('start-screen'),
            gameOverScreen: document.getElementById('game-over-screen'),
            pauseScreen: document.getElementById('pause-screen'),
            finalScore: document.getElementById('final-score')
        };
        
        this.init();
    }
    
    init() {
        for (let i = 0; i < 100; i++) {
            this.stars.push(new Star());
        }
        
        document.getElementById('start-btn').addEventListener('click', () => this.start());
        document.getElementById('restart-btn').addEventListener('click', () => this.restart());
        document.getElementById('resume-btn').addEventListener('click', () => this.resume());
        
        window.addEventListener('keydown', (e) => {
            if (e.code === 'KeyP' && this.state !== GameState.MENU) {
                this.togglePause();
            }
        });
        
        this.gameLoop(0);
    }
    
    start() {
        this.audio.init();
        this.state = GameState.PLAYING;
        this.player = new Player(
            (CONFIG.CANVAS_WIDTH - 50) / 2,
            CONFIG.CANVAS_HEIGHT - 100
        );
        this.bullets = [];
        this.enemyBullets = [];
        this.enemies = [];
        this.particles = [];
        this.explosions = [];
        this.boss = null;
        this.levelSystem = new LevelSystem();
        this.score = 0;
        this.lastTime = 0;
        this.levelSystem.spawnWave(this);
        
        this.ui.startScreen.classList.add('hidden');
        this.ui.gameOverScreen.classList.add('hidden');
        this.ui.pauseScreen.classList.add('hidden');
    }
    
    restart() {
        this.start();
    }
    
    togglePause() {
        if (this.state === GameState.PLAYING) {
            this.state = GameState.PAUSED;
            this.ui.pauseScreen.classList.remove('hidden');
        } else if (this.state === GameState.PAUSED) {
            this.resume();
        }
    }
    
    resume() {
        this.state = GameState.PLAYING;
        this.ui.pauseScreen.classList.add('hidden');
    }
    
    gameOver() {
        this.state = GameState.GAME_OVER;
        this.ui.finalScore.textContent = `最终分数：${this.score}`;
        this.ui.gameOverScreen.classList.remove('hidden');
    }
    
    createExplosion(x, y, color, count = 10) {
        this.explosions.push(new Explosion(x, y, color, count));
        
        for (let i = 0; i < CONFIG.PARTICLE_COUNT; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 5 + 2;
            const vx = Math.cos(angle) * speed;
            const vy = Math.sin(angle) * speed;
            this.particles.push(new Particle(x, y, vx, vy, color, 1000));
        }
    }
    
    checkCollisions() {
        for (const bullet of this.bullets) {
            if (!bullet.active || !bullet.isPlayerBullet) continue;
            
            for (const enemy of this.enemies) {
                if (enemy.active && bullet.collidesWith(enemy)) {
                    bullet.active = false;
                    enemy.health -= bullet.damage;
                    
                    if (enemy.health <= 0) {
                        enemy.active = false;
                        this.score += enemy.score;
                        this.player.gainExperience(enemy.experience);
                        this.createExplosion(
                            enemy.getCenter().x,
                            enemy.getCenter().y,
                            enemy.color
                        );
                        this.audio.playExplosion();
                    } else {
                        this.audio.playHit();
                    }
                }
            }
            
            if (this.boss && this.boss.active && bullet.collidesWith(this.boss)) {
                bullet.active = false;
                this.boss.health -= bullet.damage;
                this.audio.playHit();
                
                if (this.boss.health <= 0) {
                    this.boss.active = false;
                    this.score += this.boss.score;
                    this.player.gainExperience(this.boss.experience);
                    this.createExplosion(
                        this.boss.getCenter().x,
                        this.boss.getCenter().y,
                        '#ff0000',
                        30
                    );
                    this.audio.playExplosion();
                    this.levelSystem.nextLevel(this);
                }
            }
        }
        
        for (const bullet of this.enemyBullets) {
            if (!bullet.active || bullet.isPlayerBullet) continue;
            
            if (this.player.active && bullet.collidesWith(this.player)) {
                bullet.active = false;
                this.player.takeDamage(10);
                this.audio.playHit();
                
                if (!this.player.active) {
                    this.createExplosion(
                        this.player.getCenter().x,
                        this.player.getCenter().y,
                        '#00ffff',
                        30
                    );
                    this.gameOver();
                }
            }
        }
        
        for (const enemy of this.enemies) {
            if (enemy.active && this.player.active && enemy.collidesWith(this.player)) {
                enemy.active = false;
                this.player.takeDamage(20);
                this.createExplosion(
                    enemy.getCenter().x,
                    enemy.getCenter().y,
                    enemy.color
                );
                this.audio.playExplosion();
                
                if (!this.player.active) {
                    this.gameOver();
                }
            }
        }
        
        if (this.boss && this.boss.active && this.player.active && this.boss.collidesWith(this.player)) {
            this.player.takeDamage(1);
        }
    }
    
    updateUI() {
        this.ui.score.textContent = `分数：${this.score}`;
        this.ui.health.style.width = `${(this.player.health / this.player.maxHealth) * 100}%`;
        this.ui.level.textContent = `等级：${this.player.level}`;
        this.ui.wave.textContent = `波次：${this.levelSystem.currentWave}`;
        this.ui.exp.style.width = `${(this.player.experience / this.player.experienceToNextLevel) * 100}%`;
        
        if (this.player.level > 10) {
            this.ui.exp.style.display = 'none';
        }
    }
    
    update(deltaTime) {
        if (this.state !== GameState.PLAYING) {
            for (const star of this.stars) {
                star.update(deltaTime);
            }
            return;
        }
        
        if (deltaTime > 100) {
            deltaTime = 16;
        }
        
        this.player.update(deltaTime, this.input, this);
        
        for (const bullet of this.bullets) {
            bullet.update(deltaTime);
        }
        
        for (const bullet of this.enemyBullets) {
            bullet.update(deltaTime);
        }
        
        for (const enemy of this.enemies) {
            enemy.update(deltaTime, this.player);
        }
        
        if (this.boss && this.boss.active) {
            this.boss.update(deltaTime, this.player);
        }
        
        for (const particle of this.particles) {
            particle.update(deltaTime);
        }
        
        for (const explosion of this.explosions) {
            explosion.update(deltaTime);
        }
        
        for (const star of this.stars) {
            star.update(deltaTime);
        }
        
        this.bullets = this.bullets.filter(b => b.active);
        this.enemyBullets = this.enemyBullets.filter(b => b.active);
        this.enemies = this.enemies.filter(e => e.active);
        this.particles = this.particles.filter(p => p.active);
        this.explosions = this.explosions.filter(e => e.active);
        
        this.checkCollisions();
        this.levelSystem.update(this);
        this.updateUI();
    }
    
    render() {
        this.ctx.fillStyle = '#000020';
        this.ctx.fillRect(0, 0, CONFIG.CANVAS_WIDTH, CONFIG.CANVAS_HEIGHT);
        
        for (const star of this.stars) {
            star.render(this.ctx);
        }
        
        if (this.state === GameState.PLAYING && this.player.active) {
            this.player.render(this.ctx);
        }
        
        for (const bullet of this.bullets) {
            bullet.render(this.ctx);
        }
        
        for (const bullet of this.enemyBullets) {
            bullet.render(this.ctx);
        }
        
        for (const enemy of this.enemies) {
            enemy.render(this.ctx);
        }
        
        if (this.boss && this.boss.active) {
            this.boss.render(this.ctx);
        }
        
        for (const particle of this.particles) {
            particle.render(this.ctx);
        }
        
        for (const explosion of this.explosions) {
            explosion.render(this.ctx);
        }
    }
    
    gameLoop(timestamp) {
        const deltaTime = timestamp - this.lastTime;
        this.lastTime = timestamp;
        
        GlobalState.frameCount++;
        
        this.update(deltaTime);
        this.render();
        
        requestAnimationFrame((t) => this.gameLoop(t));
    }
}

const game = new Game();
