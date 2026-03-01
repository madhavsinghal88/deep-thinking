/**
 * main.js
 * Entry point for Orbital Landing Experience
 * Premium Nike x Apple x AI Dashboard aesthetic
 */

import { OrbitalExperience } from './OrbitalExperience.js';

// Global instance
let orbitalExperience = null;

// Initialize when DOM is ready
function init() {
  try {
    orbitalExperience = new OrbitalExperience();
    
    // Expose to global scope for debugging
    if (import.meta.env?.DEV || window.location.hostname === 'localhost') {
      window.orbitalExperience = orbitalExperience;
    }
  } catch (error) {
    console.error('Failed to initialize Orbital Experience:', error);
  }
}

// Handle DOM ready state
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}

// Clean up on page unload
window.addEventListener('beforeunload', () => {
  if (orbitalExperience) {
    orbitalExperience.destroy();
    orbitalExperience = null;
  }
});

// Export for module usage
export { orbitalExperience };
