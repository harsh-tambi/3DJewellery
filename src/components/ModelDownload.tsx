import React from 'react'
import { Download } from 'lucide-react'
import { JewelryModel } from '../types/jewelry'
import { 
  extractModelsFromJewelry, 
  exportToOBJ, 
  exportToSTL, 
  downloadFile 
} from '../utils/modelExporter'

interface ModelDownloadProps {
  model: JewelryModel | null
  className?: string
}

const ModelDownload: React.FC<ModelDownloadProps> = ({ model, className = '' }) => {
  const handleDownload = (format: 'obj' | 'stl') => {
    if (!model) {
      alert('No model to download')
      return
    }
    
    try {
      // Extract the jewelry data - handle both nested and direct formats
      const jewelryData = model.geometry
      const models = extractModelsFromJewelry(jewelryData)
      
      if (models.length === 0) {
        alert('No valid geometry found to export')
        return
      }
      
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
      const jewelryType = model.metadata?.jewelry_type || 'jewelry'
      
      if (format === 'obj') {
        const objContent = exportToOBJ(models)
        downloadFile(objContent, `${jewelryType}_${timestamp}.obj`, 'text/plain')
      } else if (format === 'stl') {
        const stlContent = exportToSTL(models)
        downloadFile(stlContent, `${jewelryType}_${timestamp}.stl`, 'text/plain')
      }
      
      console.log(`Downloaded ${format.toUpperCase()} file with ${models.length} parts`)
    } catch (error) {
      console.error('Export error:', error)
      alert('Failed to export model. Check console for details.')
    }
  }
  
  if (!model) {
    return null
  }
  
  return (
    <div className={`flex gap-2 ${className}`}>
      <button
        onClick={() => handleDownload('obj')}
        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        title="Download as OBJ file (compatible with Blender, Maya, etc.)"
      >
        <Download size={16} />
        Download OBJ
      </button>
      
      <button
        onClick={() => handleDownload('stl')}
        className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        title="Download as STL file (compatible with 3D printing software)"
      >
        <Download size={16} />
        Download STL
      </button>
    </div>
  )
}

export default ModelDownload
