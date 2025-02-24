class Particle {
    constructor(canvas, ctx, options = {}) {
        this.canvas = canvas;
        this.ctx = ctx;
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 2 + 2; // 2-4像素
        this.baseSize = this.size;
        this.vx = (Math.random() - 0.5) * 0.5; // 随机速度
        this.vy = (Math.random() - 0.5) * 0.5;
        this.opacity = Math.random() * 0.2 + 0.2; // 20%-40%透明度
        this.connections = []; // 存储与其他粒子的连接
        this.connectionCount = 0; // 当前连接数
        this.maxConnections = 3; // 最大连接数
        this.highlighted = false; // 是否被鼠标悬停高亮
    }

    update(mouseX, mouseY, particles) {
        // 更新位置
        this.x += this.vx;
        this.y += this.vy;

        // 边界检查
        if (this.x < 0 || this.x > this.canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > this.canvas.height) this.vy *= -1;

        // 鼠标交互
        const dx = mouseX - this.x;
        const dy = mouseY - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
            // 鼠标吸引效果
            const force = (100 - distance) * 0.0005;
            this.vx += dx * force;
            this.vy += dy * force;
            this.size = this.baseSize * 1.5; // 放大效果
            this.highlighted = true;
        } else {
            this.size = this.baseSize;
            this.highlighted = false;
        }

        // 限制速度
        const maxSpeed = 2;
        const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
        if (speed > maxSpeed) {
            this.vx = (this.vx / speed) * maxSpeed;
            this.vy = (this.vy / speed) * maxSpeed;
        }

        // 更新连接
        this.updateConnections(particles);
    }

    updateConnections(particles) {
        this.connections = [];
        this.connectionCount = 0;

        for (let particle of particles) {
            if (particle === this || this.connectionCount >= this.maxConnections) break;

            const dx = particle.x - this.x;
            const dy = particle.y - this.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 150 && particle.connectionCount < particle.maxConnections) {
                this.connections.push({
                    particle: particle,
                    distance: distance
                });
                this.connectionCount++;
                particle.connectionCount++;
            }
        }
    }

    draw() {
        // 绘制连接线
        this.ctx.lineWidth = 1;
        this.connections.forEach(connection => {
            const opacity = this.highlighted ? 0.3 : 0.1;
            this.ctx.strokeStyle = `rgba(0, 163, 255, ${opacity * (1 - connection.distance / 150)})`;
            this.ctx.beginPath();
            this.ctx.moveTo(this.x, this.y);
            this.ctx.lineTo(connection.particle.x, connection.particle.y);
            this.ctx.stroke();
        });

        // 绘制粒子
        this.ctx.beginPath();
        this.ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        this.ctx.fillStyle = `rgba(0, 163, 255, ${this.highlighted ? this.opacity * 1.5 : this.opacity})`;
        this.ctx.fill();

        // 可选：添加发光效果
        if (this.highlighted) {
            this.ctx.beginPath();
            this.ctx.arc(this.x, this.y, this.size * 2, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(0, 163, 255, 0.1)`;
            this.ctx.fill();
        }
    }
}

class ParticleNetwork {
    constructor() {
        this.canvas = document.getElementById('particles');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.mouseX = 0;
        this.mouseY = 0;
        this.resizeTimeout = null;
        this.isClicked = false;
        this.clickWave = null;

        this.init();
        this.bindEvents();
    }

    init() {
        this.resizeCanvas();
        this.createParticles();
        this.animate();
    }

    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }

    createParticles() {
        const area = this.canvas.width * this.canvas.height;
        const particleCount = Math.floor(area / 10000) * 2; // 每10000平方像素2个粒子
        this.particles = [];
        
        for (let i = 0; i < particleCount; i++) {
            this.particles.push(new Particle(this.canvas, this.ctx));
        }
    }

    bindEvents() {
        window.addEventListener('resize', () => {
            clearTimeout(this.resizeTimeout);
            this.resizeTimeout = setTimeout(() => {
                this.resizeCanvas();
                this.createParticles();
            }, 250);
        });

        window.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX;
            this.mouseY = e.clientY;
        });

        this.canvas.addEventListener('click', (e) => {
            this.isClicked = true;
            this.clickWave = {
                x: e.clientX,
                y: e.clientY,
                radius: 0,
                maxRadius: 200,
                startTime: performance.now()
            };
        });
    }

    drawClickWave() {
        if (!this.clickWave) return;

        const duration = 1000; // 波纹持续时间（毫秒）
        const now = performance.now();
        const elapsed = now - this.clickWave.startTime;
        const progress = elapsed / duration;

        if (progress >= 1) {
            this.clickWave = null;
            return;
        }

        const currentRadius = this.clickWave.maxRadius * progress;
        const opacity = 1 - progress;

        this.ctx.beginPath();
        this.ctx.arc(this.clickWave.x, this.clickWave.y, currentRadius, 0, Math.PI * 2);
        this.ctx.strokeStyle = `rgba(0, 163, 255, ${opacity * 0.3})`;
        this.ctx.lineWidth = 2;
        this.ctx.stroke();
    }

    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // 重置所有粒子的连接计数
        this.particles.forEach(particle => {
            particle.connectionCount = 0;
        });

        // 更新和绘制所有粒子
        this.particles.forEach(particle => {
            particle.update(this.mouseX, this.mouseY, this.particles);
            particle.draw();
        });

        // 绘制点击波纹
        this.drawClickWave();

        requestAnimationFrame(() => this.animate());
    }
}

// 当DOM加载完成后初始化粒子系统
document.addEventListener('DOMContentLoaded', () => {
    new ParticleNetwork();
}); 