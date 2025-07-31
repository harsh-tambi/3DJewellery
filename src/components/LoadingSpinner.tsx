import React from 'react'

const LoadingSpinner: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center space-y-4">
      <div className="loading-spinner"></div>
      <p className="text-gray-600 font-medium">Generating your jewelry...</p>
    </div>
  )
}

export default LoadingSpinner 