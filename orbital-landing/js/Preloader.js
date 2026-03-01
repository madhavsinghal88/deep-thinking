/**
 * Preloader.js
 * Handles initial loading animation and asset preloading
 */

export class Preloader {
  constructor(options = {}) {
    this.element = options.element || document.getElementById('preloader');
    this.onComplete = options.onComplete || (() => {});
    
    // Assets to preload
    this.assets = options.assets || [];
    
    // State
    this.loadedCount = 0;
    this.isComplete = false;
    
    // Minimum display time (ms)
    this.minDisplayTime = options.minDisplayTime || 1500;
    this.startTime = Date.now();
  }
  
  async start() {
    // Preload all assets
    await this.preloadAssets();
    
    // Ensure minimum display time has passed
    const elapsed = Date.now() - this.startTime;
    const remaining = this.minDisplayTime - elapsed;
    
    if (remaining > 0) {
      await this.delay(remaining);
    }
    
    // Hide preloader
    this.hide();
  }
  
  async preloadAssets() {
    if (this.assets.length === 0) {
      // If no specific assets, wait for document to be ready
      return this.waitForDocumentReady();
    }
    
    const promises = this.assets.map(asset => this.loadAsset(asset));
    
    try {
      await Promise.all(promises);
    } catch (error) {
      console.warn('Some assets failed to load:', error);
    }
  }
  
  loadAsset(asset) {
    return new Promise((resolve, reject) => {
      if (asset.type === 'image') {
        const img = new Image();
        img.onload = () => {
          this.loadedCount++;
          this.updateProgress();
          resolve();
        };
        img.onerror = reject;
        img.src = asset.src;
      } else if (asset.type === 'font') {
        // Use FontFaceObserver pattern (simplified)
        document.fonts.ready.then(() => {
          this.loadedCount++;
          this.updateProgress();
          resolve();
        }).catch(reject);
      } else {
        resolve();
      }
    });
  }
  
  waitForDocumentReady() {
    return new Promise(resolve => {
      if (document.readyState === 'complete') {
        resolve();
      } else {
        window.addEventListener('load', resolve, { once: true });
      }
    });
  }
  
  updateProgress() {
    const progress = this.loadedCount / this.assets.length;
    
    // Could update progress bar here if needed
    // this.element.querySelector('.progress').style.width = `${progress * 100}%`;
  }
  
  hide() {
    if (this.isComplete) return;
    
    this.isComplete = true;
    
    // Add hidden class for CSS transition
    this.element.classList.add('is-hidden');
    
    // Remove from DOM after transition
    setTimeout(() => {
      this.element.style.display = 'none';
      this.onComplete();
    }, 600);
  }
  
  // Force show (for testing)
  show() {
    this.isComplete = false;
    this.element.style.display = 'flex';
    this.element.classList.remove('is-hidden');
  }
  
  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  destroy() {
    this.element = null;
  }
}
