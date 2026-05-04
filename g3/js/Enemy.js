export class Enemy {
    constructor(x, y, canvasWidth, canvasHeight) {
        this.x = x;
        this.y = y;
        this.canvasWidth = canvasWidth;
        this.canvasHeight = canvasHeight;
        this.width = 30;
        this.height = 30;
        this.speed = 2;
        this.score = 100;
        this.active = true;
        this.type = 'A';
    }

    update() {
        this.y += this.speed;
        if (this.y > this.canvasHeight) {
            this.active = false;
            return true;
        }
        return false;
    }

    draw(ctx) {
        ctx.fillStyle = '#ff4444';
        ctx.fillRect(this.x, this.y, this.width, this.height);
        
        ctx.fillStyle = '#aa0000';
        ctx.fillRect(this.x + 5, this.y + 5, this.width - 10, this.height - 10);
    }

    getBounds() {
        return {
            x: this.x,
            y: this.y,
            width: this.width,
            height: this.height
        };
    }

    deactivate() {
        this.active = false;
    }

    getScore() {
        return this.score;
    }

    getType() {
        return this.type;
    }
}

export class EnemyA extends Enemy {
    constructor(x, y, canvasWidth, canvasHeight) {
        super(x, y, canvasWidth, canvasHeight);
        this.type = 'A';
        this.score = 100;
        this.speed = 2;
    }

    draw(ctx) {
        ctx.save();
        ctx.translate(this.x + this.width / 2, this.y + this.height / 2);

        ctx.fillStyle = '#ff4444';
        ctx.beginPath();
        ctx.moveTo(0, this.height / 2);
        ctx.lineTo(-this.width / 2, -this.height / 2);
        ctx.lineTo(this.width / 2, -this.height / 2);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#aa0000';
        ctx.beginPath();
        ctx.arc(0, 0, 8, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }
}

export class EnemyB extends Enemy {
    constructor(x, y, canvasWidth, canvasHeight) {
        super(x, y, canvasWidth, canvasHeight);
        this.type = 'B';
        this.score = 150;
        this.speed = 1.5;
        this.horizontalSpeed = 2;
        this.direction = Math.random() < 0.5 ? 1 : -1;
        this.time = 0;
    }

    update() {
        this.y += this.speed;
        this.time += 0.05;
        this.x += Math.sin(this.time) * this.horizontalSpeed * this.direction;

        if (this.x <= 0) {
            this.x = 0;
            this.direction = 1;
        }
        if (this.x >= this.canvasWidth - this.width) {
            this.x = this.canvasWidth - this.width;
            this.direction = -1;
        }

        if (this.y > this.canvasHeight) {
            this.active = false;
            return true;
        }
        return false;
    }

    draw(ctx) {
        ctx.save();
        ctx.translate(this.x + this.width / 2, this.y + this.height / 2);

        ctx.fillStyle = '#44ff44';
        ctx.beginPath();
        ctx.arc(0, 0, this.width / 2, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#00aa00';
        ctx.beginPath();
        ctx.arc(-8, -5, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(8, -5, 5, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = '#44ff44';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(-8, this.height / 2);
        ctx.quadraticCurveTo(-12, this.height / 2 + 10, -8, this.height / 2 + 15);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(8, this.height / 2);
        ctx.quadraticCurveTo(12, this.height / 2 + 10, 8, this.height / 2 + 15);
        ctx.stroke();

        ctx.restore();
    }
}

export class EnemyC extends Enemy {
    constructor(x, y, canvasWidth, canvasHeight) {
        super(x, y, canvasWidth, canvasHeight);
        this.type = 'C';
        this.score = 200;
        this.speed = 1.8;
        this.playerX = canvasWidth / 2;
    }

    update() {
        const dx = this.playerX - (this.x + this.width / 2);
        const dist = Math.abs(dx);
        
        if (dist > 2) {
            this.x += (dx > 0 ? 1 : -1) * Math.min(this.speed * 0.8, dist);
        }

        this.y += this.speed;

        if (this.x <= 0) this.x = 0;
        if (this.x >= this.canvasWidth - this.width) this.x = this.canvasWidth - this.width;

        if (this.y > this.canvasHeight) {
            this.active = false;
            return true;
        }
        return false;
    }

    setPlayerX(playerX) {
        this.playerX = playerX;
    }

    draw(ctx) {
        ctx.save();
        ctx.translate(this.x + this.width / 2, this.y + this.height / 2);

        ctx.fillStyle = '#ff44ff';
        ctx.beginPath();
        ctx.moveTo(0, -this.height / 2);
        ctx.lineTo(this.width / 2, 0);
        ctx.lineTo(0, this.height / 2);
        ctx.lineTo(-this.width / 2, 0);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#aa00aa';
        ctx.beginPath();
        ctx.arc(0, 0, 8, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ff00ff';
        ctx.beginPath();
        ctx.arc(0, 0, 4, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }
}

export class EnemyManager {
    constructor(canvasWidth, canvasHeight) {
        this.enemies = [];
        this.canvasWidth = canvasWidth;
        this.canvasHeight = canvasHeight;
        this.wave = 1;
        this.enemiesPerWave = 3;
        this.enemiesSpawned = 0;
        this.framesPerSpawn = 60;
        this.lastSpawnFrame = 0;
        this.waveComplete = false;
    }

    spawnEnemy(currentFrame) {
        if (this.enemiesSpawned >= this.enemiesPerWave) {
            return;
        }

        if (currentFrame - this.lastSpawnFrame < this.framesPerSpawn) {
            return;
        }

        const x = Math.random() * (this.canvasWidth - 30);
        let enemy;

        const type = this.getEnemyType();

        if (type === 'A') {
            enemy = new EnemyA(x, -30, this.canvasWidth, this.canvasHeight);
        } else if (type === 'B') {
            enemy = new EnemyB(x, -30, this.canvasWidth, this.canvasHeight);
        } else {
            enemy = new EnemyC(x, -30, this.canvasWidth, this.canvasHeight);
        }

        this.enemies.push(enemy);
        this.enemiesSpawned++;
        this.lastSpawnFrame = currentFrame;
    }

    getEnemyType() {
        if (this.wave < 3) {
            return Math.random() < 0.7 ? 'A' : 'B';
        }
        
        const rand = Math.random();
        if (rand < 0.4) return 'A';
        if (rand < 0.75) return 'B';
        return 'C';
    }

    update(playerCenterX) {
        let enemiesEscaped = 0;

        this.enemies = this.enemies.filter(enemy => {
            if (enemy.getType() === 'C') {
                enemy.setPlayerX(playerCenterX);
            }

            const escaped = enemy.update();
            if (escaped) {
                enemiesEscaped++;
            }
            return enemy.active;
        });

        if (this.enemiesSpawned >= this.enemiesPerWave && this.enemies.length === 0 && !this.waveComplete) {
            this.waveComplete = true;
            this.nextWave();
        }

        return enemiesEscaped;
    }

    nextWave() {
        this.wave++;
        this.enemiesPerWave = 3 + this.wave;
        this.enemiesSpawned = 0;
        this.waveComplete = false;
        this.framesPerSpawn = Math.max(30, 60 - this.wave * 5);
    }

    draw(ctx) {
        this.enemies.forEach(enemy => enemy.draw(ctx));
    }

    clearAll() {
        const destroyedCount = this.enemies.length;
        this.enemies = [];
        return destroyedCount;
    }

    getWave() {
        return this.wave;
    }

    clear() {
        this.enemies = [];
        this.wave = 1;
        this.enemiesPerWave = 3;
        this.enemiesSpawned = 0;
        this.lastSpawnFrame = 0;
        this.waveComplete = false;
        this.framesPerSpawn = 60;
    }
}
