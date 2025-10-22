# Image CSV Chatbot

A lightweight Streamlit chat application powered by Google Gemini API that can interact with images and CSV files.

## Features

- 🤖 Chat with Google Gemini AI (vision and text models)
- 📊 Upload and analyze CSV files with Pandas
- 🖼️ Upload and analyze images with AI vision capabilities
- 🔒 Secure API key management using environment variables
- ⚡ Built with Streamlit for fast, interactive UI

## Project Structure

```
image-csv-chatbot/
├── app.py             # Main Streamlit application
├── config.py          # Configuration and API initialization
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (create this)
├── .env.example      # Template for .env file
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

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

- **Type your message** in the chat input at the bottom of the page
- **Press Enter** to send your message
- **Watch the AI respond** with streaming output
- **Continue the conversation** - the AI remembers your chat history
- **Clear history** using the button in the sidebar to start fresh

### Features

✨ **Multi-turn Conversations**: The chatbot maintains context throughout your conversation

📝 **Streaming Responses**: See the AI's response appear in real-time

💾 **Session Persistence**: Chat history is maintained during your session

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

- **Streamlit** - Web application framework
- **Google Gemini API** - AI models for text and vision
- **Pandas** - Data manipulation and CSV handling
- **Pillow** - Image processing
- **python-dotenv** - Environment variable management

## Clean Architecture

This project follows clean architecture principles:
- **Configuration Layer**: `config.py` handles all external dependencies and API initialization
- **Environment Management**: Sensitive data is stored in `.env` and never hardcoded
- **Dependencies**: All requirements are explicitly defined in `requirements.txt`
- **Isolation**: Virtual environment keeps project dependencies separate

## License

*(Add your license here)*

## Contributing

*(Add contribution guidelines here)*
