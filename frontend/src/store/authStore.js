import { create } from 'zustand'
import { authAPI } from '../services/api'

export const useAuthStore = create((set, get) => ({
  user: null,
  token: null,
  isAuthenticated: false,

  login: (user, token) => {
    localStorage.setItem('auth-storage', JSON.stringify({ state: { user, token, isAuthenticated: true } }))
    set({ user, token, isAuthenticated: true })
  },

  logout: () => {
    localStorage.removeItem('auth-storage')
    set({ user: null, token: null, isAuthenticated: false })
  },

  updateUser: (user) => {
    try {
      const storage = JSON.parse(localStorage.getItem('auth-storage') || '{}')
      const state = storage.state || {}
      const current = get()
      storage.state = {
        ...state,
        user,
        token: state.token ?? current.token,
        isAuthenticated: state.isAuthenticated ?? current.isAuthenticated
      }
      localStorage.setItem('auth-storage', JSON.stringify(storage))
      set({ user })
    } catch (e) {
      console.error('Error persisting user update:', e)
      set({ user })
    }
  },

  fetchUser: async () => {
    try {
      const response = await authAPI.getProfile()
      if (response.data) {
        const user = response.data
        // Update local storage
        const storage = JSON.parse(localStorage.getItem('auth-storage') || '{}')
        if (storage.state) {
          storage.state.user = user
          localStorage.setItem('auth-storage', JSON.stringify(storage))
        }
        // Update store
        set({ user })
      }
    } catch (error) {
      console.error('Failed to fetch user profile:', error)
    }
  },

  // Initialize from localStorage
  init: () => {
    const storage = localStorage.getItem('auth-storage')
    if (storage) {
      try {
        const { state } = JSON.parse(storage)
        if (state?.token) {
          set({ user: state.user, token: state.token, isAuthenticated: true })
        }
      } catch (e) {
        console.error('Error loading auth state:', e)
      }
    }
  }
}))

// Initialize auth state on load
useAuthStore.getState().init()
