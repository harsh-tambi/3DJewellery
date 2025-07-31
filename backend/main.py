from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import asyncio
import os
from typing import List, Optional
from dotenv import load_dotenv
from openai import OpenAI
import httpx

# Import our custom modules
from models.jewelry_generator import JewelryGenerator
from models.parametric_engine import ParametricEngine
from utils.ai_prompt_processor import AIPromptProcessor

load_dotenv()

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise RuntimeError("OPENAI_API_KEY not set in environment variables.")
client = OpenAI()

app = FastAPI(title="Jewelry 3D Platform API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI components with error handling
try:
    jewelry_generator = JewelryGenerator()
    parametric_engine = ParametricEngine()
    ai_processor = AIPromptProcessor()
    print("✅ All components initialized successfully")
except Exception as e:
    print(f"❌ Error initializing components: {e}")
    # Initialize with fallback
    jewelry_generator = JewelryGenerator()
    parametric_engine = ParametricEngine()
    ai_processor = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Pydantic models
class JewelryRequest(BaseModel):
    prompt: str
    jewelry_type: Optional[str] = "ring"
    style: Optional[str] = "modern"
    material: Optional[str] = "gold"
    complexity: Optional[str] = "medium"

class ParametricRequest(BaseModel):
    jewelry_type: str
    parameters: dict

@app.get("/")
async def root():
    return {"message": "Jewelry 3D Platform API"}

@app.post("/api/generate-jewelry")
async def generate_jewelry(request: JewelryRequest):
    """Generate 3D jewelry model from natural language prompt"""
    try:
        # Process the AI prompt
        processed_prompt = await ai_processor.process_prompt(
            request.prompt,
            request.jewelry_type,
            request.style,
            request.material
        )
        # Generate the 3D model
        model_data = await jewelry_generator.generate_model(processed_prompt)
        # If model_data contains an error, return it as a failed response
        if "error" in model_data:
            print(f"[main.py] Error in jewelry generation: {model_data['error']}")
            return {
                "success": False,
                "error": model_data["error"],
                "model_data": model_data,
                "prompt": request.prompt,
                "processed_prompt": processed_prompt
            }
        return {
            "success": True,
            "model_data": model_data,
            "prompt": request.prompt,
            "processed_prompt": processed_prompt
        }
    except Exception as e:
        print(f"[main.py] Exception in /api/generate-jewelry: {e}")
        return {
            "success": False,
            "error": str(e),
            "model_data": {},
            "prompt": request.prompt
        }

@app.post("/api/parametric-jewelry")
async def create_parametric_jewelry(request: ParametricRequest):
    """Create parametric jewelry model with specific parameters"""
    try:
        model_data = await parametric_engine.create_model(
            request.jewelry_type,
            request.parameters
        )
        
        return {
            "success": True,
            "model_data": model_data,
            "parameters": request.parameters
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "generate_jewelry":
                # Handle real-time jewelry generation
                result = await generate_jewelry(JewelryRequest(**message["data"]))
                await manager.send_personal_message(
                    json.dumps({"type": "jewelry_generated", "data": result}),
                    websocket
                )
            
            elif message["type"] == "parametric_jewelry":
                # Handle parametric jewelry creation
                result = await create_parametric_jewelry(ParametricRequest(**message["data"]))
                await manager.send_personal_message(
                    json.dumps({"type": "parametric_generated", "data": result}),
                    websocket
                )
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 