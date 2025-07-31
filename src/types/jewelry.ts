export interface JewelryModel {
  geometry: JewelryGeometry
  metadata?: JewelryMetadata
}

export interface JewelryGeometry {
  type: string
  vertices?: number[]
  indices?: number[]
  band?: JewelryGeometry
  stones?: JewelryGeometry[]
  chain?: JewelryGeometry
  pendant?: JewelryGeometry
  post?: JewelryGeometry
  setting?: JewelryGeometry
  parameters?: Record<string, any>
}

export interface JewelryMetadata {
  jewelry_type: string
  style: string
  material: string
  complexity: string
  prompt?: string
  original_prompt?: string
}

export interface JewelryParameters {
  jewelry_type: 'ring' | 'necklace' | 'earrings' | 'bracelet'
  style: 'modern' | 'vintage' | 'classic' | 'artistic'
  material: 'gold' | 'silver' | 'platinum' | 'rose_gold'
  complexity: 'simple' | 'medium' | 'complex'
  
  // Ring specific
  band_width?: number
  band_thickness?: number
  ring_size?: number
  stone_count?: number
  stone_size?: number
  stone_type?: 'diamond' | 'ruby' | 'emerald' | 'sapphire'
  band_style?: 'plain' | 'carved' | 'braided'
  
  // Necklace specific
  chain_length?: number
  chain_style?: 'cable' | 'figaro' | 'rope'
  link_size?: number
  pendant_size?: number
  pendant_style?: 'geometric' | 'organic' | 'minimal'
  
  // Earrings specific
  earring_type?: 'stud' | 'hoop' | 'drop'
  size?: number
  
  // Bracelet specific
  wrist_size?: number
  bracelet_style?: 'chain' | 'bangle' | 'cuff'
  width?: number
}

export interface GenerationOptions {
  jewelry_type?: string
  style?: string
  material?: string
  complexity?: string
  parameters?: Record<string, any>
}

export interface ApiResponse {
  success: boolean
  model_data: JewelryModel
  error?: string
  prompt?: string
  processed_prompt?: string
  parameters?: Record<string, any>
} 