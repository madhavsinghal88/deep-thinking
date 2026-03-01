/**
 * OrbitalExperience.js
 * Main orchestrator class
 * Coordinates all modules: Canvas, Scroll, Info, Preloader
 */

import { CanvasRenderer } from './CanvasRenderer.js';
import { ScrollController } from './ScrollController.js';
import { RandomInfoGenerator } from './RandomInfoGenerator.js';
import { Preloader } from './Preloader.js';

export class OrbitalExperience {
  constructor() {
    // DOM Elements
    this.elements = {
      orbitalCanvas: document.getElementById('orbital-canvas'),
      ambientCanvas: document.getElementById('ambient-canvas'),
      hero: document.getElementById('hero'),
      heroSticky: document.querySelector('.hero__sticky'),
      heroTitle: document.querySelector('.hero__title'),
      randomInfo: document.getElementById('random-info'),
      scrollIndicator: document.querySelector('.hero__scroll-indicator'),
      preloader: document.getElementById('preloader'),
      carousel: document.getElementById('carousel')
    };
    
    // Module instances
    this.canvasRenderer = null;
    this.scrollController = null;
    this.randomInfoGenerator = null;
    this.preloader = null;
    
    // Animation state
    this.isRunning = false;
    this.lastFrameTime = 0;
    this.animationId = null;
    
    // Bind methods
    this.animate = this.animate.bind(this);
    this.handleResize = this.handleResize.bind(this);
    this.handleScrollProgress = this.handleScrollProgress.bind(this);
    
    // Initialize
    this.init();
  }
  
  async init() {
    // Initialize preloader first
    this.initPreloader();
    
    // Initialize all modules
    this.initCanvasRenderer();
    this.initScrollController();
    this.initRandomInfoGenerator();
    this.initCarousel();
    
    // Set up event listeners
    this.setupEventListeners();
    
    // Start the experience after preloader
    await this.preloader.start();
    
    // Start animation loop
    this.start();
    
    // Start info generator
    this.randomInfoGenerator.start();
  }
  
  initPreloader() {
    this.preloader = new Preloader({
      element: this.elements.preloader,
      minDisplayTime: 1500,
      onComplete: () => {
        console.log('Orbital Experience initialized');
      }
    });
  }
  
  initCanvasRenderer() {
    this.canvasRenderer = new CanvasRenderer(
      this.elements.orbitalCanvas,
      this.elements.ambientCanvas
    );
  }
  
  initScrollController() {
    this.scrollController = new ScrollController({
      heroSection: this.elements.hero,
      onProgress: this.handleScrollProgress,
      onScrollIndicatorHide: () => {
        if (this.elements.scrollIndicator) {
          this.elements.scrollIndicator.style.opacity = '0';
        }
      }
    });
  }
  
  initRandomInfoGenerator() {
    this.randomInfoGenerator = new RandomInfoGenerator({
      container: this.elements.randomInfo,
      interval: 1500
    });
  }
  
  initCarousel() {
    const carousel = this.elements.carousel;
    if (!carousel) return;
    
    const track = carousel.querySelector('.carousel__track');
    const prevBtn = document.querySelector('.carousel__arrow--prev');
    const nextBtn = document.querySelector('.carousel__arrow--next');
    
    if (!track || !prevBtn || !nextBtn) return;
    
    const scrollAmount = 340; // Card width + gap
    
    prevBtn.addEventListener('click', () => {
      carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });
    
    nextBtn.addEventListener('click', () => {
      carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
  }
  
  setupEventListeners() {
    // Debounced resize handler
    let resizeTimeout;
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(this.handleResize, 150);
    });
    
    // Visibility change - pause/resume animation
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.pause();
      } else {
        this.resume();
      }
    });
  }
  
  handleResize() {
    if (this.canvasRenderer) {
      this.canvasRenderer.resize();
    }
  }
  
  handleScrollProgress(data) {
    const { progress, velocity, isHeroVisible } = data;
    
    // Update canvas renderer with scroll progress
    if (this.canvasRenderer) {
      this.canvasRenderer.setScrollProgress(progress);
    }
    
    // Update hero title based on scroll
    if (this.elements.heroTitle) {
      const scale = 1 + progress * 0.1;
      const opacity = 1 - progress * 0.5;
      const blur = progress * 5;
      
      this.elements.heroTitle.style.transform = `scale(${scale})`;
      this.elements.heroTitle.style.opacity = opacity;
      this.elements.heroTitle.style.filter = `blur(${blur}px)`;
    }
    
    // Show/hide random info based on visibility
    if (!isHeroVisible) {
      this.randomInfoGenerator.stop();
    } else if (!this.randomInfoGenerator.isRunning) {
      this.randomInfoGenerator.start();
    }
  }
  
  start() {
    if (this.isRunning) return;
    
    this.isRunning = true;
    this.lastFrameTime = performance.now();
    this.animate();
  }
  
  pause() {
    this.isRunning = false;
    
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }
  
  resume() {
    if (!this.isRunning) {
      this.start();
    }
  }
  
  animate(currentTime = performance.now()) {
    if (!this.isRunning) return;
    
    // Calculate delta time for frame-independent animation
    const deltaTime = currentTime - this.lastFrameTime;
    this.lastFrameTime = currentTime;
    
    // Render canvas
    if (this.canvasRenderer) {
      this.canvasRenderer.render(deltaTime);
    }
    
    // Continue loop
    this.animationId = requestAnimationFrame(this.animate);
  }
  
  destroy() {
    this.pause();
    
    if (this.canvasRenderer) {
      this.canvasRenderer.destroy();
      this.canvasRenderer = null;
    }
    
    if (this.scrollController) {
      this.scrollController.destroy();
      this.scrollController = null;
    }
    
    if (this.randomInfoGenerator) {
      this.randomInfoGenerator.destroy();
      this.randomInfoGenerator = null;
    }
    
    if (this.preloader) {
      this.preloader.destroy();
      this.preloader = null;
    }
  }
}
