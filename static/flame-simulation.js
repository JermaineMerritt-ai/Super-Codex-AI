/**
 * Advanced Flame Simulation for Codex Dominion
 * Creates a realistic, interactive flame effect
 */

class FlameSimulation {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.canvas = document.createElement('canvas');
        this.ctx = this.canvas.getContext('2d');
        
        this.options = {
            flameCount: options.flameCount || 50,
            baseSize: options.baseSize || 3,
            maxHeight: options.maxHeight || 100,
            windStrength: options.windStrength || 0.02,
            intensity: options.intensity || 1.0,
            sovereignty: options.sovereignty || 'eternal',
            ...options
        };
        
        this.flames = [];
        this.particles = [];
        this.time = 0;
        this.running = false;
        
        this.setupCanvas();
        this.initializeFlames();
    }
    
    setupCanvas() {
        this.canvas.style.position = 'absolute';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.pointerEvents = 'none';
        this.canvas.style.zIndex = '1';
        
        this.resizeCanvas();
        this.container.appendChild(this.canvas);
        
        window.addEventListener('resize', () => this.resizeCanvas());
    }
    
    resizeCanvas() {
        const rect = this.container.getBoundingClientRect();
        this.canvas.width = rect.width;
        this.canvas.height = rect.height;
    }
    
    initializeFlames() {
        this.flames = [];
        for (let i = 0; i < this.options.flameCount; i++) {
            this.flames.push(this.createFlameParticle());
        }
    }
    
    createFlameParticle() {
        return {
            x: Math.random() * this.canvas.width,
            y: this.canvas.height,
            vx: (Math.random() - 0.5) * 2,
            vy: -Math.random() * 5 - 2,
            life: 1.0,
            maxLife: Math.random() * 60 + 30,
            size: this.options.baseSize + Math.random() * 4,
            hue: 35 + Math.random() * 25, // Gold to orange range
            brightness: 0.8 + Math.random() * 0.2,
            sovereignty: this.options.sovereignty === 'eternal' ? Math.random() > 0.1 : Math.random() > 0.5
        };
    }
    
    updateFlame(flame) {
        // Wind and turbulence
        const wind = Math.sin(this.time * 0.01 + flame.x * 0.001) * this.options.windStrength;
        flame.vx += wind;
        flame.vx *= 0.98; // Air resistance
        
        // Upward movement with flickering
        flame.vy += Math.sin(this.time * 0.1 + flame.x * 0.01) * 0.1;
        
        // Position update
        flame.x += flame.vx;
        flame.y += flame.vy;
        
        // Life cycle
        flame.life--;
        if (flame.life <= 0) {
            // Respawn from bottom
            Object.assign(flame, this.createFlameParticle());
        }
        
        // Color evolution based on life and sovereignty
        const lifeRatio = flame.life / flame.maxLife;
        if (flame.sovereignty) {
            // Sovereign flames burn golden longer
            flame.hue = 45 - (lifeRatio * 10); // Gold to deep gold
            flame.brightness = 0.9 + lifeRatio * 0.1;
        } else {
            // Regular flames fade to red
            flame.hue = 35 - (1 - lifeRatio) * 15; // Gold to red
            flame.brightness = 0.5 + lifeRatio * 0.4;
        }
    }
    
    drawFlame(flame) {
        const lifeRatio = flame.life / flame.maxLife;
        const alpha = lifeRatio * this.options.intensity;
        const size = flame.size * (0.5 + lifeRatio * 0.5);
        
        // Create gradient for flame effect
        const gradient = this.ctx.createRadialGradient(
            flame.x, flame.y, 0,
            flame.x, flame.y, size * 2
        );
        
        const baseColor = `hsla(${flame.hue}, 100%, ${flame.brightness * 100}%, ${alpha})`;
        const edgeColor = `hsla(${flame.hue + 10}, 100%, ${flame.brightness * 80}%, ${alpha * 0.3})`;
        
        gradient.addColorStop(0, baseColor);
        gradient.addColorStop(1, edgeColor);
        
        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(flame.x, flame.y, size, 0, Math.PI * 2);
        this.ctx.fill();
        
        // Add sovereignty glow
        if (flame.sovereignty && lifeRatio > 0.7) {
            this.ctx.shadowColor = '#d4af37';
            this.ctx.shadowBlur = 10;
            this.ctx.fillStyle = `hsla(45, 100%, 85%, ${alpha * 0.3})`;
            this.ctx.fill();
            this.ctx.shadowBlur = 0;
        }
    }
    
    addSparks(count = 10) {
        for (let i = 0; i < count; i++) {
            this.flames.push({
                ...this.createFlameParticle(),
                x: this.canvas.width * 0.5 + (Math.random() - 0.5) * 100,
                y: this.canvas.height * 0.8,
                vy: -Math.random() * 10 - 5,
                size: this.options.baseSize * 1.5,
                sovereignty: true,
                maxLife: 20
            });
        }
    }
    
    animate() {
        if (!this.running) return;
        
        // Clear canvas with slight trail effect for ethereal look
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.time++;
        
        // Update and draw all flames
        this.flames.forEach(flame => {
            this.updateFlame(flame);
            this.drawFlame(flame);
        });
        
        // Add random sovereignty sparks
        if (Math.random() < 0.02) {
            this.addSparks(Math.floor(Math.random() * 3) + 1);
        }
        
        requestAnimationFrame(() => this.animate());
    }
    
    start() {
        this.running = true;
        this.animate();
    }
    
    stop() {
        this.running = false;
    }
    
    setSovereignty(level) {
        this.options.sovereignty = level;
        this.options.intensity = level === 'eternal' ? 1.2 : level === 'sovereign' ? 1.0 : 0.8;
    }
    
    increasePower() {
        this.addSparks(20);
        this.options.intensity = Math.min(this.options.intensity * 1.5, 2.0);
        setTimeout(() => {
            this.options.intensity = Math.max(this.options.intensity * 0.8, 1.0);
        }, 2000);
    }
}

// Ceremonial Text Animation
class CeremonialTextAnimator {
    constructor() {
        this.effects = new Map();
    }
    
    addSovereignGlow(elementId) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        element.style.transition = 'all 0.5s ease-in-out';
        element.addEventListener('mouseenter', () => {
            element.style.textShadow = '0 0 20px #d4af37, 0 0 40px #b8860b, 0 0 60px #f4e190';
            element.style.transform = 'scale(1.05)';
        });
        
        element.addEventListener('mouseleave', () => {
            element.style.textShadow = '0 0 10px #d4af37';
            element.style.transform = 'scale(1)';
        });
    }
    
    typewriter(elementId, text, speed = 50) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        element.textContent = '';
        let i = 0;
        
        const type = () => {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        };
        
        type();
    }
    
    ceremonialReveal(elementId, delay = 0) {
        const element = document.getElementById(elementId);
        if (!element) return;
        
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'all 0.8s ease-out';
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, delay);
    }
}

// Dominion Status Monitor
class DominionStatusMonitor {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.status = {
            flame: 'sovereign',
            lineage: 'unbroken',
            governance: 'operational',
            ceremonies: 'active',
            custodians: 'vigilant'
        };
        
        this.setupMonitor();
        this.startMonitoring();
    }
    
    setupMonitor() {
        this.container.innerHTML = `
            <div class="status-grid">
                <div class="status-item" id="flame-status">
                    <span class="status-icon">🔥</span>
                    <span class="status-label">Flame</span>
                    <span class="status-value" id="flame-value">Sovereign</span>
                </div>
                <div class="status-item" id="lineage-status">
                    <span class="status-icon">⚡</span>
                    <span class="status-label">Lineage</span>
                    <span class="status-value" id="lineage-value">Unbroken</span>
                </div>
                <div class="status-item" id="governance-status">
                    <span class="status-icon">🏛️</span>
                    <span class="status-label">Governance</span>
                    <span class="status-value" id="governance-value">Operational</span>
                </div>
                <div class="status-item" id="ceremonies-status">
                    <span class="status-icon">📜</span>
                    <span class="status-label">Ceremonies</span>
                    <span class="status-value" id="ceremonies-value">Active</span>
                </div>
                <div class="status-item" id="custodians-status">
                    <span class="status-icon">👁️</span>
                    <span class="status-label">Custodians</span>
                    <span class="status-value" id="custodians-value">Vigilant</span>
                </div>
            </div>
        `;
    }
    
    async updateStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            // Update flame status based on server health
            const flameStatus = data.dominion_status === 'sovereign' ? 'eternal' : 'sovereign';
            this.updateStatusItem('flame', flameStatus, flameStatus === 'eternal' ? '🔥' : '✨');
            
            // Check ceremonial endpoints
            const ceremonies = await this.checkCeremonialEndpoints();
            this.updateStatusItem('ceremonies', ceremonies ? 'active' : 'dormant', ceremonies ? '📜' : '📋');
            
            // Update governance based on health checks
            const governance = data.database === 'connected' ? 'operational' : 'maintenance';
            this.updateStatusItem('governance', governance, governance === 'operational' ? '🏛️' : '🔧');
            
        } catch (error) {
            console.warn('Status update failed:', error);
            this.updateStatusItem('flame', 'flickering', '🕯️');
        }
    }
    
    async checkCeremonialEndpoints() {
        try {
            const response = await fetch('/dominion/scroll/welcome');
            return response.ok;
        } catch {
            return false;
        }
    }
    
    updateStatusItem(type, value, icon) {
        const valueElement = document.getElementById(`${type}-value`);
        const iconElement = document.querySelector(`#${type}-status .status-icon`);
        
        if (valueElement) {
            valueElement.textContent = value.charAt(0).toUpperCase() + value.slice(1);
            valueElement.className = `status-value status-${value.toLowerCase()}`;
        }
        
        if (iconElement) {
            iconElement.textContent = icon;
        }
        
        this.status[type] = value;
    }
    
    startMonitoring() {
        this.updateStatus();
        setInterval(() => this.updateStatus(), 30000); // Every 30 seconds
    }
    
    getSovereigntyLevel() {
        const sovereignCount = Object.values(this.status).filter(s => 
            s === 'sovereign' || s === 'eternal' || s === 'operational' || s === 'active' || s === 'unbroken' || s === 'vigilant'
        ).length;
        
        if (sovereignCount >= 5) return 'eternal';
        if (sovereignCount >= 4) return 'sovereign';
        if (sovereignCount >= 3) return 'strong';
        return 'flickering';
    }
}

// Export for global use
window.FlameSimulation = FlameSimulation;
window.CeremonialTextAnimator = CeremonialTextAnimator;
window.DominionStatusMonitor = DominionStatusMonitor;