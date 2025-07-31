import React, { useState } from 'react'
import PromptInput from './PromptInput'
import ParametricControls from './ParametricControls'
import { JewelryParameters } from '../types/jewelry'

interface ControlPanelProps {
  viewMode: 'ai' | 'parametric'
  onViewModeChange: (mode: 'ai' | 'parametric') => void
  onGenerate: (prompt: string, options: any) => void
  isLoading: boolean
}

const ControlPanel: React.FC<ControlPanelProps> = ({
  viewMode,
  onViewModeChange,
  onGenerate,
  isLoading
}) => {
  const [prompt, setPrompt] = useState('')
  const [parametricParams, setParametricParams] = useState<JewelryParameters>({
    jewelry_type: 'ring',
    style: 'modern',
    material: 'gold',
    complexity: 'medium',
    band_width: 3.0,
    band_thickness: 1.5,
    ring_size: 18.0,
    stone_count: 1,
    stone_size: 2.0,
    stone_type: 'diamond',
  })

  const handleGenerate = () => {
    if (viewMode === 'ai') {
      onGenerate(prompt, {
        jewelry_type: 'ring',
        style: 'modern',
        material: 'gold',
        complexity: 'medium',
      })
    } else {
      onGenerate('', {
        jewelry_type: parametricParams.jewelry_type,
        parameters: parametricParams,
      })
    }
  }

  return (
    <div className="control-panel p-6 space-y-6">
      {/* Mode Toggle */}
      <div className="flex space-x-2 p-1 bg-gray-100 rounded-lg">
        <button
          onClick={() => onViewModeChange('ai')}
          className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
            viewMode === 'ai'
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          AI Generation
        </button>
        <button
          onClick={() => onViewModeChange('parametric')}
          className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
            viewMode === 'parametric'
              ? 'bg-white text-gray-900 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Parametric
        </button>
      </div>

      {/* Content based on mode */}
      {viewMode === 'ai' ? (
        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-3">AI-Powered Design</h3>
            <p className="text-sm text-gray-600 mb-4">
              Describe your jewelry in natural language and let AI create it for you.
            </p>
          </div>
          
          <PromptInput
            value={prompt}
            onChange={setPrompt}
            placeholder="e.g., A modern gold ring with a large diamond center stone and small sapphires on the sides"
          />
          
          <button
            onClick={handleGenerate}
            disabled={!prompt.trim() || isLoading}
            className="w-full generate-button text-white py-3 px-6 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Generating...' : 'Generate Jewelry'}
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-3">Parametric Design</h3>
            <p className="text-sm text-gray-600 mb-4">
              Fine-tune every aspect of your jewelry with precise controls.
            </p>
          </div>
          
          <ParametricControls
            parameters={parametricParams}
            onChange={setParametricParams}
          />
          
          <button
            onClick={handleGenerate}
            disabled={isLoading}
            className="w-full generate-button text-white py-3 px-6 rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? 'Generating...' : 'Create Jewelry'}
          </button>
        </div>
      )}

      {/* Tips */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 className="font-medium text-blue-900 mb-2">💡 Tips</h4>
        <ul className="text-sm text-blue-800 space-y-1">
          {viewMode === 'ai' ? (
            <>
              <li>• Be specific about materials and stones</li>
              <li>• Mention style preferences (modern, vintage, etc.)</li>
              <li>• Include size and complexity details</li>
            </>
          ) : (
            <>
              <li>• Adjust parameters to see real-time changes</li>
              <li>• Use precise measurements for manufacturing</li>
              <li>• Experiment with different stone types</li>
            </>
          )}
        </ul>
      </div>
    </div>
  )
}

export default ControlPanel 