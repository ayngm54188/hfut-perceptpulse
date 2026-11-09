import axios from 'axios'

// Create Axios client with base URL pointing to FastAPI backend
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

/**
 * Fetch intelligence items with filters
 * @param {Object} params - { category, campus, search, upcoming_only, page, limit }
 */
export async function getItems(params = {}) {
  const response = await apiClient.get('/items', { params })
  return response.data
}

/**
 * Fetch intelligence item detail by ID
 * @param {number} id
 */
export async function getItemDetail(id) {
  const response = await apiClient.get(`/items/${id}`)
  return response.data
}

/**
 * Fetch system statistics overview
 */
export async function getStatsSummary() {
  const response = await apiClient.get('/stats/summary')
  return response.data
}

export default apiClient
