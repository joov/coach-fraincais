/**
 * Composable for calling the backend REST API.
 * All paths are prefixed with /api automatically.
 */
export function useApi() {
  const BASE = '/api'

  async function request(path, options = {}) {
    const url = `${BASE}${path}`
    try {
      const res = await fetch(url, options)
      if (!res.ok) {
        const body = await res.json().catch(() => null)
        const message = body?.detail || body?.message || `Request failed with status ${res.status}`
        throw new Error(message)
      }
      // Handle 204 No Content
      if (res.status === 204) return null
      return await res.json()
    } catch (err) {
      if (err instanceof TypeError) {
        // Network error (server unreachable, CORS, etc.)
        throw new Error(`Network error: ${err.message}`)
      }
      throw err
    }
  }

  function get(path) {
    return request(path, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    })
  }

  function post(path, body) {
    return request(path, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(body),
    })
  }

  function put(path, body) {
    return request(path, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(body),
    })
  }

  function postForm(path, formData) {
    // Do NOT set Content-Type — the browser sets it with the correct boundary
    return request(path, {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: formData,
    })
  }

  return { get, post, put, postForm }
}
