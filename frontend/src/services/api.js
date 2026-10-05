const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5001/api'

/**
 * Centralized API service for communicating with the Flask backend.
 * All methods return parsed JSON or throw errors with user-friendly messages.
 */

async function handleResponse(res) {
  const data = await res.json()
  if (!res.ok) {
    throw new Error(data.error || `Request failed (${res.status})`)
  }
  return data
}

/** GET /api/health */
export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`)
  return handleResponse(res)
}

/** GET /api/features — returns dropdown options for the prediction form */
export async function getFeatureOptions() {
  const res = await fetch(`${API_BASE}/features`)
  return handleResponse(res)
}

/** GET /api/metrics — returns model performance metrics */
export async function getMetrics() {
  const res = await fetch(`${API_BASE}/metrics`)
  return handleResponse(res)
}

/** POST /api/predict — submit house features for price prediction */
export async function predictPrice(formData) {
  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  })
  return handleResponse(res)
}
