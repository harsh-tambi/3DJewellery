import openai
import os
import json
from typing import Dict, Any, Optional
import asyncio

class AIPromptProcessor:
    def __init__(self):
        # Fix OpenAI client initialization
        print("[ai_prompt_processor.py] AIPromptProcessor initialized.")
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # Initialize OpenAI client with proper error handling
        try:
            self.openai_client = openai.AsyncOpenAI(api_key=api_key)
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            self.openai_client = None
        
    async def process_prompt(self, prompt: str, jewelry_type: str = "ring", 
                           style: str = "modern", material: str = "gold") -> Dict[str, Any]:
        """Process natural language prompt into structured jewelry parameters"""
        print(f"[ai_prompt_processor.py] process_prompt called with: {prompt}, {jewelry_type}, {style}, {material}")
        
        # Create enhanced prompt for AI processing
        enhanced_prompt = self._create_enhanced_prompt(prompt, jewelry_type, style, material)
        
        try:
            # Check if OpenAI client is available
            if not self.openai_client:
                print("OpenAI client not available, using fallback")
                return self._create_default_parameters(prompt, jewelry_type, style, material)
        
            # Use OpenAI to extract parameters
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a jewelry design expert. Extract specific parameters from natural language descriptions of jewelry. Return only valid JSON with the following structure:
{
    "jewelry_type": "ring|necklace|earrings|bracelet",
    "style": "modern|vintage|classic|artistic",
    "material": "gold|silver|platinum|rose_gold",
    "complexity": "simple|medium|complex",
    "band_width": 3.0,
    "band_thickness": 1.5,
    "ring_size": 18.0,
    "stone_count": 1,
    "stone_size": 2.0,
    "stone_type": "diamond|ruby|emerald|sapphire",
    "chain_length": 450,
    "chain_style": "cable|figaro|rope",
    "link_size": 3.0,
    "pendant_size": 15.0,
    "pendant_style": "geometric|organic|minimal",
    "earring_type": "stud|hoop|drop",
    "size": 8.0,
    "wrist_size": 170,
    "bracelet_style": "chain|bangle|cuff",
    "width": 5.0,
    "band_style": "plain|carved|braided"
}"""
                    },
                    {
                        "role": "user",
                        "content": enhanced_prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Parse the response
            content = response.choices[0].message.content
            try:
                parameters = json.loads(content)
                parameters["original_prompt"] = prompt
                return parameters
            except json.JSONDecodeError:
                # Fallback to default parameters
                return self._create_default_parameters(prompt, jewelry_type, style, material)
                
        except Exception as e:
            print(f"AI processing error: {e}")
            # Fallback to default parameters
            return self._create_default_parameters(prompt, jewelry_type, style, material)
    
    def _create_enhanced_prompt(self, prompt: str, jewelry_type: str, style: str, material: str) -> str:
        """Create enhanced prompt for AI processing"""
        
        base_prompt = f"""
Analyze this jewelry description and extract specific parameters:

Original description: "{prompt}"
Jewelry type: {jewelry_type}
Style preference: {style}
Material preference: {material}

Extract all relevant parameters and return them as JSON. Focus on:
- Dimensions (sizes, widths, thicknesses)
- Stone details (count, size, type)
- Style elements (patterns, cuts, designs)
- Material specifications
- Complexity level

Return only valid JSON with the exact structure specified.
"""
        return base_prompt
    
    def _create_default_parameters(self, prompt: str, jewelry_type: str, style: str, material: str) -> Dict[str, Any]:
        """Create default parameters based on basic prompt analysis"""
        
        # Basic keyword analysis
        prompt_lower = prompt.lower()
        
        # Extract jewelry type if not specified
        if jewelry_type == "auto":
            if any(word in prompt_lower for word in ["ring", "band", "engagement"]):
                jewelry_type = "ring"
            elif any(word in prompt_lower for word in ["necklace", "chain", "pendant"]):
                jewelry_type = "necklace"
            elif any(word in prompt_lower for word in ["earrings", "earring", "stud", "hoop"]):
                jewelry_type = "earrings"
            elif any(word in prompt_lower for word in ["bracelet", "bangle", "cuff"]):
                jewelry_type = "bracelet"
            else:
                jewelry_type = "ring"
        
        # Extract style
        if style == "auto":
            if any(word in prompt_lower for word in ["modern", "contemporary", "minimal"]):
                style = "modern"
            elif any(word in prompt_lower for word in ["vintage", "antique", "classic"]):
                style = "vintage"
            elif any(word in prompt_lower for word in ["artistic", "unique", "creative"]):
                style = "artistic"
            else:
                style = "modern"
        
        # Extract material
        if material == "auto":
            if any(word in prompt_lower for word in ["gold", "yellow"]):
                material = "gold"
            elif any(word in prompt_lower for word in ["silver", "white"]):
                material = "silver"
            elif any(word in prompt_lower for word in ["platinum", "plat"]):
                material = "platinum"
            elif any(word in prompt_lower for word in ["rose", "pink"]):
                material = "rose_gold"
            else:
                material = "gold"
        
        # Extract stone information
        stone_count = 1
        stone_type = "diamond"
        stone_size = 2.0
        
        if any(word in prompt_lower for word in ["diamond", "diamonds"]):
            stone_type = "diamond"
        elif any(word in prompt_lower for word in ["ruby", "rubies"]):
            stone_type = "ruby"
        elif any(word in prompt_lower for word in ["emerald", "emeralds"]):
            stone_type = "emerald"
        elif any(word in prompt_lower for word in ["sapphire", "sapphires"]):
            stone_type = "sapphire"
        
        # Extract size information
        if "large" in prompt_lower or "big" in prompt_lower:
            stone_size = 3.0
            stone_count = 1
        elif "small" in prompt_lower or "tiny" in prompt_lower:
            stone_size = 1.0
            stone_count = 1
        elif "multiple" in prompt_lower or "several" in prompt_lower:
            stone_count = 3
            stone_size = 1.5
        
        # Create base parameters
        base_params = {
            "jewelry_type": jewelry_type,
            "style": style,
            "material": material,
            "complexity": "medium",
            "original_prompt": prompt
        }
        
        # Add type-specific parameters
        if jewelry_type == "ring":
            base_params.update({
                "band_width": 3.0,
                "band_thickness": 1.5,
                "ring_size": 18.0,
                "stone_count": stone_count,
                "stone_size": stone_size,
                "stone_type": stone_type,
                "band_style": "plain"
            })
        elif jewelry_type == "necklace":
            base_params.update({
                "chain_length": 450,
                "chain_style": "cable",
                "link_size": 3.0,
                "pendant_size": 15.0,
                "pendant_style": "geometric"
            })
        elif jewelry_type == "earrings":
            base_params.update({
                "earring_type": "stud",
                "size": 8.0,
                "stone_size": stone_size,
                "stone_type": stone_type
            })
        elif jewelry_type == "bracelet":
            base_params.update({
                "wrist_size": 170,
                "bracelet_style": "chain",
                "width": 5.0
            })
        
        return base_params 