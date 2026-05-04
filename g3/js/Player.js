export class Player {
    constructor(canvasWidth, canvasHeight) {
        this.canvasWidth = canvasWidth;
        this.canvasHeight = canvasHeight;
        this.width = 40;
        this.height = 40;
        this.x = canvasWidth / 2 - this.width / 2;
        this.y = canvasHeight - this.height - 20;
        this.speed = 5;
        this.lives = 3;
        this.bombs = 3;
        this.maxBombs = 3;
        this.score = 0;
        this.isInvincible = false;
        this.invincibleFrames = 0;
        this.maxInvincibleFrames = 30;
    }

    update(keys, currentFrame) {
        if (keys.left) {
            this.x = Math.max(0, this.x - this.speed);
        }
        if (keys.right) {
            this.x = Math.min(this.canvasWidth - this.width, this.x + this.speed);
        }

        if (this.isInvincible) {
            this.invincibleFrames++;
            if (this.invincibleFrames >= this.maxInvincibleFrames) {
                this.isInvincible = false;
                this.invincibleFrames = 0;
            }
        }
    }

    draw(ctx, currentFrame) {
        if (this.isInvincible && currentFrame % 4 < 2) {
            return;
        }

        ctx.save();
        ctx.translate(this.x + this.width / 2, this.y + this.height / 2);

        ctx.fillStyle = '#00aaff';
        ctx.beginPath();
        ctx.moveTo(0, -this.height / 2);
        ctx.lineTo(-this.width / 2, this.height / 2);
        ctx.lineTo(this.width / 2, this.height / 2);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#0066cc';
        ctx.beginPath();
        ctx.moveTo(-this.width / 2 + 5, this.height / 2);
        ctx.lineTo(-this.width / 2 - 10, this.height / 2 + 15);
        ctx.lineTo(-this.width / 2 + 15, this.height / 2);
        ctx.closePath();
        ctx.fill();

        ctx.beginPath();
        ctx.moveTo(this.width / 2 - 5, this.height / 2);
        ctx.lineTo(this.width / 2 + 10, this.height / 2 + 15);
        ctx.lineTo(this.width / 2 - 15, this.height / 2);
        ctx.closePath();
        ctx.fill();

        ctx.fillStyle = '#ff6600';
        ctx.beginPath();
        ctx.moveTo(-8, this.height / 2);
        ctx.lineTo(0, this.height / 2 + 10 + Math.random() * 5);
        ctx.lineTo(8, this.height / 2);
        ctx.closePath();
        ctx.fill();

        ctx.restore();
    }

    takeDamage() {
        if (this.isInvincible) return false;

        this.lives--;
        this.isInvincible = true;
        this.invincibleFrames = 0;
        return true;
    }

    useBomb() {
        if (this.bombs > 0) {
            this.bombs--;
            return true;
        }
        return false;
    }

    addBomb() {
        if (this.bombs < this.maxBombs) {
            this.bombs++;
        }
    }

    addScore(points) {
        this.score += points;
    }

    getBounds() {
        return {
            x: this.x,
            y: this.y,
            width: this.width,
            height: this.height
        };
    }

    getCenterX() {
        return this.x + this.width / 2;
    }

    reset() {
        this.x = this.canvasWidth / 2 - this.width / 2;
        this.y = this.canvasHeight - this.height - 20;
        this.lives = 3;
        this.bombs = 3;
        this.score = 0;
        this.isInvincible = false;
        this.invincibleFrames = 0;
    }
}
