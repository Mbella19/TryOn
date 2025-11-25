import axios from 'axios'

// Direct connection to backend (override with VITE_API_URL if needed)
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  let token = null
  const authStorage = localStorage.getItem('auth-storage')
  if (authStorage) {
    try {
      const { state } = JSON.parse(authStorage)
      token = state?.token || null
    } catch {
      token = null
    }
  }

  if (token) {
    console.log('🔑 Attaching token to request:', token.substring(0, 20) + '...')
    config.headers.Authorization = `Bearer ${token}`
  } else {
    console.log('⚠️ No token found for request')
  }
  return config
})

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getProfile: () => api.get('/user/profile')
}

// Photos APIs
export const photosAPI = {
  getAll: () => api.get('/photos'),
  upload: (formData) => api.post('/photos', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  delete: (id) => api.delete(`/photos/${id}`),
  select: (id) => api.put(`/photos/${id}/select`)
}

// Clothing APIs
export const clothingAPI = {
  getAll: (category) => api.get('/clothing', { params: { category } }),
  upload: (formData) => api.post('/clothing', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  delete: (id) => api.delete(`/clothing/${id}`),
  generateFromText: (data) => api.post('/clothing/generate', data),
  refineGenerated: (data) => api.post('/clothing/refine', data),
  saveGenerated: (data) => api.post('/clothing/save-generated', data),
  importFromUrl: (data) => api.post('/clothing/import', data)
}

// Try-On APIs
export const tryonAPI = {
  generate: (data) => api.post('/tryon', data),
  getSaved: () => api.get('/saved-looks'),
  deleteSaved: (id) => api.delete(`/saved-looks/${id}`)
}

// Daily briefing / utility
export const utilityAPI = {
  getDailyBriefing: (location) => api.get('/daily-briefing', { params: { location } })
}

// Challenge APIs
export const challengeAPI = {
  getCurrent: () => api.get('/challenges'),
  getEntries: (challengeId) => api.get(`/challenges/${challengeId}/entries`),
  enter: (challengeId, payload) => api.post(`/challenges/${challengeId}/enter`, payload),
  vote: (entryId) => api.post('/challenges/vote', { entry_id: entryId })
}

export default api
