# Image CSV Chatbot

A lightweight Streamlit chat application powered by Google Gemini API that can interact with images and CSV files.

## Features

- 🤖 **Multi-turn AI Conversations** - Chat with Google Gemini AI with context awareness
- 🖼️ **Image Analysis** - Upload and analyze images with AI vision capabilities
  - Supported formats: PNG, JPG, JPEG
  - Image description, object detection, text extraction (OCR)
  - Visual question answering
- 📊 **CSV File Analysis** - Upload and analyze data files with AI
  - **File Upload API**: Direct CSV upload to Gemini (no token usage for CSV data!)
  - **Token Estimation**: Preview token usage before processing large files
  - **Token Validation**: Automatic verification against model limits (1M tokens)
  - Support for file uploads and URLs
  - Automatic data analysis and insights
  - Missing value detection and reporting
  - Statistical queries (averages, counts, correlations, etc.)
  - Natural language data exploration
  - Supports files up to 2GB (50K rows recommended for performance)
- 📈 **Interactive Plot Generation** - AI-powered data visualization with code execution
  - **Gemini Code Execution**: Real Python code execution for authentic plots
  - **Automatic Plot Detection**: Intelligently identifies visualization requests
  - **Multiple Plot Types**: Histograms, scatter plots, bar charts, line graphs, pie charts, heatmaps
  - **CSV Integration**: Generate plots from uploaded CSV data
  - **Standalone Plots**: Create visualizations from data described in chat
  - **In-Chat Display**: Plots appear directly in the conversation
- 💾 **Persistent Chat History** - Chat sessions survive page refreshes
  - **JSON File Storage**: Automatic save after each message
  - **Session Management**: Unique session IDs for each conversation
  - **Auto-Cleanup**: Old sessions (7+ days) automatically removed
  - **Image & Plot Persistence**: Uploaded images and generated plots saved with history
- ⏱️ **Message Timestamps** - Track when messages are sent and replied
- 📋 **Comprehensive Logging** - Monitor app activity, debug issues, track performance with detailed timing
- 🔍 **Performance Diagnostics** - Built-in tools to identify and troubleshoot performance bottlenecks
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
│   │   ├── message.py     # Message data structures
│   │   └── plot.py        # Plot data structures
│   │
│   ├── services/          # Business logic
│   │   ├── chat_history.py        # Chat state management with persistence
│   │   ├── gemini_service.py      # AI model communication
│   │   ├── csv_service.py         # CSV processing with token estimation/validation
│   │   ├── prompts.py             # Centralized prompt templates
│   │   ├── prompt_analyzer.py     # Plot detection and prompt analysis
│   │   ├── plot_service.py        # Plot extraction from AI responses
│   │   ├── persistence_service.py # JSON file persistence for chat history
│   │   └── response_handler.py    # Response generation
│   │
│   └── ui/                # UI components
│       ├── chat.py        # Chat interface
│       └── sidebar.py     # Sidebar components
│
├── logs/                   # Application logs (auto-generated)
│   └── chatbot_*.log      # Daily log files with performance timing
│
├── chat_sessions/          # Saved chat sessions (auto-generated, git-ignored)
│   └── *.json             # Session files with chat history
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

#### CSV File Analysis
1. **Upload a CSV file** in the sidebar (📊 CSV Upload section)
   - Drag and drop or click to browse
   - Supported formats: .csv files
   - **Token estimation** shown before upload (Preview: ~X tokens)
   - **Automatic validation** against 1M token limit
2. **File uploads to Gemini** using File Upload API
   - CSV data doesn't count toward prompt token limits
   - Supports large files (up to 2GB, 50K rows recommended)
3. **Ask questions** about your data
   - "What are the main insights from this dataset?"
   - "Show me the average of column X"
   - "Which rows have missing values?"
   - "What correlations exist in this data?"
4. **Get AI-powered analysis** with streaming responses
5. **CSV persists** during your session until you clear or upload new file

#### Plot Generation & Visualization
1. **Request plots naturally** in your conversation
   - With CSV: "Create a histogram of the age column"
   - With CSV: "Plot a scatter chart showing price vs quantity"
   - Standalone: "Plot a line graph showing sales from January to June: 100, 120, 150, 180, 200, 220"
   - Standalone: "Create a pie chart for: Apples 30%, Oranges 25%, Bananas 45%"
2. **AI generates code** using Gemini Code Execution API
   - Executes real Python code with matplotlib
   - Creates authentic, high-quality plots
3. **Plots appear in chat** automatically
   - Displayed inline with AI's explanation
   - Saved in chat history for reference
4. **Supported plot types**:
   - 📊 Histograms
   - 📈 Line graphs
   - 📉 Scatter plots
   - 📊 Bar charts
   - 🥧 Pie charts
   - 🔥 Heatmaps
   - And more!

#### Performance Monitoring
- **Built-in diagnostics**: Run `python test_performance_diagnosis.py quick` to test baseline performance
- **Detailed timing logs**: Check `logs/chatbot_*.log` for performance metrics
  - `[UPLOAD]`: CSV file upload timing
  - `[REQUEST]`: Request processing timing
  - `[RESPONSE]`: AI response timing (first chunk is key metric)
- **Performance guide**: See `PERFORMANCE_GUIDE.md` for troubleshooting slow responses

#### Tips for Best Results
- 💬 Ask clear, specific questions
- 🖼️ Use high-quality images for better analysis
- 📝 Provide context in your prompts when uploading images
- � For plots, specify chart type and data columns clearly
- 🎨 Request specific plot customizations (colors, labels, titles)
- �🔄 Start a new conversation with "Clear Chat History" for fresh context

### Key Features

✨ **Multi-turn Conversations**: The chatbot maintains context throughout your conversation

📝 **Streaming Responses**: See the AI's response appear in real-time

💾 **Persistent Chat History**: Chat sessions automatically saved and restored across page refreshes
- JSON file storage with automatic save after each message
- Most recent session automatically loaded on refresh
- Old sessions (7+ days) automatically cleaned up
- Images and plots preserved in history

🖼️ **Image Vision AI**: Upload and analyze images with Google Gemini's vision capabilities
- Object detection and identification
- Scene understanding and description
- Text extraction (OCR) from images
- Visual question answering
- Images persist in chat history

⏱️ **Message Timestamps**: Optional timestamp display showing when each message was sent/replied

📊 **Comprehensive Logging**: All events, errors, and interactions are logged for monitoring and debugging
- **Performance timing**: Upload, request, and response metrics
- **Token tracking**: Estimation and validation logging
- **Streaming metrics**: First chunk time and total chunks
- **Session tracking**: Chat history save/load operations

📈 **CSV Analysis with Code Execution**:
- **Token estimation**: Preview token usage before upload
- **Token validation**: Automatic check against 1M token limit
- **File Upload API**: CSV data doesn't consume prompt tokens
- **Code-verified answers**: Uses pandas code execution for accurate results
- **Industry-standard approach**: No guessing, only verified calculations

📊 **Interactive Plot Generation**:
- **Real code execution**: Python code execution via Gemini API
- **Smart detection**: Automatically recognizes visualization requests
- **Multiple formats**: Histograms, scatter plots, line graphs, pie charts, heatmaps
- **Flexible input**: Works with uploaded CSV data or standalone data descriptions
- **Silent execution**: Code runs in background, only results shown
- **Plots persist**: Generated plots saved in chat history

🎨 **Clean UI**: Simple, intuitive interface built with Streamlit

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
  - `gemini-2.5-flash` - Main conversational model with vision and code execution
  - `gemini-2.5-flash-lite` - Fast response model for quick interactions
- **Gemini Code Execution** - Secure Python code execution for data analysis and plot generation
- **Pandas** - Data manipulation and CSV handling
- **Pillow (PIL)** - Image processing and format handling
- **Python Logging** - Built-in logging with file and console handlers
- **python-dotenv** - Secure environment variable management
- **JSON** - File-based persistence for chat history storage

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

## License

*(Add your license here)*

## Contributing

*(Add contribution guidelines here)*
