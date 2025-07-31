import React, { useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { JewelryModel } from '../types/jewelry'
import * as THREE from 'three'

interface JewelryViewerProps {
  model: JewelryModel
}

const JewelryViewer: React.FC<JewelryViewerProps> = ({ model }) => {
  const { geometry, metadata } = model

  // Check for geometry validity - handle the actual backend structure
  const jewelryData = geometry as any // Cast to any to handle backend structure
  
  const isGeometryValid = jewelryData && (
    (jewelryData.band && Array.isArray(jewelryData.band.vertices) && jewelryData.band.vertices.length > 0) ||
    (jewelryData.chain && Array.isArray(jewelryData.chain.vertices) && jewelryData.chain.vertices.length > 0) ||
    (jewelryData.pendant && Array.isArray(jewelryData.pendant.vertices) && jewelryData.pendant.vertices.length > 0) ||
    (jewelryData.post && Array.isArray(jewelryData.post.vertices) && jewelryData.post.vertices.length > 0) ||
    (jewelryData.setting && Array.isArray(jewelryData.setting.vertices) && jewelryData.setting.vertices.length > 0)
  )

  // Create materials based on jewelry type and material
  const materials = useMemo(() => {
    const materialType = metadata?.material || 'gold'
    
    const materialMap = {
      gold: new THREE.MeshStandardMaterial({
        color: 0xFFD700,
        metalness: 0.9,
        roughness: 0.1,
        envMapIntensity: 1.0,
      }),
      silver: new THREE.MeshStandardMaterial({
        color: 0xC0C0C0,
        metalness: 0.9,
        roughness: 0.1,
        envMapIntensity: 1.0,
      }),
      platinum: new THREE.MeshStandardMaterial({
        color: 0xE5E4E2,
        metalness: 0.9,
        roughness: 0.1,
        envMapIntensity: 1.0,
      }),
      rose_gold: new THREE.MeshStandardMaterial({
        color: 0xB76E79,
        metalness: 0.9,
        roughness: 0.1,
        envMapIntensity: 1.0,
      }),
    }
    
    return materialMap[materialType as keyof typeof materialMap] || materialMap.gold
  }, [metadata?.material])

  // Create stone material
  const stoneMaterial = useMemo(() => {
    const stoneType = jewelryData?.parameters?.stone_type || 'diamond'
    
    const stoneMaterialMap = {
      diamond: new THREE.MeshStandardMaterial({
        color: 0xFFFFFF,
        metalness: 0.0,
        roughness: 0.0,
        envMapIntensity: 1.5,
        transparent: true,
        opacity: 0.9,
      }),
      ruby: new THREE.MeshStandardMaterial({
        color: 0xFF0000,
        metalness: 0.0,
        roughness: 0.1,
        envMapIntensity: 1.2,
      }),
      emerald: new THREE.MeshStandardMaterial({
        color: 0x00FF00,
        metalness: 0.0,
        roughness: 0.1,
        envMapIntensity: 1.2,
      }),
      sapphire: new THREE.MeshStandardMaterial({
        color: 0x0000FF,
        metalness: 0.0,
        roughness: 0.1,
        envMapIntensity: 1.2,
      }),
    }
    
    return stoneMaterialMap[stoneType as keyof typeof stoneMaterialMap] || stoneMaterialMap.diamond
  }, [jewelryData?.parameters?.stone_type])

  // Create geometry from vertices and indices
  const createGeometry = (vertices: number[], indices: number[]) => {
    const geometry = new THREE.BufferGeometry()
    
    // Create Float32Array for vertices
    const vertexArray = new Float32Array(vertices)
    geometry.setAttribute('position', new THREE.BufferAttribute(vertexArray, 3))
    
    // Create indices if provided
    if (indices.length > 0) {
      geometry.setIndex(indices)
    }
    
    // Compute normals for proper lighting
    geometry.computeVertexNormals()
    
    return geometry
  }

  // Render jewelry components
  const renderJewelryComponent = (component: any, material: THREE.Material, position: [number, number, number] = [0, 0, 0]) => {
    if (!component || !component.vertices) return null
    
    const geometry = createGeometry(component.vertices, component.indices)
    
    return (
      <mesh geometry={geometry} material={material} position={position}>
        {component.stones && component.stones.map((stone: any, index: number) => (
          <mesh
            key={index}
            geometry={createGeometry(stone.vertices, stone.indices)}
            material={stoneMaterial}
          />
        ))}
      </mesh>
    )
  }

  // Render based on jewelry type
  const renderJewelry = () => {
    const jewelryType = metadata?.jewelry_type || 'ring'
    
    switch (jewelryType) {
      case 'ring':
        return (
          <group>
            {jewelryData.band && renderJewelryComponent(jewelryData.band, materials)}
            {jewelryData.stones && jewelryData.stones.map((stone: any, index: number) => (
              <mesh
                key={index}
                geometry={createGeometry(stone.vertices, stone.indices)}
                material={stoneMaterial}
              />
            ))}
          </group>
        )
      case 'necklace':
        return (
          <group>
            {jewelryData.chain && renderJewelryComponent(jewelryData.chain, materials)}
            {jewelryData.pendant && renderJewelryComponent(jewelryData.pendant, materials, [0, -2, 0])}
          </group>
        )
      case 'earrings':
        return (
          <group>
            {jewelryData.post && renderJewelryComponent(jewelryData.post, materials)}
            {jewelryData.setting && renderJewelryComponent(jewelryData.setting, materials)}
          </group>
        )
      case 'bracelet':
        return (
          <group>
            {jewelryData.band && renderJewelryComponent(jewelryData.band, materials)}
          </group>
        )
      default:
        // Fallback for any geometry type
        return null
    }
  }

  // Add subtle rotation animation
  useFrame((state) => {
    if (state.clock.elapsedTime < 2) {
      // Initial positioning
      return
    }
    
    // Subtle rotation for better viewing
    const time = state.clock.elapsedTime * 0.1
    state.camera.position.x = Math.sin(time) * 8
    state.camera.position.z = Math.cos(time) * 8
    state.camera.lookAt(0, 0, 0)
  })

  return (
    <group>
      {/* Ambient light for overall illumination */}
      <ambientLight intensity={0.4} />
      {/* Directional light for highlights */}
      <directionalLight
        position={[10, 10, 5]}
        intensity={1}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
      />
      {/* Point light for sparkle effect */}
      <pointLight position={[0, 5, 0]} intensity={0.5} />
      {/* Render the jewelry or show error */}
      {isGeometryValid ? (
        renderJewelry()
      ) : (
        <mesh position={[0,0,0]}>
          <boxGeometry args={[2, 2, 2]} />
          <meshStandardMaterial color="red" />
        </mesh>
        /* You can also add a floating HTML label with @react-three/drei's Html if you want */
      )}
    </group>
  )
}

export default JewelryViewer 