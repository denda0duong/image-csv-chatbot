# Project Architecture

## 📁 Directory Structure

```
image-csv-chatbot/
├── app.py                      # Main application entry point
├── config.py                   # Configuration and API setup
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in repo)
├── .env.example               # Template for environment variables
│
├── src/                        # Source code package
│   ├── __init__.py            # Package initialization
│   │
│   ├── models/                 # Data models and constants
│   │   ├── constants.py       # Application constants and enums
│   │   └── message.py         # Message data models
│   │
│   ├── services/              # Business logic and services
│   │   ├── chat_history.py   # Chat history management
│   │   ├── gemini_service.py # Gemini API communication
│   │   └── response_handler.py # Response generation handling
│   │
│   └── ui/                    # User interface components
│       ├── chat.py            # Chat UI components
│       └── sidebar.py         # Sidebar UI components
│
└── README.md                  # Main documentation
```

## 🏗️ Architecture Principles

### Clean Architecture
The project follows clean architecture principles with clear separation of concerns:

1. **Models Layer** (`src/models/`)
   - Data structures and constants
   - No dependencies on UI or services
   - Pure Python classes

2. **Services Layer** (`src/services/`)
   - Business logic
   - API communication
   - State management
   - Independent of UI framework

3. **UI Layer** (`src/ui/`)
   - Streamlit-specific components
   - No business logic
   - Purely presentational

4. **Entry Point** (`app.py`)
   - Orchestrates all components
   - Minimal logic
   - Easy to understand flow

### Design Patterns Used

1. **Static Methods Pattern**
   - Utility classes use static methods
   - No need for instantiation
   - Clear, focused responsibilities

2. **Service Pattern**
   - Services encapsulate business logic
   - Easy to test and mock
   - Reusable across features

3. **Facade Pattern**
   - UI components provide simple interfaces
   - Hide complexity
   - Easy to modify

4. **Strategy Pattern**
   - ResponseHandler can be extended
   - Different response strategies possible
   - Easy to add new features

## 🔧 Component Details

### Models (`src/models/`)

**constants.py**
- `MessageRole`: Enum for message roles
- `AppConfig`: Application-wide constants

**message.py**
- `ChatMessage`: Chat message data structure
- `GeminiMessage`: Gemini API format message

### Services (`src/services/`)

**chat_history.py**
- `ChatHistoryManager`: Manages chat state
- Methods for CRUD operations on history
- Session state abstraction

**gemini_service.py**
- `GeminiChatService`: Gemini API wrapper
- Streaming and non-streaming responses
- Format conversion

**response_handler.py**
- `ResponseHandler`: Orchestrates response generation
- Error handling
- Status updates

### UI (`src/ui/`)

**chat.py**
- `ChatUI`: Chat interface components
- Message rendering
- Input handling

**sidebar.py**
- `SidebarUI`: Sidebar components
- Settings
- Information sections

## 🚀 Adding New Features

### Adding a New Service

1. Create a new file in `src/services/`
2. Implement your service class
3. Import it in `src/__init__.py`
4. Use it in `app.py` or other components

Example:
```python
# src/services/csv_service.py
class CSVService:
    """Handles CSV file processing."""
    
    def process_csv(self, file) -> str:
        # Your logic here
        pass
```

### Adding a New UI Component

1. Create a new file in `src/ui/`
2. Implement your UI class
3. Import and use in `app.py`

Example:
```python
# src/ui/file_upload.py
class FileUploadUI:
    """Handles file upload interface."""
    
    @staticmethod
    def render() -> None:
        # Your UI code here
        pass
```

### Adding a New Model

1. Create a new file or add to existing in `src/models/`
2. Define your data structure
3. Import in `src/__init__.py`

Example:
```python
# src/models/file.py
from dataclasses import dataclass

@dataclass
class UploadedFile:
    """Represents an uploaded file."""
    name: str
    content: bytes
    type: str
```

## 🧪 Testing Strategy

### Unit Tests
- Test each service independently
- Mock external dependencies
- Test edge cases

### Integration Tests
- Test component interactions
- Test with real API (rate limits!)
- Test error scenarios

### Manual Testing
- Use test_config.py for setup validation
- Test UI interactions
- Test performance with large histories

## 📊 Future Enhancements

Ready for:
- ✅ CSV file upload and analysis
- ✅ Image upload and vision analysis
- ✅ Multiple chat sessions
- ✅ Export chat history
- ✅ Custom system prompts
- ✅ Response templates
- ✅ User preferences
- ✅ Analytics dashboard

## 🔒 Security Considerations

1. **API Keys**: Never hardcode, always use .env
2. **Input Validation**: Validate user inputs
3. **Rate Limiting**: Handle API rate limits gracefully
4. **Error Messages**: Don't expose sensitive information
5. **Session State**: Clear sensitive data on logout

## 🎯 Best Practices

1. **Keep components small and focused**
2. **Use type hints everywhere**
3. **Write comprehensive docstrings**
4. **Handle errors gracefully**
5. **Test new features**
6. **Keep dependencies minimal**
7. **Document architectural decisions**

## 📚 References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Best Practices](https://docs.python-guide.org/)
