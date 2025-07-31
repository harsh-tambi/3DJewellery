
import axios from 'axios'
import { JewelryModel, JewelryParameters, ApiResponse } from '../types/jewelry'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const generateJewelry = async (
  prompt: string, 
  options: any = {}
): Promise<JewelryModel> => {
  try {
    const response = await api.post<ApiResponse>('/generate-jewelry', {
      prompt,
      jewelry_type: options.jewelry_type || 'ring',
      style: options.style || 'modern',
      material: options.material || 'gold',
      complexity: options.complexity || 'medium',
    })
    
    if (response.data.success) {
      return response.data.model_data
    } else {
      // Show backend error message if available
      throw new Error(response.data.error || 'Failed to generate jewelry')
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Network error')
    }
    throw error
  }
}

export const createParametricJewelry = async (
  jewelry_type: string,
  parameters: Record<string, any>
): Promise<JewelryModel> => {
  try {
    const response = await api.post<ApiResponse>('/parametric-jewelry', {
      jewelry_type,
      parameters,
    })
    
    if (response.data.success) {
      return response.data.model_data
    } else {
      throw new Error('Failed to create parametric jewelry')
    }
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.detail || 'Network error')
    }
    throw error
  }
}

export const connectWebSocket = (onMessage: (data: any) => void) => {
  const ws = new WebSocket(`ws://${window.location.host}/ws`)
  
  ws.onopen = () => {
    console.log('WebSocket connected')
  }
  
  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage(data)
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error)
    }
  }
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
  }
  
  ws.onclose = () => {
    console.log('WebSocket disconnected')
  }
  
  return ws
}

export const downloadSTL = async (prompt: string, options: any = {}) => {
  const response = await api.post('/export-stl', {
    prompt,
    jewelry_type: options.jewelry_type || 'ring',
    style: options.style || 'modern',
    material: options.material || 'gold',
    complexity: options.complexity || 'medium',
  }, { responseType: 'blob' })
  // Create a link and trigger download
  const url = window.URL.createObjectURL(new Blob([response.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'jewelry.stl')
  document.body.appendChild(link)
  link.click()
  link.parentNode?.removeChild(link)
}


export const sendWebSocketMessage = (ws: WebSocket, type: string, data: any) => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type, data }))
  }
} 