import { Player } from './Player.js';
import { BulletManager } from './Bullet.js';
import { EnemyManager } from './Enemy.js';
import { PowerUpManager } from './PowerUp.js';
import { Collision } from './Collision.js';
import { UI } from './UI.js';

class Game {
    constructor() {
        this.LOGICAL_WIDTH = 800;
        this.LOGICAL_HEIGHT = 450;
        this.ASPECT_RATIO = 16 / 9;

        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');

        this.setupCanvas();
        this.setupEventListeners();

        this.player = new Player(this.LOGICAL_WIDTH, this.LOGICAL_HEIGHT);
        this.bulletManager = new BulletManager(this.LOGICAL_WIDTH, this.LOGICAL_HEIGHT);
        this.enemyManager = new EnemyManager(this.LOGICAL_WIDTH, this.LOGICAL_HEIGHT);
        this.powerUpManager = new PowerUpManager(this.LOGICAL_WIDTH, this.LOGICAL_HEIGHT);
        this.ui = new UI(this.LOGICAL_WIDTH, this.LOGICAL_HEIGHT);

        this.keys = {
            left: false,
            right: false,
            space: false
        };

        this.currentFrame = 0;
        this.isPaused = false;
        this.isGameOver = false;
        this.animationId = null;
        this.eventsBound = false;
    }

    setupCanvas() {
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
    }

    resizeCanvas() {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        let canvasWidth, canvasHeight;

        if (windowWidth / windowHeight > this.ASPECT_RATIO) {
            canvasHeight = windowHeight - 40;
            canvasWidth = canvasHeight * this.ASPECT_RATIO;
        } else {
            canvasWidth = windowWidth - 40;
            canvasHeight = canvasWidth / this.ASPECT_RATIO;
        }

        this.canvas.width = canvasWidth;
        this.canvas.height = canvasHeight;

        this.scaleX = this.LOGICAL_WIDTH / canvasWidth;
        this.scaleY = this.LOGICAL_HEIGHT / canvasHeight;
    }

    setupEventListeners() {
        if (this.eventsBound) {
            return;
        }

        window.addEventListener('keydown', (e) => this.handleKeyDown(e));
        window.addEventListener('keyup', (e) => this.handleKeyUp(e));
        this.canvas.addEventListener('click', () => this.handleCanvasClick());

        this.eventsBound = true;
    }

    handleKeyDown(e) {
        const key = e.key.toLowerCase();

        if (key === 'a' || key === 'arrowleft') {
            this.keys.left = true;
        }
        if (key === 'd' || key === 'arrowright') {
            this.keys.right = true;
        }
        if (key === ' ' || e.code === 'Space') {
            e.preventDefault();
            if (!e.repeat) {
                if (!this.isPaused && !this.isGameOver) {
                    this.bulletManager.fire(
                        this.player.getCenterX(),
                        this.player.y,
                        true,
                        this.currentFrame
                    );
                }
            }
        }
        if (key === 'p') {
            if (!this.isGameOver) {
                this.togglePause();
            }
        }
        if (key === 'x') {
            if (!this.isPaused && !this.isGameOver) {
                this.useBomb();
            }
        }
        if (key === 'r') {
            this.resetGame();
        }
    }

    handleKeyUp(e) {
        const key = e.key.toLowerCase();

        if (key === 'a' || key === 'arrowleft') {
            this.keys.left = false;
        }
        if (key === 'd' || key === 'arrowright') {
            this.keys.right = false;
        }
        if (key === ' ') {
            this.keys.space = false;
        }
    }

    handleCanvasClick() {
        if (this.isGameOver) {
            this.resetGame();
        }
    }

    togglePause() {
        this.isPaused = !this.isPaused;

        if (this.isPaused) {
            if (this.animationId) {
                cancelAnimationFrame(this.animationId);
                this.animationId = null;
            }
            this.draw();
        } else {
            this.gameLoop();
        }
    }

    useBomb() {
        if (this.player.useBomb()) {
            const destroyedCount = this.enemyManager.clearAll();
            const bonusScore = destroyedCount * 50;
            this.player.addScore(bonusScore);
        }
    }

    resetGame() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }

        this.player.reset();
        this.bulletManager.clear();
        this.enemyManager.clear();
        this.powerUpManager.clear();

        this.currentFrame = 0;
        this.isPaused = false;
        this.isGameOver = false;

        this.gameLoop();
    }

    gameLoop() {
        if (this.isPaused || this.isGameOver) {
            return;
        }

        this.animationId = requestAnimationFrame(() => this.gameLoop());

        this.update();
        this.draw();

        this.currentFrame++;
    }

    update() {
        this.player.update(this.keys, this.currentFrame);

        this.bulletManager.fire(
            this.player.getCenterX(),
            this.player.y,
            false,
            this.currentFrame
        );
        this.bulletManager.update();

        this.enemyManager.spawnEnemy(this.currentFrame);
        const escaped = this.enemyManager.update(this.player.getCenterX());
        
        if (escaped > 0) {
            for (let i = 0; i < escaped; i++) {
                this.player.takeDamage();
            }
        }

        this.powerUpManager.update();

        Collision.checkAllCollisions(
            this.bulletManager,
            this.enemyManager,
            this.player,
            this.powerUpManager
        );

        if (this.player.lives <= 0) {
            this.isGameOver = true;
            if (this.animationId) {
                cancelAnimationFrame(this.animationId);
                this.animationId = null;
            }
            this.draw();
        }
    }

    draw() {
        this.ctx.save();

        this.ctx.scale(1 / this.scaleX, 1 / this.scaleY);

        this.ctx.fillStyle = '#0a0a20';
        this.ctx.fillRect(0, 0, this.LOGICAL_WIDTH, this.LOGICAL_HEIGHT);

        this.drawStars();

        this.bulletManager.draw(this.ctx);
        this.enemyManager.draw(this.ctx);
        this.powerUpManager.draw(this.ctx);
        this.player.draw(this.ctx, this.currentFrame);

        this.ui.draw(
            this.ctx,
            this.player,
            this.bulletManager,
            this.enemyManager,
            this.isPaused
        );

        if (this.isGameOver) {
            this.ui.drawGameOverScreen(
                this.ctx,
                this.player.score,
                this.enemyManager.getWave()
            );
        }

        this.ctx.restore();
    }

    drawStars() {
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.5)';
        
        for (let i = 0; i < 50; i++) {
            const x = (i * 137 + this.currentFrame * 0.5) % this.LOGICAL_WIDTH;
            const y = (i * 251 + this.currentFrame * 0.3) % this.LOGICAL_HEIGHT;
            const size = (i % 3) + 1;
            
            this.ctx.fillRect(x, y, size, size);
        }
    }

    start() {
        this.gameLoop();
    }
}

const game = new Game();
game.start();
