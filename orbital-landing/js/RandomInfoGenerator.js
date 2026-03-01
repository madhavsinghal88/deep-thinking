/**
 * RandomInfoGenerator.js
 * Floating data information system
 * Cycles through random info text with smooth opacity transitions
 */

export class RandomInfoGenerator {
  constructor(options = {}) {
    this.container = options.container || document.getElementById('random-info');
    this.textElement = this.container?.querySelector('.hero__info-text');
    
    // Info messages - Portfolio/Engineer themed
    this.messages = options.messages || [
      'BACKEND ENGINEER',
      'JAVA SPECIALIST',
      'SPRING BOOT',
      'GO DEVELOPER',
      'SYSTEM ARCHITECT',
      'PROBLEM SOLVER',
      'OPEN TO OPPORTUNITIES',
      'BUILDING THE FUTURE',
      'SCALABLE SYSTEMS',
      'CLEAN CODE ADVOCATE',
      'CONTINUOUS LEARNER',
      'MICROSERVICES',
      'DATA DRIVEN',
      'REST APIS',
      'CLOUD NATIVE'
    ];
    
    // State
    this.currentIndex = 0;
    this.isRunning = false;
    this.intervalId = null;
    
    // Config
    this.interval = options.interval || 1500; // 1.5 seconds
    this.fadeDuration = options.fadeDuration || 500;
    
    // Bind methods
    this.cycle = this.cycle.bind(this);
  }
  
  start() {
    if (this.isRunning || !this.textElement) return;
    
    this.isRunning = true;
    
    // Show first message immediately
    this.showMessage(this.getRandomMessage());
    
    // Start cycling
    this.intervalId = setInterval(this.cycle, this.interval);
  }
  
  stop() {
    this.isRunning = false;
    
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    
    // Fade out current message
    this.hideMessage();
  }
  
  cycle() {
    // Fade out
    this.hideMessage();
    
    // After fade out, show new message
    setTimeout(() => {
      if (this.isRunning) {
        this.showMessage(this.getRandomMessage());
      }
    }, this.fadeDuration);
  }
  
  getRandomMessage() {
    // Get random message, avoiding immediate repeats
    let newIndex;
    do {
      newIndex = Math.floor(Math.random() * this.messages.length);
    } while (newIndex === this.currentIndex && this.messages.length > 1);
    
    this.currentIndex = newIndex;
    return this.messages[this.currentIndex];
  }
  
  showMessage(message) {
    if (!this.textElement) return;
    
    this.textElement.textContent = message;
    this.textElement.classList.add('is-visible');
  }
  
  hideMessage() {
    if (!this.textElement) return;
    
    this.textElement.classList.remove('is-visible');
  }
  
  // Add custom message
  addMessage(message) {
    if (!this.messages.includes(message)) {
      this.messages.push(message);
    }
  }
  
  // Set all messages
  setMessages(messages) {
    this.messages = messages;
    this.currentIndex = 0;
  }
  
  // Update interval
  setInterval(interval) {
    this.interval = interval;
    
    if (this.isRunning) {
      this.stop();
      this.start();
    }
  }
  
  destroy() {
    this.stop();
    this.container = null;
    this.textElement = null;
  }
}
