import numpy as np
import trimesh
import json
import asyncio
from typing import Dict, Any, List
import openai
import os

class JewelryGenerator:
    def __init__(self):
        print("[jewelry_generator.py] JewelryGenerator initialized.")
        
        
    async def generate_model(self, processed_prompt: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[jewelry_generator.py] generate_model called with: {processed_prompt}")
        """Generate 3D jewelry model from processed AI prompt"""
        # Extract parameters from processed prompt
        jewelry_type = processed_prompt.get("jewelry_type", "ring")
        style = processed_prompt.get("style", "modern")
        material = processed_prompt.get("material", "gold")
        complexity = processed_prompt.get("complexity", "medium")
        print(f"[jewelry_generator.py] Parameters: type={jewelry_type}, style={style}, material={material}, complexity={complexity}")
        # Generate 3D geometry based on jewelry type
        if jewelry_type == "ring":
            print("[jewelry_generator.py] Generating ring geometry...")
            geometry = await self._generate_ring(processed_prompt)
        elif jewelry_type == "necklace":
            print("[jewelry_generator.py] Generating necklace geometry...")
            geometry = await self._generate_necklace(processed_prompt)
        elif jewelry_type == "earrings":
            print("[jewelry_generator.py] Generating earrings geometry...")
            geometry = await self._generate_earrings(processed_prompt)
        elif jewelry_type == "bracelet":
            print("[jewelry_generator.py] Generating bracelet geometry...")
            geometry = await self._generate_bracelet(processed_prompt)
        else:
            print("[jewelry_generator.py] Unknown type, defaulting to ring geometry...")
            geometry = await self._generate_ring(processed_prompt)  # Default
        print(f"[jewelry_generator.py] Geometry generated: {geometry}")
        return {
            "geometry": geometry,
            "metadata": {
                "jewelry_type": jewelry_type,
                "style": style,
                "material": material,
                "complexity": complexity,
                "prompt": processed_prompt.get("original_prompt", "")
            }
        }
    
    async def _generate_ring(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate ring geometry with customizable parameters"""
        print("[_generate_ring] Called with prompt_data:", prompt_data)
        try:
            # Extract ring-specific parameters
            band_width = prompt_data.get("band_width") or 3.0
            band_thickness = prompt_data.get("band_thickness") or 1.5
            ring_size = prompt_data.get("ring_size") or 18.0  # US ring size
            stone_count = prompt_data.get("stone_count") if prompt_data.get("stone_count") is not None else 1
            stone_size = prompt_data.get("stone_size") or 2.0
            print(f"[_generate_ring] band_width={band_width}, band_thickness={band_thickness}, ring_size={ring_size}, stone_count={stone_count}, stone_size={stone_size}")
            # Convert ring size to diameter (mm)
            diameter = self._ring_size_to_diameter(ring_size)
            radius = diameter / 2
            print(f"[_generate_ring] diameter={diameter}, radius={radius}")
            # Create ring band (torus)
            band_geometry = self._create_torus(
                radius=radius,
                tube_radius=band_thickness,
                radial_segments=32,
                tubular_segments=16
            )
            print(f"[_generate_ring] band_geometry={band_geometry}")
            # Add stones if specified
            stones = []
            if stone_count > 0:
                stone_positions = self._calculate_stone_positions(stone_count, radius)
                print(f"[_generate_ring] stone_positions={stone_positions}")
                for i, pos in enumerate(stone_positions):
                    stone = self._create_stone(
                        size=stone_size,
                        position=pos,
                    )
                    print(f"[_generate_ring] stone {i}: {stone}")
                    stones.append(stone)
            return {
                "type": "ring",
                "band": band_geometry,
                "stones": stones,
                "parameters": {
                    "band_width": band_width,
                    "band_thickness": band_thickness,
                    "ring_size": ring_size,
                    "diameter": diameter,
                    "stone_count": stone_count,
                    "stone_size": stone_size
                }
            }
        except Exception as e:
            print(f"[_generate_ring] ERROR: {e}")
            # Fallback: return minimal geometry and error message
            return {
                "type": "ring",
                "band": {
                    "vertices": [0,0,0, 1,0,0, 0,1,0],
                    "indices": [0,1,2]
                },
                "stones": [],
                "parameters": {},
                "error": str(e)
            }
    
    async def _generate_necklace(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate necklace geometry"""
        
        chain_length = prompt_data.get("chain_length", 450)  # mm
        pendant_size = prompt_data.get("pendant_size", 15.0)
        chain_style = prompt_data.get("chain_style", "cable")
        
        # Create chain links
        chain_geometry = self._create_chain(
            length=chain_length,
            style=chain_style,
            link_size=prompt_data.get("link_size", 3.0)
        )
        
        # Create pendant
        pendant = self._create_pendant(
            size=pendant_size,
            style=prompt_data.get("pendant_style", "geometric")
        )
        
        return {
            "type": "necklace",
            "chain": chain_geometry,
            "pendant": pendant,
            "parameters": {
                "chain_length": chain_length,
                "chain_style": chain_style,
                "pendant_size": pendant_size
            }
        }
    
    async def _generate_earrings(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate earring geometry"""
        
        earring_type = prompt_data.get("earring_type", "stud")
        size = prompt_data.get("size", 8.0)
        
        if earring_type == "stud":
            geometry = self._create_stud_earring(size)
        elif earring_type == "hoop":
            geometry = self._create_hoop_earring(size)
        else:
            geometry = self._create_stud_earring(size)
            
        return {
            "type": "earrings",
            "geometry": geometry,
            "parameters": {
                "earring_type": earring_type,
                "size": size
            }
        }
    
    async def _generate_bracelet(self, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate bracelet geometry"""
        
        wrist_size = prompt_data.get("wrist_size", 170)  # mm
        bracelet_style = prompt_data.get("bracelet_style", "chain")
        
        if bracelet_style == "chain":
            geometry = self._create_chain_bracelet(wrist_size)
        elif bracelet_style == "bangle":
            geometry = self._create_bangle_bracelet(wrist_size)
        else:
            geometry = self._create_chain_bracelet(wrist_size)
            
        return {
            "type": "bracelet",
            "geometry": geometry,
            "parameters": {
                "wrist_size": wrist_size,
                "bracelet_style": bracelet_style
            }
        }
    
    def _create_torus(self, radius: float, tube_radius: float, 
                     radial_segments: int = 32, tubular_segments: int = 16) -> Dict[str, Any]:
        """Create torus geometry for ring band"""
        
        # Generate torus vertices
        vertices = []
        indices = []
        
        for i in range(radial_segments + 1):
            for j in range(tubular_segments + 1):
                u = i / radial_segments * 2 * np.pi
                v = j / tubular_segments * 2 * np.pi
                
                x = (radius + tube_radius * np.cos(v)) * np.cos(u)
                y = (radius + tube_radius * np.cos(v)) * np.sin(u)
                z = tube_radius * np.sin(v)
                
                vertices.extend([x, y, z])
        
        # Generate indices
        for i in range(radial_segments):
            for j in range(tubular_segments):
                a = i * (tubular_segments + 1) + j
                b = a + tubular_segments + 1
                c = a + 1
                d = b + 1
                
                indices.extend([a, b, c, b, d, c])
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "torus"
        }
    
    def _create_stone(self, size: float, position: List[float], 
                     stone_type: str = "diamond") -> Dict[str, Any]:
        """Create stone geometry (simplified as octahedron)"""
        
        # Create octahedron for diamond-like stone
        vertices = [
            [0, size, 0], [0, -size, 0], [size, 0, 0], [-size, 0, 0],
            [0, 0, size], [0, 0, -size]
        ]
        
        indices = [
            0, 2, 4, 0, 4, 3, 0, 3, 5, 0, 5, 2,
            1, 2, 4, 1, 4, 3, 1, 3, 5, 1, 5, 2
        ]
        
        # Apply position offset
        positioned_vertices = []
        for vertex in vertices:
            positioned_vertices.extend([
                vertex[0] + position[0],
                vertex[1] + position[1],
                vertex[2] + position[2]
            ])
        
        return {
            "vertices": positioned_vertices,
            "indices": indices,
            "type": "stone",
            "stone_type": stone_type
        }
    
    def _calculate_stone_positions(self, stone_count: int, ring_radius: float) -> List[List[float]]:
        """Calculate positions for stones around the ring"""
        positions = []
        angle_step = 2 * np.pi / stone_count
        
        for i in range(stone_count):
            angle = i * angle_step
            x = ring_radius * np.cos(angle)
            y = ring_radius * np.sin(angle)
            z = 0
            positions.append([x, y, z])
        
        return positions
    
    def _ring_size_to_diameter(self, ring_size: float) -> float:
        """Convert US ring size to diameter in mm"""
        # Approximate conversion
        return 16.5 + ring_size * 0.8
    
    def _create_chain(self, length: float, style: str, link_size: float) -> Dict[str, Any]:
        """Create chain geometry"""
        # Simplified chain representation
        link_count = int(length / (link_size * 2))
        vertices = []
        indices = []
        
        for i in range(link_count):
            x = i * link_size * 2
            # Create oval link
            link_vertices = self._create_oval_link(x, 0, 0, link_size)
            vertices.extend(link_vertices)
            
            # Add indices for this link
            base_index = i * 8
            link_indices = [
                base_index, base_index + 1, base_index + 2,
                base_index + 1, base_index + 3, base_index + 2
            ]
            indices.extend(link_indices)
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "chain",
            "style": style
        }
    
    def _create_oval_link(self, x: float, y: float, z: float, size: float) -> List[float]:
        """Create oval link vertices"""
        return [
            x, y, z, x + size, y, z,
            x, y + size/2, z, x + size, y + size/2, z
        ]
    
    def _create_pendant(self, size: float, style: str) -> Dict[str, Any]:
        """Create pendant geometry"""
        if style == "geometric":
            # Create geometric pendant (hexagon)
            vertices = []
            for i in range(6):
                angle = i * np.pi / 3
                x = size * np.cos(angle)
                y = size * np.sin(angle)
                vertices.extend([x, y, 0])
            
            indices = [0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5]
            
            return {
                "vertices": vertices,
                "indices": indices,
                "type": "pendant",
                "style": style
            }
        else:
            # Default circular pendant
            return self._create_circular_pendant(size)
    
    def _create_circular_pendant(self, size: float) -> Dict[str, Any]:
        """Create circular pendant"""
        segments = 16
        vertices = []
        indices = []
        
        # Center vertex
        vertices.extend([0, 0, 0])
        
        # Perimeter vertices
        for i in range(segments):
            angle = i * 2 * np.pi / segments
            x = size * np.cos(angle)
            y = size * np.sin(angle)
            vertices.extend([x, y, 0])
        
        # Create triangles
        for i in range(segments):
            indices.extend([0, i + 1, (i + 1) % segments + 1])
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "pendant",
            "style": "circular"
        }
    
    def _create_stud_earring(self, size: float) -> Dict[str, Any]:
        """Create stud earring geometry"""
        # Simple cylinder for stud
        height = size * 2
        radius = size / 2
        
        vertices = []
        indices = []
        segments = 12
        
        # Top and bottom circles
        for i in range(segments):
            angle = i * 2 * np.pi / segments
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            # Top circle
            vertices.extend([x, y, height/2])
            # Bottom circle
            vertices.extend([x, y, -height/2])
        
        # Create side faces
        for i in range(segments):
            base = i * 2
            next_base = ((i + 1) % segments) * 2
            
            # Side rectangle
            indices.extend([base, base + 1, next_base, next_base, base + 1, next_base + 1])
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "stud_earring"
        }
    
    def _create_hoop_earring(self, size: float) -> Dict[str, Any]:
        """Create hoop earring geometry"""
        # Create partial torus for hoop
        radius = size
        tube_radius = size / 4
        
        return self._create_torus(
            radius=radius,
            tube_radius=tube_radius,
            radial_segments=16,
            tubular_segments=8
        )
    
    def _create_chain_bracelet(self, wrist_size: float) -> Dict[str, Any]:
        """Create chain bracelet geometry"""
        # Similar to necklace chain but closed loop
        return self._create_chain(
            length=wrist_size,
            style="cable",
            link_size=2.0
        )
    
    def _create_bangle_bracelet(self, wrist_size: float) -> Dict[str, Any]:
        """Create bangle bracelet geometry"""
        # Create open ring (partial torus)
        radius = wrist_size / (2 * np.pi)
        tube_radius = 3.0
        
        return self._create_torus(
            radius=radius,
            tube_radius=tube_radius,
            radial_segments=24,
            tubular_segments=8
        )