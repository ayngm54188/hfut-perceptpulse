import { ref, watch } from 'vue'

const STORAGE_KEY = 'hfut_perceptpulse_favorites'

function loadFromStorage() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : []
  } catch (e) {
    console.error('Failed to parse favorites from storage:', e)
    return []
  }
}

// Global reactive state of favorited item IDs
export const favoriteIds = ref(loadFromStorage())

// Sync to localStorage whenever favoriteIds changes
watch(
  favoriteIds,
  (newVal) => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(newVal))
    } catch (e) {
      console.error('Failed to save favorites to storage:', e)
    }
  },
  { deep: true }
)

export function isFavorite(id) {
  return favoriteIds.value.includes(id)
}

export function toggleFavorite(id) {
  const index = favoriteIds.value.indexOf(id)
  if (index > -1) {
    favoriteIds.value.splice(index, 1)
    return false // unfavorited
  } else {
    favoriteIds.value.push(id)
    return true // favorited
  }
}
