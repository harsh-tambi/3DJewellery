import React from 'react'
import { JewelryParameters } from '../types/jewelry'

interface ParametricControlsProps {
  parameters: JewelryParameters
  onChange: (parameters: JewelryParameters) => void
}

const ParametricControls: React.FC<ParametricControlsProps> = ({ parameters, onChange }) => {
  const updateParameter = (key: keyof JewelryParameters, value: any) => {
    onChange({ ...parameters, [key]: value })
  }

  const renderSlider = (
    label: string,
    key: keyof JewelryParameters,
    min: number,
    max: number,
    step: number = 0.1,
    unit: string = ''
  ) => (
    <div className="space-y-2">
      <div className="flex justify-between items-center">
        <label className="text-sm font-medium text-gray-700">{label}</label>
        <span className="text-sm text-gray-500">
          {parameters[key]}{unit}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={parameters[key] as number}
        onChange={(e) => updateParameter(key, parseFloat(e.target.value))}
        className="w-full parameter-slider"
      />
    </div>
  )

  const renderSelect = (
    label: string,
    key: keyof JewelryParameters,
    options: { value: string; label: string }[]
  ) => (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">{label}</label>
      <select
        value={parameters[key] as string}
        onChange={(e) => updateParameter(key, e.target.value)}
        className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  )

  return (
    <div className="space-y-4">
      {/* Basic Settings */}
      <div className="space-y-3">
        <h4 className="font-medium text-gray-900">Basic Settings</h4>
        
        {renderSelect('Jewelry Type', 'jewelry_type', [
          { value: 'ring', label: 'Ring' },
          { value: 'necklace', label: 'Necklace' },
          { value: 'earrings', label: 'Earrings' },
          { value: 'bracelet', label: 'Bracelet' },
        ])}
        
        {renderSelect('Style', 'style', [
          { value: 'modern', label: 'Modern' },
          { value: 'vintage', label: 'Vintage' },
          { value: 'classic', label: 'Classic' },
          { value: 'artistic', label: 'Artistic' },
        ])}
        
        {renderSelect('Material', 'material', [
          { value: 'gold', label: 'Gold' },
          { value: 'silver', label: 'Silver' },
          { value: 'platinum', label: 'Platinum' },
          { value: 'rose_gold', label: 'Rose Gold' },
        ])}
      </div>

      {/* Ring-specific controls */}
      {parameters.jewelry_type === 'ring' && (
        <div className="space-y-3">
          <h4 className="font-medium text-gray-900">Ring Settings</h4>
          
          {renderSlider('Ring Size', 'ring_size', 4, 12, 0.5, ' US')}
          {renderSlider('Band Width', 'band_width', 1, 8, 0.1, 'mm')}
          {renderSlider('Band Thickness', 'band_thickness', 0.5, 4, 0.1, 'mm')}
          {renderSlider('Stone Count', 'stone_count', 0, 10, 1, '')}
          {renderSlider('Stone Size', 'stone_size', 0.5, 5, 0.1, 'mm')}
          
          {renderSelect('Stone Type', 'stone_type', [
            { value: 'diamond', label: 'Diamond' },
            { value: 'ruby', label: 'Ruby' },
            { value: 'emerald', label: 'Emerald' },
            { value: 'sapphire', label: 'Sapphire' },
          ])}
          
          {renderSelect('Band Style', 'band_style', [
            { value: 'plain', label: 'Plain' },
            { value: 'carved', label: 'Carved' },
            { value: 'braided', label: 'Braided' },
          ])}
        </div>
      )}

      {/* Necklace-specific controls */}
      {parameters.jewelry_type === 'necklace' && (
        <div className="space-y-3">
          <h4 className="font-medium text-gray-900">Necklace Settings</h4>
          
          {renderSlider('Chain Length', 'chain_length', 300, 600, 10, 'mm')}
          {renderSlider('Link Size', 'link_size', 1, 8, 0.5, 'mm')}
          {renderSlider('Pendant Size', 'pendant_size', 5, 30, 0.5, 'mm')}
          
          {renderSelect('Chain Style', 'chain_style', [
            { value: 'cable', label: 'Cable' },
            { value: 'figaro', label: 'Figaro' },
            { value: 'rope', label: 'Rope' },
          ])}
          
          {renderSelect('Pendant Style', 'pendant_style', [
            { value: 'geometric', label: 'Geometric' },
            { value: 'organic', label: 'Organic' },
            { value: 'minimal', label: 'Minimal' },
          ])}
        </div>
      )}

      {/* Earrings-specific controls */}
      {parameters.jewelry_type === 'earrings' && (
        <div className="space-y-3">
          <h4 className="font-medium text-gray-900">Earring Settings</h4>
          
          {renderSlider('Size', 'size', 3, 15, 0.5, 'mm')}
          {renderSlider('Stone Size', 'stone_size', 0.5, 3, 0.1, 'mm')}
          
          {renderSelect('Earring Type', 'earring_type', [
            { value: 'stud', label: 'Stud' },
            { value: 'hoop', label: 'Hoop' },
            { value: 'drop', label: 'Drop' },
          ])}
          
          {renderSelect('Stone Type', 'stone_type', [
            { value: 'diamond', label: 'Diamond' },
            { value: 'ruby', label: 'Ruby' },
            { value: 'emerald', label: 'Emerald' },
            { value: 'sapphire', label: 'Sapphire' },
          ])}
        </div>
      )}

      {/* Bracelet-specific controls */}
      {parameters.jewelry_type === 'bracelet' && (
        <div className="space-y-3">
          <h4 className="font-medium text-gray-900">Bracelet Settings</h4>
          
          {renderSlider('Wrist Size', 'wrist_size', 140, 200, 5, 'mm')}
          {renderSlider('Width', 'width', 2, 12, 0.5, 'mm')}
          
          {renderSelect('Bracelet Style', 'bracelet_style', [
            { value: 'chain', label: 'Chain' },
            { value: 'bangle', label: 'Bangle' },
            { value: 'cuff', label: 'Cuff' },
          ])}
        </div>
      )}
    </div>
  )
}

export default ParametricControls 