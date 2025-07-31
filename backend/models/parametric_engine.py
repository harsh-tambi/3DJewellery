import numpy as np
import json
from typing import Dict, Any, List
import asyncio

class ParametricEngine:
    def __init__(self):
        print("[parametric_engine.py] ParametricEngine initialized.")
        self.jewelry_templates = {
            "ring": self._ring_template,
            "necklace": self._necklace_template,
            "earrings": self._earrings_template,
            "bracelet": self._bracelet_template
        }
        
    async def create_model(self, jewelry_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        print(f"[parametric_engine.py] create_model called with: {jewelry_type}, {parameters}")
        """Create parametric jewelry model with specific parameters"""
        if jewelry_type not in self.jewelry_templates:
            print(f"[parametric_engine.py] Unsupported jewelry type: {jewelry_type}")
            raise ValueError(f"Unsupported jewelry type: {jewelry_type}")
        # Get the template function
        template_func = self.jewelry_templates[jewelry_type]
        print(f"[parametric_engine.py] Using template function: {template_func.__name__}")
        # Create the model using the template
        model_data = await template_func(parameters)
        print(f"[parametric_engine.py] Model data generated: {model_data}")
        return {
            "type": jewelry_type,
            "geometry": model_data,
            "parameters": parameters
        }
    
    async def _ring_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Parametric ring template"""
        
        # Extract parameters with defaults
        ring_size = params.get("ring_size", 18.0)
        band_width = params.get("band_width", 3.0)
        band_thickness = params.get("band_thickness", 1.5)
        stone_count = params.get("stone_count", 1)
        stone_size = params.get("stone_size", 2.0)
        stone_type = params.get("stone_type", "diamond")
        band_style = params.get("band_style", "plain")
        
        # Convert ring size to diameter
        diameter = self._ring_size_to_diameter(ring_size)
        radius = diameter / 2
        
        # Create band geometry
        band = self._create_parametric_band(
            radius=radius,
            width=band_width,
            thickness=band_thickness,
            style=band_style
        )
        
        # Create stones
        stones = []
        if stone_count > 0:
            stone_positions = self._calculate_stone_positions(stone_count, radius)
            for i, pos in enumerate(stone_positions):
                stone = self._create_parametric_stone(
                    size=stone_size,
                    position=pos,
                    stone_type=stone_type
                )
                stones.append(stone)
        
        return {
            "band": band,
            "stones": stones,
            "parameters": {
                "ring_size": ring_size,
                "diameter": diameter,
                "band_width": band_width,
                "band_thickness": band_thickness,
                "stone_count": stone_count,
                "stone_size": stone_size
            }
        }
    
    async def _necklace_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Parametric necklace template"""
        
        chain_length = params.get("chain_length", 450)
        chain_style = params.get("chain_style", "cable")
        link_size = params.get("link_size", 3.0)
        pendant_size = params.get("pendant_size", 15.0)
        pendant_style = params.get("pendant_style", "geometric")
        
        # Create chain
        chain = self._create_parametric_chain(
            length=chain_length,
            style=chain_style,
            link_size=link_size
        )
        
        # Create pendant
        pendant = self._create_parametric_pendant(
            size=pendant_size,
            style=pendant_style
        )
        
        return {
            "chain": chain,
            "pendant": pendant,
            "parameters": {
                "chain_length": chain_length,
                "chain_style": chain_style,
                "link_size": link_size,
                "pendant_size": pendant_size,
                "pendant_style": pendant_style
            }
        }
    
    async def _earrings_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Parametric earrings template"""
        
        earring_type = params.get("earring_type", "stud")
        size = params.get("size", 8.0)
        stone_size = params.get("stone_size", 2.0)
        
        if earring_type == "stud":
            geometry = self._create_parametric_stud(size, stone_size)
        elif earring_type == "hoop":
            geometry = self._create_parametric_hoop(size)
        elif earring_type == "drop":
            geometry = self._create_parametric_drop(size, stone_size)
        else:
            geometry = self._create_parametric_stud(size, stone_size)
        
        return {
            "geometry": geometry,
            "parameters": {
                "earring_type": earring_type,
                "size": size,
                "stone_size": stone_size
            }
        }
    
    async def _bracelet_template(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Parametric bracelet template"""
        
        wrist_size = params.get("wrist_size", 170)
        bracelet_style = params.get("bracelet_style", "chain")
        width = params.get("width", 5.0)
        
        if bracelet_style == "chain":
            geometry = self._create_parametric_chain_bracelet(wrist_size, width)
        elif bracelet_style == "bangle":
            geometry = self._create_parametric_bangle(wrist_size, width)
        elif bracelet_style == "cuff":
            geometry = self._create_parametric_cuff(wrist_size, width)
        else:
            geometry = self._create_parametric_chain_bracelet(wrist_size, width)
        
        return {
            "geometry": geometry,
            "parameters": {
                "wrist_size": wrist_size,
                "bracelet_style": bracelet_style,
                "width": width
            }
        }
    
    def _create_parametric_band(self, radius: float, width: float, 
                               thickness: float, style: str) -> Dict[str, Any]:
        """Create parametric ring band"""
        
        if style == "plain":
            return self._create_torus(radius, thickness, 32, 16)
        elif style == "carved":
            return self._create_carved_band(radius, width, thickness)
        elif style == "braided":
            return self._create_braided_band(radius, width, thickness)
        else:
            return self._create_torus(radius, thickness, 32, 16)
    
    def _create_carved_band(self, radius: float, width: float, thickness: float) -> Dict[str, Any]:
        """Create carved band with decorative pattern"""
        # Create base torus
        base_torus = self._create_torus(radius, thickness, 64, 32)
        
        # Add carved pattern (simplified as geometric cuts)
        carved_vertices = base_torus["vertices"].copy()
        carved_indices = base_torus["indices"].copy()
        
        # Add decorative cuts
        for i in range(0, len(carved_vertices), 3):
            if i % 9 == 0:  # Every 3rd vertex
                carved_vertices[i] *= 0.95  # Slight inward cut
        
        return {
            "vertices": carved_vertices,
            "indices": carved_indices,
            "type": "carved_band"
        }
    
    def _create_braided_band(self, radius: float, width: float, thickness: float) -> Dict[str, Any]:
        """Create braided band pattern"""
        # Create multiple interwoven bands
        bands = []
        strands = 3
        
        for i in range(strands):
            angle_offset = i * 2 * np.pi / strands
            band = self._create_torus(
                radius + i * 0.2,
                thickness / strands,
                32,
                16
            )
            # Rotate band
            rotated_vertices = []
            for j in range(0, len(band["vertices"]), 3):
                x, y, z = band["vertices"][j:j+3]
                # Apply rotation
                new_x = x * np.cos(angle_offset) - y * np.sin(angle_offset)
                new_y = x * np.sin(angle_offset) + y * np.cos(angle_offset)
                rotated_vertices.extend([new_x, new_y, z])
            band["vertices"] = rotated_vertices
            bands.append(band)
        
        # Combine all bands
        combined_vertices = []
        combined_indices = []
        index_offset = 0
        
        for band in bands:
            combined_vertices.extend(band["vertices"])
            for index in band["indices"]:
                combined_indices.append(index + index_offset)
            index_offset += len(band["vertices"]) // 3
        
        return {
            "vertices": combined_vertices,
            "indices": combined_indices,
            "type": "braided_band"
        }
    
    def _create_parametric_stone(self, size: float, position: List[float], 
                                stone_type: str) -> Dict[str, Any]:
        """Create parametric stone with different cuts"""
        
        if stone_type == "diamond":
            return self._create_diamond_cut(size, position)
        elif stone_type == "ruby":
            return self._create_ruby_cut(size, position)
        elif stone_type == "emerald":
            return self._create_emerald_cut(size, position)
        else:
            return self._create_diamond_cut(size, position)
    
    def _create_diamond_cut(self, size: float, position: List[float]) -> Dict[str, Any]:
        """Create diamond-cut stone (octahedron)"""
        vertices = [
            [0, size, 0], [0, -size, 0], [size, 0, 0], [-size, 0, 0],
            [0, 0, size], [0, 0, -size]
        ]
        
        indices = [
            0, 2, 4, 0, 4, 3, 0, 3, 5, 0, 5, 2,
            1, 2, 4, 1, 4, 3, 1, 3, 5, 1, 5, 2
        ]
        
        # Apply position
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
            "type": "diamond_cut"
        }
    
    def _create_ruby_cut(self, size: float, position: List[float]) -> Dict[str, Any]:
        """Create ruby-cut stone (hexagonal prism)"""
        # Create hexagonal prism
        vertices = []
        indices = []
        
        # Top and bottom hexagons
        for i in range(6):
            angle = i * np.pi / 3
            x = size * np.cos(angle)
            y = size * np.sin(angle)
            
            # Top hexagon
            vertices.extend([x + position[0], y + position[1], size/2 + position[2]])
            # Bottom hexagon
            vertices.extend([x + position[0], y + position[1], -size/2 + position[2]])
        
        # Create side faces
        for i in range(6):
            base = i * 2
            next_base = ((i + 1) % 6) * 2
            
            # Side rectangle
            indices.extend([base, base + 1, next_base, next_base, base + 1, next_base + 1])
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "ruby_cut"
        }
    
    def _create_emerald_cut(self, size: float, position: List[float]) -> Dict[str, Any]:
        """Create emerald-cut stone (rectangular prism with beveled edges)"""
        # Simplified emerald cut as rectangular prism
        half_size = size / 2
        vertices = [
            # Top face
            [-half_size, -half_size, half_size],
            [half_size, -half_size, half_size],
            [half_size, half_size, half_size],
            [-half_size, half_size, half_size],
            # Bottom face
            [-half_size, -half_size, -half_size],
            [half_size, -half_size, -half_size],
            [half_size, half_size, -half_size],
            [-half_size, half_size, -half_size]
        ]
        
        indices = [
            # Top face
            0, 1, 2, 0, 2, 3,
            # Bottom face
            4, 6, 5, 4, 7, 6,
            # Side faces
            0, 4, 1, 1, 4, 5,
            1, 5, 2, 2, 5, 6,
            2, 6, 3, 3, 6, 7,
            3, 7, 0, 0, 7, 4
        ]
        
        # Apply position
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
            "type": "emerald_cut"
        }
    
    def _create_parametric_chain(self, length: float, style: str, link_size: float) -> Dict[str, Any]:
        """Create parametric chain"""
        
        if style == "cable":
            return self._create_cable_chain(length, link_size)
        elif style == "figaro":
            return self._create_figaro_chain(length, link_size)
        elif style == "rope":
            return self._create_rope_chain(length, link_size)
        else:
            return self._create_cable_chain(length, link_size)
    
    def _create_cable_chain(self, length: float, link_size: float) -> Dict[str, Any]:
        """Create cable chain pattern"""
        link_count = int(length / (link_size * 2))
        vertices = []
        indices = []
        
        for i in range(link_count):
            x = i * link_size * 2
            # Create oval link
            link_vertices = self._create_oval_link(x, 0, 0, link_size)
            vertices.extend(link_vertices)
            
            # Add indices
            base_index = i * 8
            link_indices = [
                base_index, base_index + 1, base_index + 2,
                base_index + 1, base_index + 3, base_index + 2
            ]
            indices.extend(link_indices)
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "cable_chain"
        }
    
    def _create_figaro_chain(self, length: float, link_size: float) -> Dict[str, Any]:
        """Create figaro chain pattern (alternating link sizes)"""
        link_count = int(length / (link_size * 3))
        vertices = []
        indices = []
        
        for i in range(link_count):
            x = i * link_size * 3
            # Alternate between large and small links
            current_link_size = link_size * (2 if i % 2 == 0 else 1)
            link_vertices = self._create_oval_link(x, 0, 0, current_link_size)
            vertices.extend(link_vertices)
            
            # Add indices
            base_index = i * 8
            link_indices = [
                base_index, base_index + 1, base_index + 2,
                base_index + 1, base_index + 3, base_index + 2
            ]
            indices.extend(link_indices)
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "figaro_chain"
        }
    
    def _create_rope_chain(self, length: float, link_size: float) -> Dict[str, Any]:
        """Create rope chain pattern (twisted)"""
        link_count = int(length / (link_size * 2))
        vertices = []
        indices = []
        
        for i in range(link_count):
            x = i * link_size * 2
            # Create twisted oval link
            twist_angle = i * np.pi / 4  # Gradual twist
            link_vertices = self._create_twisted_oval_link(x, 0, 0, link_size, twist_angle)
            vertices.extend(link_vertices)
            
            # Add indices
            base_index = i * 8
            link_indices = [
                base_index, base_index + 1, base_index + 2,
                base_index + 1, base_index + 3, base_index + 2
            ]
            indices.extend(link_indices)
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "rope_chain"
        }
    
    def _create_twisted_oval_link(self, x: float, y: float, z: float, size: float, twist: float) -> List[float]:
        """Create twisted oval link"""
        # Apply twist transformation
        cos_twist = np.cos(twist)
        sin_twist = np.sin(twist)
        
        base_vertices = [
            x, y, z, x + size, y, z,
            x, y + size/2, z, x + size, y + size/2, z
        ]
        
        twisted_vertices = []
        for i in range(0, len(base_vertices), 3):
            vx, vy, vz = base_vertices[i:i+3]
            # Apply twist rotation around Y axis
            new_x = vx * cos_twist - vz * sin_twist
            new_z = vx * sin_twist + vz * cos_twist
            twisted_vertices.extend([new_x, vy, new_z])
        
        return twisted_vertices
    
    def _create_parametric_pendant(self, size: float, style: str) -> Dict[str, Any]:
        """Create parametric pendant"""
        
        if style == "geometric":
            return self._create_geometric_pendant(size)
        elif style == "organic":
            return self._create_organic_pendant(size)
        elif style == "minimal":
            return self._create_minimal_pendant(size)
        else:
            return self._create_geometric_pendant(size)
    
    def _create_geometric_pendant(self, size: float) -> Dict[str, Any]:
        """Create geometric pendant (hexagon)"""
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
            "type": "geometric_pendant"
        }
    
    def _create_organic_pendant(self, size: float) -> Dict[str, Any]:
        """Create organic pendant (flower-like)"""
        vertices = []
        petal_count = 8
        
        for i in range(petal_count):
            angle = i * 2 * np.pi / petal_count
            # Create petal shape
            petal_length = size * 0.8
            petal_width = size * 0.3
            
            # Petal tip
            tip_x = petal_length * np.cos(angle)
            tip_y = petal_length * np.sin(angle)
            vertices.extend([tip_x, tip_y, 0])
            
            # Petal base
            base_x = petal_width * np.cos(angle + np.pi/2)
            base_y = petal_width * np.sin(angle + np.pi/2)
            vertices.extend([base_x, base_y, 0])
        
        # Create triangles
        indices = []
        for i in range(petal_count):
            base = i * 2
            next_base = ((i + 1) % petal_count) * 2
            indices.extend([base, next_base, base + 1, next_base, next_base + 1, base + 1])
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "organic_pendant"
        }
    
    def _create_minimal_pendant(self, size: float) -> Dict[str, Any]:
        """Create minimal pendant (circle)"""
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
            "type": "minimal_pendant"
        }
    
    def _create_parametric_stud(self, size: float, stone_size: float) -> Dict[str, Any]:
        """Create parametric stud earring"""
        # Create post
        post_height = size * 2
        post_radius = size / 4
        
        post = self._create_cylinder(post_radius, post_height)
        
        # Create stone setting
        setting = self._create_stone_setting(stone_size, post_radius)
        
        return {
            "post": post,
            "setting": setting,
            "type": "parametric_stud"
        }
    
    def _create_parametric_hoop(self, size: float) -> Dict[str, Any]:
        """Create parametric hoop earring"""
        radius = size
        tube_radius = size / 4
        
        return self._create_torus(
            radius=radius,
            tube_radius=tube_radius,
            radial_segments=16,
            tubular_segments=8
        )
    
    def _create_parametric_drop(self, size: float, stone_size: float) -> Dict[str, Any]:
        """Create parametric drop earring"""
        # Create drop shape (teardrop)
        vertices = []
        indices = []
        
        # Create teardrop shape
        segments = 16
        for i in range(segments):
            angle = i * 2 * np.pi / segments
            # Teardrop formula
            r = size * (1 - np.cos(angle)) / 2
            x = r * np.cos(angle)
            y = r * np.sin(angle)
            vertices.extend([x, y, 0])
        
        # Create triangles
        for i in range(segments - 2):
            indices.extend([0, i + 1, i + 2])
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "parametric_drop"
        }
    
    def _create_parametric_chain_bracelet(self, wrist_size: float, width: float) -> Dict[str, Any]:
        """Create parametric chain bracelet"""
        # Similar to necklace chain but closed loop
        return self._create_parametric_chain(
            length=wrist_size,
            style="cable",
            link_size=width / 2
        )
    
    def _create_parametric_bangle(self, wrist_size: float, width: float) -> Dict[str, Any]:
        """Create parametric bangle bracelet"""
        radius = wrist_size / (2 * np.pi)
        tube_radius = width / 2
        
        return self._create_torus(
            radius=radius,
            tube_radius=tube_radius,
            radial_segments=24,
            tubular_segments=8
        )
    
    def _create_parametric_cuff(self, wrist_size: float, width: float) -> Dict[str, Any]:
        """Create parametric cuff bracelet"""
        # Create open cuff (partial torus with gap)
        radius = wrist_size / (2 * np.pi)
        tube_radius = width / 2
        
        # Create partial torus (3/4 circle)
        vertices = []
        indices = []
        radial_segments = 18  # 3/4 of 24
        tubular_segments = 8
        
        for i in range(radial_segments + 1):
            for j in range(tubular_segments + 1):
                u = i / radial_segments * 1.5 * np.pi  # 3/4 circle
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
            "type": "parametric_cuff"
        }
    
    def _create_cylinder(self, radius: float, height: float) -> Dict[str, Any]:
        """Create cylinder geometry"""
        segments = 12
        vertices = []
        indices = []
        
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
            "type": "cylinder"
        }
    
    def _create_stone_setting(self, stone_size: float, post_radius: float) -> Dict[str, Any]:
        """Create stone setting geometry"""
        # Create prong setting
        prong_count = 4
        prong_length = stone_size * 0.8
        prong_width = post_radius * 0.3
        
        vertices = []
        indices = []
        
        for i in range(prong_count):
            angle = i * 2 * np.pi / prong_count
            
            # Prong base
            base_x = post_radius * np.cos(angle)
            base_y = post_radius * np.sin(angle)
            vertices.extend([base_x, base_y, 0])
            
            # Prong tip
            tip_x = (post_radius + prong_length) * np.cos(angle)
            tip_y = (post_radius + prong_length) * np.sin(angle)
            vertices.extend([tip_x, tip_y, prong_width])
        
        # Create prong faces
        for i in range(prong_count):
            base = i * 2
            next_base = ((i + 1) % prong_count) * 2
            indices.extend([base, next_base, base + 1, next_base, next_base + 1, base + 1])
        
        return {
            "vertices": vertices,
            "indices": indices,
            "type": "stone_setting"
        }
    
    def _create_torus(self, radius: float, tube_radius: float, 
                     radial_segments: int = 32, tubular_segments: int = 16) -> Dict[str, Any]:
        """Create torus geometry"""
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
    
    def _create_oval_link(self, x: float, y: float, z: float, size: float) -> List[float]:
        """Create oval link vertices"""
        return [
            x, y, z, x + size, y, z,
            x, y + size/2, z, x + size, y + size/2, z
        ]
    
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
        return 16.5 + ring_size * 0.8 