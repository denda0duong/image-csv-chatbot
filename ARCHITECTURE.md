# Project Architecture

## 📁 Directory Structure

```
image-csv-chatbot/
├── app.py                      # Main application entry point
├── config.py                   # Configuration and API setup
├── logger_config.py            # Logging system configuration
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
│   │   ├── csv_service.py    # CSV processing with token management
│   │   ├── prompts.py        # Centralized prompt templates
│   │   └── response_handler.py # Response generation handling
│   │
│   └── ui/                    # User interface components
│       ├── chat.py            # Chat UI components
│       └── sidebar.py         # Sidebar UI components
│
├── logs/                       # Application logs (auto-generated)
│   └── chatbot_*.log          # Daily log files
│
├── README.md                  # Main documentation
├── ARCHITECTURE.md            # This file
├── PERFORMANCE_GUIDE.md       # Performance troubleshooting guide
└── TOKEN_ESTIMATION.md        # Token management documentation
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

5. **Generator Pattern**
   - Streaming responses use generators
   - Memory efficient for large responses
   - Immediate feedback to users

### Code Quality Principles

1. **Clean and Focused**
   - Each service has a single responsibility
   - No text-based fallback code (uses File Upload API exclusively)
   - Consolidated error handling
   - Removed redundant methods

2. **Performance Monitoring**
   - Comprehensive timing logs with markers: `[UPLOAD]`, `[REQUEST]`, `[RESPONSE]`
   - First chunk time as key performance indicator
   - Automatic bottleneck detection
   - Built-in diagnostic tools

3. **Token Management**
   - Proactive token estimation before upload
   - Automatic validation against model limits
   - Clear user feedback on token usage
   - Prevention of API errors due to token limits

## 🔧 Component Details

### Models (`src/models/`)

**constants.py**
- `MessageRole`: Enum for message roles
- `AppConfig`: Application-wide constants

**message.py**
- `ChatMessage`: Chat message data structure
- `GeminiMessage`: Gemini API format message
- Auto-generates timestamps when messages are created

### Core Infrastructure

**logger_config.py**
- `LoggerConfig`: Centralized logging configuration
- `setup_logging()`: Configures file and console handlers
- Daily log files in `logs/` directory
- Privacy-focused logging (metadata only)

### Services (`src/services/`)

**chat_history.py**
- `ChatHistoryManager`: Manages chat state
- Methods for CRUD operations on history
- Session state abstraction
- Comprehensive logging of all operations

**gemini_service.py**
- `GeminiChatService`: Gemini API wrapper
- Streaming and non-streaming responses
- Format conversion
- Detailed logging with error tracking and performance metrics
- Response timing tracking (first chunk, total chunks)

**csv_service.py**
- `CSVService`: CSV file processing
- Token estimation and validation
- File Upload API integration
- Comprehensive timing logs for upload operations
- Methods:
  - `estimate_tokens()`: Calculate token usage before upload
  - `validate_tokens()`: Check against model limits (1M tokens)
  - `upload_csv_to_gemini()`: Upload with detailed timing

**prompts.py**
- Centralized prompt templates
- CSV analysis prompts
- System instructions

**response_handler.py**
- `ResponseHandler`: Orchestrates response generation
- Error handling with logging
- Status updates
- Request/response lifecycle tracking

### UI (`src/ui/`)

**chat.py**
- `ChatUI`: Chat interface components
- Message rendering with optional timestamps
- Input handling
- Conditional timestamp display based on user preference

**sidebar.py**
- `SidebarUI`: Sidebar components
- Settings
- Information sections
- User preference management

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

## 📊 Recent Enhancements

### Implemented Features

- ✅ **CSV File Upload with Token Management**
  - Token estimation before upload (preview usage)
  - Token validation against 1M token limit
  - File Upload API integration (CSV data doesn't consume tokens)
  - Comprehensive upload timing logs

- ✅ **Performance Diagnostics System**
  - Three-marker logging system: `[UPLOAD]`, `[REQUEST]`, `[RESPONSE]`
  - Detailed timing for all operations
  - First chunk time as key performance indicator
  - Automated performance testing tool
  - Bottleneck detection and recommendations

- ✅ **Code Cleanup (39% Reduction)**
  - Removed text-based fallback methods (uses File Upload API exclusively)
  - Consolidated error handling (7 handlers → 1)
  - Removed unused methods and redundant code
  - Reduced from 737 lines to 449 lines across main services

- ✅ **Message Timestamps**
  - Track when messages are sent/replied
  - Optional display with sidebar toggle
  - Persistent timestamp storage

- ✅ **Comprehensive Logging**
  - Enterprise-grade logging system
  - Daily log files in `logs/` directory
  - File and console handlers
  - Privacy-focused (metadata only)
  - Performance timing included

- ✅ **Image Analysis**
  - Vision AI with Gemini
  - Multiple format support
  - OCR and object detection

### Future Enhancements

Ready for:
- Multiple chat sessions
- Export chat history
- Custom system prompts
- Response templates
- User preferences
- Analytics dashboard
- Advanced CSV filtering
- Data visualization

## 🔒 Security Considerations

1. **API Keys**: Never hardcode, always use .env
2. **Input Validation**: Validate user inputs
3. **Rate Limiting**: Handle API rate limits gracefully
4. **Error Messages**: Don't expose sensitive information
5. **Session State**: Clear sensitive data on logout
6. **Token Limits**: Validate before upload to prevent API errors
7. **File Size**: Check file sizes before processing

## 🎯 Best Practices

1. **Keep components small and focused**
2. **Use type hints everywhere**
3. **Write comprehensive docstrings**
4. **Handle errors gracefully**
5. **Test new features**
6. **Keep dependencies minimal**
7. **Document architectural decisions**
8. **Monitor performance with logging**
9. **Validate tokens before upload**
10. **Use generators for streaming responses**

### Performance Metrics
The tool measures:
1. **Token estimation time** (should be < 1s)
2. **Token validation time** (should be < 0.1s)
3. **File upload time** (varies by size: 2-15s)
4. **First chunk time** (KEY: 3-30s for normal operation)
5. **Total response time** (complete answer)

### Expected Performance
- Small files (< 1K rows): 10-20s total
- Medium files (1K-10K rows): 20-40s total
- Large files (10K-50K rows): 40-90s total
- Complex analysis prompts: 30-60s is NORMAL for large datasets

## 📚 References

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/docs)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Python Best Practices](https://docs.python-guide.org/)
