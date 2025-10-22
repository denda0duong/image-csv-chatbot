# Image CSV Chatbot

A lightweight Streamlit chat application powered by Google Gemini API that can interact with images and CSV files.

## Features

- 🤖 **Multi-turn AI Conversations** - Chat with Google Gemini AI with context awareness
- �️ **Image Analysis** - Upload and analyze images with AI vision capabilities
  - Supported formats: PNG, JPG, JPEG
  - Image description, object detection, text extraction (OCR)
  - Visual question answering
- 📊 **CSV File Analysis** - Upload and analyze data files (Coming Soon)
- ⏱️ **Message Timestamps** - Track when messages are sent and replied
- 📋 **Comprehensive Logging** - Monitor app activity, debug issues, track performance
- 🔒 **Secure API Management** - Environment variable-based API key storage
- ⚡ **Fast & Interactive** - Built with Streamlit for responsive UI
- 💾 **Session Persistence** - Chat history maintained during your session

## Project Structure

```
image-csv-chatbot/
├── app.py                  # Main application entry point
├── config.py               # Configuration and API initialization
├── logger_config.py        # Logging configuration
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .env.example           # Template for .env file
├── .gitignore             # Git ignore rules
│
├── src/                    # Source code package
│   ├── models/            # Data models and constants
│   │   ├── constants.py   # Application constants
│   │   └── message.py     # Message data structures
│   │
│   ├── services/          # Business logic
│   │   ├── chat_history.py      # Chat state management
│   │   ├── gemini_service.py    # AI model communication
│   │   └── response_handler.py  # Response generation
│   │
│   └── ui/                # UI components
│       ├── chat.py        # Chat interface
│       └── sidebar.py     # Sidebar components
│
├── logs/                   # Application logs (auto-generated)
│   └── chatbot_*.log      # Daily log files
│
├── ARCHITECTURE.md         # Architecture documentation
└── README.md              # This file
```

**Note**: This project follows clean architecture principles with clear separation between models, services, and UI layers. See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download this repository**
   ```powershell
   cd c:\Users\samtr\Documents\dev\personal\AI\image-csv-chatbot
   ```

2. **Create a virtual environment**
   ```powershell
   python -m venv venv
   ```

3. **Activate the virtual environment**
   
   On Windows (PowerShell):
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   On Windows (Command Prompt):
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Set up your environment variables**
   
   Create a `.env` file in the project root directory:
   ```powershell
   # Copy the example file
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your Google Gemini API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
   
   ⚠️ **Important**: Never commit your `.env` file to version control! It's already in `.gitignore`.

### Verify Installation

Test that the configuration loads correctly:
```powershell
python -c "from config import model, text_model; print('✓ Configuration loaded successfully!')"
```

## Usage

### Running the Application

1. **Make sure your virtual environment is activated**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Run the Streamlit app**
   ```powershell
   streamlit run app.py
   ```

3. **Open your browser**
   
   The app will automatically open in your default browser at `http://localhost:8501`

### Using the Chatbot

#### Basic Chat
- **Type your message** in the chat input at the bottom of the page
- **Press Enter** to send your message
- **Watch the AI respond** with streaming output
- **Continue the conversation** - the AI remembers your chat history
- **Clear history** using the button in the sidebar to start fresh
- **Toggle timestamps** in the sidebar to show/hide message times

#### Image Analysis
1. **Upload an image** in the sidebar (🖼️ Image Upload section)
   - Supported formats: PNG, JPG, JPEG
   - Drag and drop or click to browse
2. **Preview appears** - verify your image is loaded
3. **Ask a question** about the image in the chat
   - "What's in this image?"
   - "Describe this photo in detail"
   - "Extract the text from this screenshot"
   - "What objects can you see?"
4. **Get AI analysis** - the image is sent with your prompt
5. **Image auto-clears** - ready for the next image

#### Tips for Best Results
- 💬 Ask clear, specific questions
- 🖼️ Use high-quality images for better analysis
- 📝 Provide context in your prompts when uploading images
- 🔄 Start a new conversation with "Clear Chat History" for fresh context

### Key Features

✨ **Multi-turn Conversations**: The chatbot maintains context throughout your conversation

📝 **Streaming Responses**: See the AI's response appear in real-time

💾 **Session Persistence**: Chat history is maintained during your session

🖼️ **Image Vision AI**: Upload and analyze images with Google Gemini's vision capabilities
- Object detection and identification
- Scene understanding and description
- Text extraction (OCR) from images
- Visual question answering
- Style and composition analysis

⏱️ **Message Timestamps**: Optional timestamp display showing when each message was sent/replied

📊 **Comprehensive Logging**: All events, errors, and interactions are logged for monitoring and debugging

🎨 **Clean UI**: Simple, intuitive interface built with Streamlit

### Additional Documentation

#### Timestamp Feature
The chatbot tracks when messages are sent and replied to:
- **Toggle on/off** in the sidebar settings
- **Format**: Shows time in 24-hour format (e.g., "14:30:15")
- **Persistent**: Timestamps are saved with each message

📖 See [TIMESTAMP_FEATURE.md](TIMESTAMP_FEATURE.md) for detailed documentation.

#### Image Analysis Feature
Upload and analyze images with AI vision:
- **Supported formats**: PNG, JPG, JPEG
- **Use cases**: Image description, OCR, object detection, visual Q&A
- **Privacy**: Images auto-cleared after one use
- **Integration**: Seamlessly works with chat context

📖 See [IMAGE_FEATURE.md](IMAGE_FEATURE.md) for complete guide with examples.

#### Logging System
Enterprise-grade logging for monitoring and debugging:
- **Daily log files**: Automatically created in `logs/` directory
- **Comprehensive tracking**: User actions, API calls, errors, performance
- **Privacy-focused**: Logs metadata only, not message content
- **Easy debugging**: Full error traces with context

📖 See [LOGGING.md](LOGGING.md) for detailed documentation.

### Stopping the Application

Press `Ctrl+C` in the terminal where Streamlit is running

## Development

### Deactivating the Virtual Environment

When you're done working on the project:
```powershell
deactivate
```

### Updating Dependencies

To add new packages:
1. Activate the virtual environment
2. Install the package: `pip install package-name`
3. Update requirements: `pip freeze > requirements.txt`

## Tech Stack

- **Streamlit** - Web application framework for interactive UI
- **Google Gemini API** - Advanced AI models for text and vision analysis
  - `gemini-2.5-pro` - Main conversational model with vision
  - `gemini-2.5-flash` - Fast response model
- **Pandas** - Data manipulation and CSV handling (coming soon)
- **Pillow (PIL)** - Image processing and format handling
- **Python Logging** - Built-in logging with file and console handlers
- **python-dotenv** - Secure environment variable management

## Architecture

This project follows **clean architecture principles** with clear separation of concerns:

### Layer Structure
- **Models Layer** (`src/models/`) - Data structures, constants, message formats
- **Services Layer** (`src/services/`) - Business logic, API communication, state management
- **UI Layer** (`src/ui/`) - Streamlit components, user interface
- **Configuration** (`config.py`, `logger_config.py`) - External dependencies and system setup

### Key Principles
- ✅ **Separation of Concerns**: Each module has a single, well-defined responsibility
- ✅ **Dependency Injection**: Components receive dependencies rather than creating them
- ✅ **Environment Isolation**: Virtual environment keeps dependencies separate
- ✅ **Security First**: API keys and sensitive data stored in `.env` files
- ✅ **Comprehensive Logging**: All operations tracked for debugging and monitoring

📖 See [ARCHITECTURE.md](ARCHITECTURE.md) and [ARCHITECTURE_VISUAL.md](ARCHITECTURE_VISUAL.md) for detailed documentation.

## Documentation

- 📖 [README.md](README.md) - This file (setup and usage guide)
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed architecture documentation
- 📊 [ARCHITECTURE_VISUAL.md](ARCHITECTURE_VISUAL.md) - Visual architecture diagrams
- ⏱️ [TIMESTAMP_FEATURE.md](TIMESTAMP_FEATURE.md) - Timestamp feature guide
- 🖼️ [IMAGE_FEATURE.md](IMAGE_FEATURE.md) - Image analysis feature guide
- 📋 [LOGGING.md](LOGGING.md) - Logging system documentation
- 🚀 [IMAGE_IMPLEMENTATION.md](IMAGE_IMPLEMENTATION.md) - Image feature implementation details

## License

*(Add your license here)*

## Contributing

*(Add contribution guidelines here)*
