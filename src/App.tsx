import React, { useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Environment, PerspectiveCamera } from '@react-three/drei'
import JewelryViewer from './components/JewelryViewer'
import ControlPanel from './components/ControlPanel'
import PromptInput from './components/PromptInput'
import LoadingSpinner from './components/LoadingSpinner'
import { JewelryModel } from './types/jewelry'
import { generateJewelry, createParametricJewelry } from './services/api'
import { downloadSTL } from './services/api'

function App() {
  const [currentModel, setCurrentModel] = useState<JewelryModel | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [viewMode, setViewMode] = useState<'ai' | 'parametric'>('ai')
  // Import STL download function
  // @ts-ignore


  const handleGenerateJewelry = async (prompt: string, options: any) => {
    setIsLoading(true)
    setError(null)
    
    try {
      let modelData
      
      if (viewMode === 'ai') {
        modelData = await generateJewelry(prompt, options)
      } else {
        modelData = await createParametricJewelry(options.jewelry_type, options.parameters)
      }
      
      setCurrentModel(modelData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate jewelry')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <header className="glass-effect p-6 mb-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Jewelry 3D Platform
          </h1>
          <p className="text-gray-600 text-lg">
            AI-powered 3D jewelry design and modeling
          </p>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Control Panel */}
          <div className="lg:col-span-1">
            <ControlPanel
              viewMode={viewMode}
              onViewModeChange={setViewMode}
              onGenerate={handleGenerateJewelry}
              isLoading={isLoading}
            />
          </div>

          {/* 3D Viewer */}
          <div className="lg:col-span-2">
            <div className="canvas-container h-96 lg:h-[600px] relative">
              {isLoading && (
                <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-75 z-10">
                  <LoadingSpinner />
                </div>
              )}
              
              {error && (
                <div className="absolute top-4 right-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                  {error}
                </div>
              )}

              <Canvas>
                <PerspectiveCamera makeDefault position={[0, 0, 10]} />
                <OrbitControls 
                  enablePan={true}
                  enableZoom={true}
                  enableRotate={true}
                  minDistance={2}
                  maxDistance={20}
                />
                <Environment preset="studio" />
                
                {currentModel && (
                  <JewelryViewer model={currentModel} />
                )}
              </Canvas>
            </div>
          </div>
        </div>

        {/* Model Information & Download Button */}
        {currentModel && (
          <div className="mt-8">
            <div className="control-panel p-6">
              <h3 className="text-xl font-semibold mb-4">Model Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div>
                  <span className="text-sm font-medium text-gray-500">Type:</span>
                  <p className="text-gray-900">{currentModel.metadata?.jewelry_type || 'Unknown'}</p>
                </div>
                <div>
                  <span className="text-sm font-medium text-gray-500">Style:</span>
                  <p className="text-gray-900">{currentModel.metadata?.style || 'Unknown'}</p>
                </div>
                <div>
                  <span className="text-sm font-medium text-gray-500">Material:</span>
                  <p className="text-gray-900">{currentModel.metadata?.material || 'Unknown'}</p>
                </div>
                {currentModel.metadata?.prompt && (
                  <div className="md:col-span-2 lg:col-span-3">
                    <span className="text-sm font-medium text-gray-500">Original Prompt:</span>
                    <p className="text-gray-900">{currentModel.metadata.prompt}</p>
                  </div>
                )}
              </div>
              {/* Download STL Button */}
              <button
                className="mt-6 w-full generate-button text-white py-3 px-6 rounded-lg font-medium"
                onClick={() => downloadSTL(currentModel.metadata?.prompt || '', currentModel.metadata)}
              >
                Download 3D Model (STL)
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App 