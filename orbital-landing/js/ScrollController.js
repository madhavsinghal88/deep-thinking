/**
 * ScrollController.js
 * Handles scroll-linked animations with smooth inertia
 * Uses IntersectionObserver + scroll events for performance
 */

export class ScrollController {
  constructor(options = {}) {
    this.heroSection = options.heroSection || document.getElementById('hero');
    this.onProgress = options.onProgress || (() => {});
    this.onScrollIndicatorHide = options.onScrollIndicatorHide || (() => {});
    
    // Scroll state
    this.scrollProgress = 0;
    this.targetProgress = 0;
    this.velocity = 0;
    this.isHeroVisible = true;
    
    // Performance
    this.ticking = false;
    this.lastScrollY = 0;
    
    // Smoothing factor (lower = smoother but slower)
    this.smoothing = 0.08;
    
    // Bind methods
    this.handleScroll = this.handleScroll.bind(this);
    this.handleResize = this.handleResize.bind(this);
    this.update = this.update.bind(this);
    
    // Initialize
    this.init();
  }
  
  init() {
    // Calculate hero dimensions
    this.calculateDimensions();
    
    // Set up event listeners
    window.addEventListener('scroll', this.handleScroll, { passive: true });
    window.addEventListener('resize', this.debounce(this.handleResize, 150));
    
    // Set up IntersectionObserver for hero visibility
    this.setupIntersectionObserver();
    
    // Start update loop
    this.startUpdateLoop();
  }
  
  calculateDimensions() {
    const rect = this.heroSection.getBoundingClientRect();
    this.heroTop = window.scrollY + rect.top;
    this.heroHeight = rect.height;
    this.viewportHeight = window.innerHeight;
    
    // Scroll range for hero animation (800vh - 100vh = 700vh)
    this.scrollRange = this.heroHeight - this.viewportHeight;
  }
  
  setupIntersectionObserver() {
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          this.isHeroVisible = entry.isIntersecting;
        });
      },
      { threshold: 0 }
    );
    
    this.observer.observe(this.heroSection);
  }
  
  handleScroll() {
    if (!this.ticking) {
      requestAnimationFrame(() => {
        this.updateScrollProgress();
        this.ticking = false;
      });
      this.ticking = true;
    }
  }
  
  updateScrollProgress() {
    const scrollY = window.scrollY;
    
    // Calculate raw progress through hero section
    const scrollInHero = scrollY - this.heroTop;
    const rawProgress = Math.max(0, Math.min(1, scrollInHero / this.scrollRange));
    
    // Store target progress (actual scroll position)
    this.targetProgress = rawProgress;
    
    // Calculate velocity for momentum effects
    this.velocity = scrollY - this.lastScrollY;
    this.lastScrollY = scrollY;
    
    // Hide scroll indicator after first scroll
    if (scrollY > 50) {
      this.onScrollIndicatorHide();
    }
  }
  
  handleResize() {
    this.calculateDimensions();
  }
  
  startUpdateLoop() {
    const loop = () => {
      this.update();
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }
  
  update() {
    // Smooth interpolation towards target
    const diff = this.targetProgress - this.scrollProgress;
    
    if (Math.abs(diff) > 0.0001) {
      this.scrollProgress += diff * this.smoothing;
      
      // Notify listeners with smoothed progress
      this.onProgress({
        progress: this.scrollProgress,
        rawProgress: this.targetProgress,
        velocity: this.velocity,
        isHeroVisible: this.isHeroVisible
      });
    }
  }
  
  // Utility: Debounce function
  debounce(func, wait) {
    let timeout;
    return (...args) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }
  
  // Get current scroll data
  getScrollData() {
    return {
      progress: this.scrollProgress,
      rawProgress: this.targetProgress,
      velocity: this.velocity,
      isHeroVisible: this.isHeroVisible
    };
  }
  
  // Programmatic scroll
  scrollToProgress(progress, duration = 1000) {
    const targetScroll = this.heroTop + (this.scrollRange * progress);
    
    window.scrollTo({
      top: targetScroll,
      behavior: 'smooth'
    });
  }
  
  destroy() {
    window.removeEventListener('scroll', this.handleScroll);
    window.removeEventListener('resize', this.handleResize);
    
    if (this.observer) {
      this.observer.disconnect();
    }
  }
}
