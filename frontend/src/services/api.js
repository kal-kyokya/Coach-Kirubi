import axios from 'axios'

const api = axios.create({
    baseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
})

export const fetchHome = async () => (await api.get('/pages/home/')).data
export const fetchPrograms = async () => (await api.get('/programs/')).data
export const fetchProgramBySlug = async (slug) => (await api.get(`/programs/${slug}/`)).data
export const fetchCheckout = async (payload) => (await api.get('/orders/checkout/', payload)).data
export const fetchOrderStatus = async (orderId) => (await api.get(`/orders/${orderId}/status/`)).data
