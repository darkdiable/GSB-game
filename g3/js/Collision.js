export class Collision {
    static checkRectCollision(rect1, rect2) {
        return (
            rect1.x < rect2.x + rect2.width &&
            rect1.x + rect1.width > rect2.x &&
            rect1.y < rect2.y + rect2.height &&
            rect1.y + rect1.height > rect2.y
        );
    }

    static checkBulletEnemyCollision(bulletManager, enemyManager, player, powerUpManager) {
        let scoreGained = 0;

        bulletManager.bullets = bulletManager.bullets.filter(bullet => {
            const bulletBounds = bullet.getBounds();
            let bulletHit = false;

            enemyManager.enemies = enemyManager.enemies.filter(enemy => {
                if (bulletHit) return enemy.active;

                const enemyBounds = enemy.getBounds();
                if (this.checkRectCollision(bulletBounds, enemyBounds)) {
                    bulletHit = true;
                    bullet.deactivate();
                    scoreGained += enemy.getScore();
                    
                    if (Math.random() < powerUpManager.dropChance) {
                        powerUpManager.spawnPowerUp(
                            enemyBounds.x + enemyBounds.width / 2 - 12.5,
                            enemyBounds.y
                        );
                    }

                    return false;
                }
                return enemy.active;
            });

            return bullet.active;
        });

        if (scoreGained > 0) {
            player.addScore(scoreGained);
        }

        return scoreGained;
    }

    static checkPlayerEnemyCollision(player, enemyManager) {
        let playerHit = false;

        if (player.isInvincible) {
            return playerHit;
        }

        const playerBounds = player.getBounds();

        enemyManager.enemies = enemyManager.enemies.filter(enemy => {
            const enemyBounds = enemy.getBounds();
            if (this.checkRectCollision(playerBounds, enemyBounds)) {
                playerHit = true;
                return false;
            }
            return enemy.active;
        });

        return playerHit;
    }

    static checkPlayerPowerUpCollision(player, powerUpManager) {
        let powerUpCollected = false;

        const playerBounds = player.getBounds();

        powerUpManager.powerUps = powerUpManager.powerUps.filter(powerUp => {
            const powerUpBounds = powerUp.getBounds();
            if (this.checkRectCollision(playerBounds, powerUpBounds)) {
                if (powerUp.getType() === 'bomb') {
                    player.addBomb();
                }
                powerUpCollected = true;
                return false;
            }
            return powerUp.active;
        });

        return powerUpCollected;
    }

    static checkAllCollisions(bulletManager, enemyManager, player, powerUpManager) {
        this.checkBulletEnemyCollision(bulletManager, enemyManager, player, powerUpManager);
        
        const playerHit = this.checkPlayerEnemyCollision(player, enemyManager);
        if (playerHit) {
            player.takeDamage();
        }

        this.checkPlayerPowerUpCollision(player, powerUpManager);
    }
}
