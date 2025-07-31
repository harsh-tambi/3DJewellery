import React from 'react'

interface PromptInputProps {
  value: string
  onChange: (value: string) => void
  placeholder?: string
}

const PromptInput: React.FC<PromptInputProps> = ({ value, onChange, placeholder }) => {
  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        Describe your jewelry
      </label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full prompt-input rounded-lg p-3 resize-none h-24 focus:outline-none"
        rows={4}
      />
      <div className="flex justify-between items-center text-xs text-gray-500">
        <span>Be as detailed as possible for better results</span>
        <span>{value.length}/500</span>
      </div>
    </div>
  )
}

export default PromptInput 