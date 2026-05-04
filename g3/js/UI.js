export class UI {
    constructor(canvasWidth, canvasHeight) {
        this.canvasWidth = canvasWidth;
        this.canvasHeight = canvasHeight;
    }

    draw(ctx, player, bulletManager, enemyManager, isPaused) {
        this.drawHUD(ctx, player, bulletManager, enemyManager);
        
        if (isPaused) {
            this.drawPauseScreen(ctx);
        }
    }

    drawHUD(ctx, player, bulletManager, enemyManager) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.fillRect(0, 0, this.canvasWidth, 40);

        ctx.fillStyle = '#ffffff';
        ctx.font = '16px Arial';
        ctx.textAlign = 'left';

        ctx.fillText(`分数: ${player.score}`, 20, 26);

        ctx.fillStyle = '#ff4444';
        ctx.fillText(`生命: `, 180, 26);
        
        for (let i = 0; i < player.lives; i++) {
            this.drawHeart(ctx, 240 + i * 25, 18);
        }

        ctx.fillStyle = '#ff8800';
        ctx.fillText(`炸弹: `, 350, 26);
        ctx.fillStyle = '#ff8800';
        for (let i = 0; i < player.bombs; i++) {
            this.drawBombIcon(ctx, 420 + i * 25, 18);
        }

        ctx.fillStyle = '#44aaff';
        ctx.fillText(`子弹: ${bulletManager.getActiveCount()}/${bulletManager.getMaxBullets()}`, 520, 26);

        ctx.fillStyle = '#44ff44';
        ctx.fillText(`波次: ${enemyManager.getWave()}`, 700, 26);

        ctx.fillStyle = '#aaaaaa';
        ctx.font = '12px Arial';
        ctx.fillText('A/D或方向键移动 | 空格单发 | X炸弹 | P暂停 | R重置', this.canvasWidth / 2 - 200, this.canvasHeight - 15);
    }

    drawHeart(ctx, x, y) {
        ctx.fillStyle = '#ff4444';
        ctx.beginPath();
        ctx.moveTo(x + 8, y + 5);
        ctx.bezierCurveTo(x + 8, y + 2, x + 4, y + 2, x + 4, y + 5);
        ctx.bezierCurveTo(x + 4, y + 2, x, y + 2, x, y + 5);
        ctx.bezierCurveTo(x, y + 8, x + 4, y + 11, x + 8, y + 14);
        ctx.bezierCurveTo(x + 12, y + 11, x + 16, y + 8, x + 16, y + 5);
        ctx.bezierCurveTo(x + 16, y + 2, x + 12, y + 2, x + 12, y + 5);
        ctx.bezierCurveTo(x + 12, y + 2, x + 8, y + 2, x + 8, y + 5);
        ctx.fill();
    }

    drawBombIcon(ctx, x, y) {
        ctx.fillStyle = '#ff8800';
        ctx.beginPath();
        ctx.arc(x + 8, y + 8, 8, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = '#ffaa00';
        ctx.beginPath();
        ctx.arc(x + 6, y + 6, 3, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = '#888888';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(x + 8, y);
        ctx.lineTo(x + 8, y - 3);
        ctx.stroke();
    }

    drawPauseScreen(ctx) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, this.canvasWidth, this.canvasHeight);

        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 48px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('游戏暂停', this.canvasWidth / 2, this.canvasHeight / 2 - 20);

        ctx.font = '24px Arial';
        ctx.fillText('按 P 继续游戏', this.canvasWidth / 2, this.canvasHeight / 2 + 30);
    }

    drawGameOverScreen(ctx, finalScore, finalWave) {
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(0, 0, this.canvasWidth, this.canvasHeight);

        ctx.fillStyle = '#ff4444';
        ctx.font = 'bold 64px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('游戏结束', this.canvasWidth / 2, this.canvasHeight / 2 - 60);

        ctx.fillStyle = '#ffffff';
        ctx.font = '28px Arial';
        ctx.fillText(`最终分数: ${finalScore}`, this.canvasWidth / 2, this.canvasHeight / 2);
        ctx.fillText(`到达波次: ${finalWave}`, this.canvasWidth / 2, this.canvasHeight / 2 + 40);

        ctx.font = '20px Arial';
        ctx.fillStyle = '#aaaaaa';
        ctx.fillText('点击画布或按 R 键重新开始', this.canvasWidth / 2, this.canvasHeight / 2 + 100);
    }
}
