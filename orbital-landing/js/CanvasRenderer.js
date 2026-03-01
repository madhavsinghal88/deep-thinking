/**
 * CanvasRenderer.js
 * Dual canvas system with multi-layer rotating orbital rings
 * Tech/circuit style symbols rotating in mandala formation
 */

export class CanvasRenderer {
  constructor(orbitalCanvas, ambientCanvas) {
    this.orbitalCanvas = orbitalCanvas;
    this.ambientCanvas = ambientCanvas;
    this.orbitalCtx = orbitalCanvas.getContext('2d');
    this.ambientCtx = ambientCanvas.getContext('2d');
    
    // Animation state
    this.rotation = 0;
    this.scrollProgress = 0;
    this.glowIntensity = 1;
    this.logoScale = 1;
    
    // Ring configuration
    this.rings = this.createRingConfig();
    
    // Tech symbols for circuit/data aesthetic
    this.outerSymbols = ['◇', '⬡', '⬢', '◈', '▣', '◎', '⊕', '⊗', '⌬', '⏣', '⏢', '⎔'];
    this.middleSymbols = ['⟁', '⟐', '⟊', '⫯', '⫰', '⧉', '⧈', '⧇', '◬', '⬡', '⎈', '⏚'];
    this.innerSymbols = ['◉', '◎', '●', '○', '◌', '◍'];
    
    // Colors
    this.colors = {
      cyan: '#00d4ff',
      purple: '#a855f7',
      blue: '#3b82f6',
      pink: '#ec4899',
      white: '#ffffff'
    };
    
    // Canvas dimensions
    this.width = 0;
    this.height = 0;
    this.centerX = 0;
    this.centerY = 0;
    this.baseRadius = 0;
    
    // Bind methods
    this.resize = this.resize.bind(this);
    this.render = this.render.bind(this);
    
    // Initial setup
    this.resize();
  }
  
  createRingConfig() {
    return {
      outer: {
        radiusRatio: 0.38,
        symbolCount: 12,
        rotationSpeed: 0.0003,
        direction: 1, // clockwise
        fontSize: 24,
        opacity: 0.8
      },
      middle: {
        radiusRatio: 0.28,
        symbolCount: 10,
        rotationSpeed: 0.0005,
        direction: -1, // counter-clockwise
        fontSize: 20,
        opacity: 0.9
      },
      inner: {
        radiusRatio: 0.18,
        symbolCount: 8,
        rotationSpeed: 0.0002,
        direction: 1,
        fontSize: 16,
        opacity: 0.7
      },
      petals: {
        radiusRatio: 0.22,
        petalCount: 6,
        rotationSpeed: 0.0001,
        direction: -1
      }
    };
  }
  
  resize() {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.orbitalCanvas.parentElement.getBoundingClientRect();
    
    this.width = rect.width;
    this.height = rect.height;
    this.centerX = this.width / 2;
    this.centerY = this.height / 2;
    
    // Base radius scales with viewport, ensuring content never crops
    this.baseRadius = Math.min(this.width, this.height) * 0.42;
    
    // Set canvas dimensions with DPR for crisp rendering
    [this.orbitalCanvas, this.ambientCanvas].forEach(canvas => {
      canvas.width = this.width * dpr;
      canvas.height = this.height * dpr;
      canvas.style.width = `${this.width}px`;
      canvas.style.height = `${this.height}px`;
      canvas.getContext('2d').scale(dpr, dpr);
    });
  }
  
  setScrollProgress(progress) {
    this.scrollProgress = Math.max(0, Math.min(1, progress));
    this.glowIntensity = 1 + this.scrollProgress * 0.5;
    this.logoScale = 1 + Math.sin(this.scrollProgress * Math.PI) * 0.1;
  }
  
  render(deltaTime = 16) {
    // Update rotation based on time and scroll
    const scrollBoost = 1 + this.scrollProgress * 2;
    this.rotation += deltaTime * 0.001 * scrollBoost;
    
    // Clear canvases
    this.orbitalCtx.clearRect(0, 0, this.width, this.height);
    this.ambientCtx.clearRect(0, 0, this.width, this.height);
    
    // Draw to orbital canvas (sharp)
    this.drawBackground(this.orbitalCtx);
    this.drawOuterRing(this.orbitalCtx);
    this.drawMiddleRing(this.orbitalCtx);
    this.drawGlowingPetals(this.orbitalCtx);
    this.drawInnerRing(this.orbitalCtx);
    this.drawCenterGlow(this.orbitalCtx);
    this.drawOrbitalLines(this.orbitalCtx);
    this.drawDataParticles(this.orbitalCtx);
    
    // Copy to ambient canvas (will be blurred via CSS)
    this.ambientCtx.drawImage(this.orbitalCanvas, 0, 0, this.width, this.height);
  }
  
  drawBackground(ctx) {
    // Subtle radial gradient background
    const gradient = ctx.createRadialGradient(
      this.centerX, this.centerY, 0,
      this.centerX, this.centerY, this.baseRadius * 1.5
    );
    gradient.addColorStop(0, 'rgba(0, 20, 40, 0.3)');
    gradient.addColorStop(0.5, 'rgba(0, 10, 20, 0.2)');
    gradient.addColorStop(1, 'transparent');
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, this.width, this.height);
  }
  
  drawOuterRing(ctx) {
    const config = this.rings.outer;
    const radius = this.baseRadius * config.radiusRatio;
    const angle = this.rotation * config.rotationSpeed * config.direction * 1000;
    
    ctx.save();
    ctx.translate(this.centerX, this.centerY);
    ctx.rotate(angle);
    
    // Draw ring circle
    ctx.strokeStyle = `rgba(0, 212, 255, ${0.2 * this.glowIntensity})`;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI * 2);
    ctx.stroke();
    
    // Draw symbols
    const symbolCount = config.symbolCount;
    const fontSize = config.fontSize * (this.baseRadius / 200);
    
    ctx.font = `${fontSize}px Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    for (let i = 0; i < symbolCount; i++) {
      const symbolAngle = (i / symbolCount) * Math.PI * 2;
      const x = Math.cos(symbolAngle) * radius;
      const y = Math.sin(symbolAngle) * radius;
      
      // Gradient color based on position
      const hue = (i / symbolCount) * 60 + 180; // cyan to blue range
      ctx.fillStyle = `hsla(${hue}, 100%, 60%, ${config.opacity * this.glowIntensity})`;
      
      // Add glow effect
      ctx.shadowColor = this.colors.cyan;
      ctx.shadowBlur = 10 * this.glowIntensity;
      
      ctx.fillText(this.outerSymbols[i % this.outerSymbols.length], x, y);
    }
    
    ctx.restore();
  }
  
  drawMiddleRing(ctx) {
    const config = this.rings.middle;
    const radius = this.baseRadius * config.radiusRatio;
    const angle = this.rotation * config.rotationSpeed * config.direction * 1000;
    
    ctx.save();
    ctx.translate(this.centerX, this.centerY);
    ctx.rotate(angle);
    
    // Draw ring circle
    ctx.strokeStyle = `rgba(168, 85, 247, ${0.25 * this.glowIntensity})`;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(0, 0, radius, 0, Math.PI * 2);
    ctx.stroke();
    
    // Draw symbols
    const symbolCount = config.symbolCount;
    const fontSize = config.fontSize * (this.baseRadius / 200);
    
    ctx.font = `${fontSize}px Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    for (let i = 0; i < symbolCount; i++) {
      const symbolAngle = (i / symbolCount) * Math.PI * 2;
      const x = Math.cos(symbolAngle) * radius;
      const y = Math.sin(symbolAngle) * radius;
      
      const hue = (i / symbolCount) * 40 + 270; // purple range
      ctx.fillStyle = `hsla(${hue}, 80%, 65%, ${config.opacity * this.glowIntensity})`;
      
      ctx.shadowColor = this.colors.purple;
      ctx.shadowBlur = 8 * this.glowIntensity;
      
      ctx.fillText(this.middleSymbols[i % this.middleSymbols.length], x, y);
    }
    
    ctx.restore();
  }
  
  drawInnerRing(ctx) {
    const config = this.rings.inner;
    const radius = this.baseRadius * config.radiusRatio;
    const angle = this.rotation * config.rotationSpeed * config.direction * 1000;
    
    ctx.save();
    ctx.translate(this.centerX, this.centerY);
    ctx.rotate(angle);
    
    // Draw symbols
    const symbolCount = config.symbolCount;
    const fontSize = config.fontSize * (this.baseRadius / 200);
    
    ctx.font = `${fontSize}px Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    for (let i = 0; i < symbolCount; i++) {
      const symbolAngle = (i / symbolCount) * Math.PI * 2;
      const x = Math.cos(symbolAngle) * radius;
      const y = Math.sin(symbolAngle) * radius;
      
      ctx.fillStyle = `rgba(59, 130, 246, ${config.opacity * this.glowIntensity})`;
      ctx.shadowColor = this.colors.blue;
      ctx.shadowBlur = 6 * this.glowIntensity;
      
      ctx.fillText(this.innerSymbols[i % this.innerSymbols.length], x, y);
    }
    
    ctx.restore();
  }
  
  drawGlowingPetals(ctx) {
    const config = this.rings.petals;
    const radius = this.baseRadius * config.radiusRatio;
    const angle = this.rotation * config.rotationSpeed * config.direction * 1000;
    
    ctx.save();
    ctx.translate(this.centerX, this.centerY);
    ctx.rotate(angle);
    
    const petalCount = config.petalCount;
    
    for (let i = 0; i < petalCount; i++) {
      const petalAngle = (i / petalCount) * Math.PI * 2;
      
      ctx.save();
      ctx.rotate(petalAngle);
      
      // Create petal shape
      const gradient = ctx.createRadialGradient(0, -radius * 0.5, 0, 0, -radius * 0.5, radius * 0.4);
      gradient.addColorStop(0, `rgba(236, 72, 153, ${0.4 * this.glowIntensity})`);
      gradient.addColorStop(0.5, `rgba(168, 85, 247, ${0.2 * this.glowIntensity})`);
      gradient.addColorStop(1, 'transparent');
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.ellipse(0, -radius * 0.5, radius * 0.15, radius * 0.35, 0, 0, Math.PI * 2);
      ctx.fill();
      
      ctx.restore();
    }
    
    ctx.restore();
  }
  
  drawCenterGlow(ctx) {
    const radius = this.baseRadius * 0.12 * this.logoScale;
    
    // Multi-layer glow
    const layers = [
      { radius: radius * 2.5, color: 'rgba(0, 212, 255, 0.05)' },
      { radius: radius * 2, color: 'rgba(0, 212, 255, 0.1)' },
      { radius: radius * 1.5, color: 'rgba(168, 85, 247, 0.15)' },
      { radius: radius, color: 'rgba(255, 255, 255, 0.2)' }
    ];
    
    layers.forEach(layer => {
      const gradient = ctx.createRadialGradient(
        this.centerX, this.centerY, 0,
        this.centerX, this.centerY, layer.radius * this.glowIntensity
      );
      gradient.addColorStop(0, layer.color);
      gradient.addColorStop(1, 'transparent');
      
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.arc(this.centerX, this.centerY, layer.radius * this.glowIntensity, 0, Math.PI * 2);
      ctx.fill();
    });
    
    // Center dot
    ctx.fillStyle = `rgba(255, 255, 255, ${0.8 * this.glowIntensity})`;
    ctx.shadowColor = this.colors.white;
    ctx.shadowBlur = 20 * this.glowIntensity;
    ctx.beginPath();
    ctx.arc(this.centerX, this.centerY, radius * 0.3, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;
  }
  
  drawOrbitalLines(ctx) {
    // Subtle connecting lines between rings
    const innerRadius = this.baseRadius * 0.1;
    const outerRadius = this.baseRadius * 0.4;
    
    ctx.save();
    ctx.translate(this.centerX, this.centerY);
    
    for (let i = 0; i < 6; i++) {
      const angle = (i / 6) * Math.PI * 2 + this.rotation * 0.0002 * 1000;
      
      const gradient = ctx.createLinearGradient(
        Math.cos(angle) * innerRadius,
        Math.sin(angle) * innerRadius,
        Math.cos(angle) * outerRadius,
        Math.sin(angle) * outerRadius
      );
      gradient.addColorStop(0, 'transparent');
      gradient.addColorStop(0.3, `rgba(0, 212, 255, ${0.1 * this.glowIntensity})`);
      gradient.addColorStop(0.7, `rgba(168, 85, 247, ${0.1 * this.glowIntensity})`);
      gradient.addColorStop(1, 'transparent');
      
      ctx.strokeStyle = gradient;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(Math.cos(angle) * innerRadius, Math.sin(angle) * innerRadius);
      ctx.lineTo(Math.cos(angle) * outerRadius, Math.sin(angle) * outerRadius);
      ctx.stroke();
    }
    
    ctx.restore();
  }
  
  drawDataParticles(ctx) {
    // Floating data particles around the orbital system
    const particleCount = 20;
    const time = this.rotation * 500;
    
    ctx.save();
    
    for (let i = 0; i < particleCount; i++) {
      const angle = (i / particleCount) * Math.PI * 2 + time * 0.001 * (i % 2 === 0 ? 1 : -1);
      const radiusVariation = Math.sin(time * 0.002 + i) * 20;
      const radius = this.baseRadius * (0.15 + (i / particleCount) * 0.3) + radiusVariation;
      
      const x = this.centerX + Math.cos(angle) * radius;
      const y = this.centerY + Math.sin(angle) * radius;
      
      const size = 1 + Math.sin(time * 0.003 + i * 0.5) * 0.5;
      const opacity = 0.3 + Math.sin(time * 0.002 + i) * 0.2;
      
      const colors = [this.colors.cyan, this.colors.purple, this.colors.blue];
      ctx.fillStyle = colors[i % colors.length].replace(')', `, ${opacity * this.glowIntensity})`).replace('rgb', 'rgba');
      
      ctx.beginPath();
      ctx.arc(x, y, size * 2, 0, Math.PI * 2);
      ctx.fill();
    }
    
    ctx.restore();
  }
  
  destroy() {
    // Cleanup if needed
    this.orbitalCtx = null;
    this.ambientCtx = null;
  }
}
