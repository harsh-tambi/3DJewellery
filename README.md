# Jewelry 3D Platform

A comprehensive browser-based 3D jewelry modeling platform that combines AI-powered design with parametric modeling for creating customizable, precision-controlled 3D jewelry forms suitable for direct manufacturing.

## 🚀 Features

### AI-Powered Design
- **Natural Language Processing**: Convert text descriptions into 3D jewelry models
- **Smart Parameter Extraction**: AI automatically extracts dimensions, materials, and style preferences
- **Multiple Jewelry Types**: Rings, necklaces, earrings, and bracelets
- **Style Variations**: Modern, vintage, classic, and artistic styles

### Parametric Modeling
- **Precise Control**: Fine-tune every aspect of jewelry design
- **Real-time Updates**: See changes instantly in the 3D viewer
- **Manufacturing Ready**: Export models suitable for 3D printing and manufacturing
- **Customizable Parameters**: Band width, stone count, ring size, and more

### 3D Visualization
- **Interactive Viewer**: Rotate, zoom, and pan around your designs
- **Realistic Materials**: Gold, silver, platinum, and rose gold with proper lighting
- **Stone Rendering**: Diamond, ruby, emerald, and sapphire with realistic properties
- **Studio Lighting**: Professional lighting setup for accurate visualization

### Real-time Generation
- **Instant Feedback**: See your jewelry appear in seconds
- **WebSocket Support**: Real-time updates and live collaboration
- **Error Handling**: Graceful fallbacks and user-friendly error messages

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Three.js** for 3D rendering
- **React Three Fiber** for React integration
- **Tailwind CSS** for styling
- **Vite** for fast development

### Backend
- **FastAPI** for high-performance API
- **OpenAI GPT-4** for AI processing
- **NumPy & SciPy** for mathematical operations
- **Trimesh** for 3D geometry processing
- **WebSocket** for real-time communication

### AI Models
- **GPT-4** for natural language processing
- **Custom Parametric Engine** for precise geometry generation
- **Domain-specific Constraints** for jewelry manufacturing

## 📦 Installation

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- OpenAI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jewelry-3d-platform
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Start the development servers**

   In one terminal (backend):
   ```bash
   cd backend
   python main.py
   ```

   In another terminal (frontend):
   ```bash
   npm run dev
   ```

6. **Open your browser**
   Navigate to `http://localhost:3000`

## 🎯 Usage

### AI Generation Mode
1. Select "AI Generation" mode
2. Describe your jewelry in natural language
3. Click "Generate Jewelry"
4. View your 3D model instantly

**Example prompts:**
- "A modern gold ring with a large diamond center stone"
- "Vintage silver necklace with geometric pendant"
- "Rose gold earrings with multiple small sapphires"

### Parametric Mode
1. Select "Parametric" mode
2. Choose jewelry type and style
3. Adjust parameters using sliders
4. Click "Create Jewelry" to generate

### 3D Viewer Controls
- **Mouse**: Rotate the view
- **Scroll**: Zoom in/out
- **Right-click + drag**: Pan the view

## 🔧 Configuration

### Environment Variables
```env
OPENAI_API_KEY=your_openai_api_key_here
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
VITE_API_BASE_URL=http://localhost:8000
```

### Customization
- Modify jewelry templates in `backend/models/parametric_engine.py`
- Adjust AI prompts in `backend/utils/ai_prompt_processor.py`
- Customize materials in `src/components/JewelryViewer.tsx`

## 📊 Supported Jewelry Types

### Rings
- **Band Styles**: Plain, carved, braided
- **Stone Types**: Diamond, ruby, emerald, sapphire
- **Parameters**: Ring size, band width/thickness, stone count/size

### Necklaces
- **Chain Styles**: Cable, figaro, rope
- **Pendant Styles**: Geometric, organic, minimal
- **Parameters**: Chain length, link size, pendant size

### Earrings
- **Types**: Stud, hoop, drop
- **Parameters**: Size, stone type/size
- **Materials**: All precious metals

### Bracelets
- **Styles**: Chain, bangle, cuff
- **Parameters**: Wrist size, width
- **Customization**: Full parametric control

## 🏭 Manufacturing Ready

The platform generates models suitable for:
- **3D Printing**: STL file export
- **CAD Software**: Standard geometry formats
- **Jewelry Manufacturing**: Precision dimensions
- **Rapid Prototyping**: Iterative design process

## 🔮 Future Enhancements

- **Advanced AI Models**: More sophisticated jewelry generation
- **Texture Mapping**: Realistic surface textures
- **Animation**: Jewelry movement and interaction
- **Collaboration**: Multi-user design sessions
- **Export Options**: Multiple file formats
- **Mobile Support**: Responsive design for tablets/phones

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the example prompts

---

**Built with ❤️ for the jewelry design community** 