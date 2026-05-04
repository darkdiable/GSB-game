export class Bullet {
    constructor(x, y, canvasHeight) {
        this.x = x;
        this.y = y;
        this.width = 4;
        this.height = 12;
        this.speed = 8;
        this.canvasHeight = canvasHeight;
        this.active = true;
    }

    update() {
        this.y -= this.speed;
        if (this.y + this.height < 0) {
            this.active = false;
        }
    }

    draw(ctx) {
        ctx.fillStyle = '#ffff00';
        ctx.fillRect(this.x - this.width / 2, this.y, this.width, this.height);

        ctx.fillStyle = '#ffaa00';
        ctx.fillRect(this.x - this.width / 2 - 1, this.y + this.height - 3, this.width + 2, 3);
    }

    getBounds() {
        return {
            x: this.x - this.width / 2,
            y: this.y,
            width: this.width,
            height: this.height
        };
    }

    deactivate() {
        this.active = false;
    }
}

export class BulletManager {
    constructor(canvasWidth, canvasHeight) {
        this.bullets = [];
        this.canvasWidth = canvasWidth;
        this.canvasHeight = canvasHeight;
        this.maxBullets = 10;
        this.framesPerBullet = 6;
        this.lastBulletFrame = 0;
    }

    fire(playerX, playerY, force = false, currentFrame = 0) {
        if (this.bullets.length >= this.maxBullets) {
            return false;
        }

        if (force) {
            const bullet = new Bullet(playerX, playerY, this.canvasHeight);
            this.bullets.push(bullet);
            return true;
        }

        if (currentFrame - this.lastBulletFrame >= this.framesPerBullet) {
            const bullet = new Bullet(playerX, playerY, this.canvasHeight);
            this.bullets.push(bullet);
            this.lastBulletFrame = currentFrame;
            return true;
        }

        return false;
    }

    update() {
        this.bullets = this.bullets.filter(bullet => {
            bullet.update();
            return bullet.active;
        });
    }

    draw(ctx) {
        this.bullets.forEach(bullet => bullet.draw(ctx));
    }

    getActiveCount() {
        return this.bullets.length;
    }

    getMaxBullets() {
        return this.maxBullets;
    }

    clear() {
        this.bullets = [];
        this.lastBulletFrame = 0;
    }
}
