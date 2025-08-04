// src/composables/useFloorPlan.js
import { ref } from 'vue'

const floorPlanImage = ref(null)

export function useFloorPlan() {
  const loadFloorPlan = async (svgPath) => {
    try {
      // Method 1: Load SVG as image (recommended for complex SVGs)
      const img = new Image()
      img.onload = () => {
        floorPlanImage.value = img
      }
      img.onerror = (error) => {
        console.error('Failed to load image:', error)
      }
      
      // For files in public folder, use absolute path starting with /
      img.src = svgPath.startsWith('/') ? svgPath : `/${svgPath}`
      
    } catch (error) {
      console.error('Failed to load floor plan:', error)
    }
  }

  // Alternative method for direct SVG file import
  const loadFloorPlanAsModule = async () => {
    try {
      // Import as URL (works with SVG files in src/assets)
      const { default: svgUrl } = await import('../assets/floor-plan.svg?url')
      const img = new Image()
      img.onload = () => {
        floorPlanImage.value = img
      }
      img.src = svgUrl
    } catch (error) {
      console.error('Failed to load floor plan as module:', error)
    }
  }

  return {
    floorPlanImage,
    loadFloorPlan,
    loadFloorPlanAsModule
  }
}
