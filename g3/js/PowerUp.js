export class PowerUp {
    constructor(x, y, canvasHeight) {
        this.x = x;
        this.y = y;
        this.width = 25;
        this.height = 25;
        this.speed = 2;
        this.canvasHeight = canvasHeight;
        this.active = true;
        this.type = 'bomb';
        this.rotation = 0;
    }

    update() {
        this.y += this.speed;
        this.rotation += 0.05;

        if (this.y > this.canvasHeight) {
            this.active = false;
        }
    }

    draw(ctx) {
        ctx.save();
        ctx.translate(this.x + this.width / 2, this.y + this.height / 2);
        ctx.rotate(this.rotation);

        ctx.fillStyle = '#ff8800';
        ctx.beginPath();
        ctx.arc(0, 0, this.width / 2, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffaa00';
        ctx.beginPath();
        ctx.arc(-3, -3, this.width / 3, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#000';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('B', 0, 0);

        ctx.restore();
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

    getType() {
        return this.type;
    }
}

export class PowerUpManager {
    constructor(canvasWidth, canvasHeight) {
        this.powerUps = [];
        this.canvasWidth = canvasWidth;
        this.canvasHeight = canvasHeight;
        this.dropChance = 0.2;
    }

    spawnPowerUp(x, y) {
        if (Math.random() < this.dropChance) {
            const powerUp = new PowerUp(x, y, this.canvasHeight);
            this.powerUps.push(powerUp);
        }
    }

    update() {
        this.powerUps = this.powerUps.filter(powerUp => {
            powerUp.update();
            return powerUp.active;
        });
    }

    draw(ctx) {
        this.powerUps.forEach(powerUp => powerUp.draw(ctx));
    }

    clear() {
        this.powerUps = [];
    }
}
