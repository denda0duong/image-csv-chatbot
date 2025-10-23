# Architecture Visual Guide

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        app.py                                │
│                  (Entry Point - Orchestrator)                │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            ChatbotApp (Orchestrator)                    │ │
│  │  - Initializes logging system                           │ │
│  │  - Initializes all components                           │ │
│  │  - Coordinates application flow                         │ │
│  │  - Handles CSV upload and image upload                  │ │
│  │  - Routes to plot-aware or regular response handlers    │ │
│  │  - Minimal business logic                               │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┬──────────────┬──────────┐
        │                   │                   │              │          │
        ▼                   ▼                   ▼              ▼          ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌─────────┐  ┌──────────┐
│   MODELS     │   │  SERVICES    │   │      UI      │   │ LOGGING │  │  STORAGE │
│              │   │              │   │              │   │         │  │          │
│ constants.py │   │ chat_history │   │   chat.py    │   │ logger_ │  │  chat_   │
│ message.py   │   │ gemini_svc   │   │  sidebar.py  │   │ config  │  │ sessions/│
│ plot.py      │   │ csv_service  │   │ +image/plot  │   │         │  │  (JSON)  │
│ +image/plots │   │ plot_service │   │  display     │   │         │  │          │
│              │   │ persistence  │   │              │   │         │  │          │
└──────────────┘   │ +code exec   │   └──────────────┘   └─────────┘  └──────────┘
                   └──────────────┘
```

## 📦 Layer Responsibilities

```
┌─────────────────────────────────────────────────────────┐
│                     MODELS LAYER                         │
│  - Data structures (ChatMessage, GeminiMessage, PlotData)│
│  - Constants and enums (MessageRole, AppConfig)         │
│  - Timestamp support for messages                       │
│  - Image and plot data support (binary bytes)           │
│  - No dependencies on other layers                      │
│  - Pure Python, framework-agnostic                      │
└─────────────────────────────────────────────────────────┘
                            │
                            │ uses
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   SERVICES LAYER                         │
│  - Business logic and data processing                   │
│  - ChatHistoryManager: State + persistence + logging    │
│  - GeminiChatService: AI communication + plot extract   │
│  - PersistenceService: JSON file storage (base64)       │
│  - PlotService: Extract plots from API responses        │
│  - PromptAnalyzer: Detect plot requests                 │
│  - ResponseHandler: Route to plot or regular handler    │
│  - CSVService: Token management + file upload           │
│  - Comprehensive event tracking                         │
│  - Independent of UI framework                          │
└─────────────────────────────────────────────────────────┘
                            │
                            │ used by
                            ▼
┌─────────────────────────────────────────────────────────┐
│                      UI LAYER                            │
│  - Streamlit-specific components                        │
│  - ChatUI: Chat interface + timestamp + image/plots     │
│  - SidebarUI: Sidebar + settings + uploads              │
│  - Display images and plots from chat history           │
│  - No business logic                                    │
│  - Purely presentational                                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   LOGGING SYSTEM                         │
│  - logger_config.py: Centralized configuration          │
│  - Daily log files in logs/ directory                   │
│  - File handler: All events (INFO+)                     │
│  - Console handler: Warnings/Errors only                │
│  - Privacy-focused: Metadata only, no message content   │
│  - Session persistence operations logged                │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 PERSISTENCE SYSTEM                       │
│  - JSON files in chat_sessions/ directory               │
│  - Automatic save after each message                    │
│  - Base64 encoding for binary data (images, plots)      │
│  - Session restoration on page refresh                  │
│  - Auto-cleanup of old sessions (7+ days)               │
│  - Unique session IDs with timestamps                   │
└─────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

### Regular Chat Flow
```
User Input
    │
    ▼
┌────────────────┐
│   ChatUI       │ Get user input
│  get_input()   │
└────────────────┘
    │
    ▼
┌─────────────────────┐
│ ChatHistoryManager  │ Store message (with timestamp, image if any)
│   add_message()     │ [LOGGED] → Auto-save to JSON
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  ResponseHandler    │ Orchestrate response
│ handle_response()   │ [LOGGED]
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│ GeminiChatService   │ Get streaming response
│ get_response_stream │ [LOGGED] (timing tracked)
└─────────────────────┘
    │
    ▼
┌────────────────┐
│   ChatUI       │ Display streaming response
│ write_stream() │
└────────────────┘
    │
    ▼
┌─────────────────────┐
│ ChatHistoryManager  │ Store AI response (with timestamp)
│   add_message()     │ [LOGGED] → Auto-save to JSON
└─────────────────────┘

### Plot Generation Flow
```
User Input (with plot keywords)
    │
    ▼
┌────────────────────┐
│ PromptAnalyzer     │ Detect plot request
│  requires_plot()   │ (keywords: plot, chart, graph, etc.)
└────────────────────┘
    │
    ▼
┌─────────────────────┐
│ ChatHistoryManager  │ Store message (with image/timestamp)
│   add_message()     │ [LOGGED] → Auto-save to JSON
└─────────────────────┘
    │
    ▼
┌─────────────────────────┐
│  ResponseHandler        │ Use plot-aware handler
│ handle_response_with    │ [LOGGED]
│     _plots()            │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ GeminiChatService       │ Get non-streaming response with plots
│ get_response_with_plots │ [LOGGED] (code execution enabled)
└─────────────────────────┘
    │
    ▼
┌─────────────────────┐
│   PlotService       │ Extract plots from response
│ extract_plots()     │ (find inline_data parts)
└─────────────────────┘
    │
    ▼
┌────────────────┐
│   ChatUI       │ Display text + plots
│  st.markdown() │
│  st.image()    │
└────────────────┘
    │
    ▼
┌─────────────────────┐
│ ChatHistoryManager  │ Store AI response + plots (as bytes)
│ add_message(plots)  │ [LOGGED] → Auto-save to JSON (base64)
└─────────────────────┘

### Page Refresh Flow
```
Page Refresh (F5)
    │
    ▼
st.session_state cleared
    │
    ▼
┌─────────────────────────┐
│ ChatHistoryManager      │ Initialize
│   initialize()          │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ PersistenceService      │ List all sessions
│  list_sessions()        │
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ PersistenceService      │ Load most recent session
│  load_session()         │ (base64 → bytes for images/plots)
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│ st.session_state        │ Restore messages, session_id
│  messages = loaded      │
└─────────────────────────┘
    │
    ▼
┌────────────────┐
│   ChatUI       │ Render all messages (with images/plots)
│ render_msgs()  │
└────────────────┘
```
│ GeminiChatService   │ Get AI response
│ get_response_stream()│ [LOGGED: request, chunks, completion]
└─────────────────────┘
    │
    ▼
┌────────────────┐
│   ChatUI       │ Display response (with timestamp)
│ display_stream()│
└────────────────┘
    │
    ▼
┌─────────────────────┐
│ ChatHistoryManager  │ Store AI response (with timestamp)
│   add_message()     │ [LOGGED]
└─────────────────────┘
    │
    ▼
User sees response + optional timestamp
```

## 🗂️ File Organization

```
project-root/
│
├── 📄 app.py ─────────────────► Entry point (orchestration + logging init)
├── ⚙️ config.py ──────────────► API configuration (code execution enabled)
├── 📊 logger_config.py ───────► Logging system configuration
│
├── 📁 src/
│   │
│   ├── 📁 models/
│   │   ├── constants.py ──────► Enums, constants
│   │   ├── message.py ────────► Message models (timestamps, images, plots)
│   │   └── plot.py ───────────► Plot data structures
│   │
│   ├── 📁 services/
│   │   ├── chat_history.py ───────► State + persistence (+ logging)
│   │   ├── gemini_service.py ─────► AI API + plot extract (+ logging)
│   │   ├── csv_service.py ────────► CSV upload + token mgmt
│   │   ├── prompts.py ────────────► Prompt templates (code exec)
│   │   ├── prompt_analyzer.py ────► Plot detection
│   │   ├── plot_service.py ───────► Extract plots
│   │   ├── persistence_service.py ► JSON storage (base64)
│   │   └── response_handler.py ───► Response logic (plot-aware)
│   │
│   └── 📁 ui/
│       ├── chat.py ───────────► Chat interface (images, plots, timestamps)
│       └── sidebar.py ────────► Sidebar UI (uploads, settings)
│
├── 📁 logs/
│   └── chatbot_*.log ─────────► Daily log files (performance + session)
│
├── 📁 chat_sessions/
│   └── *.json ────────────────► Saved sessions (auto-generated)
│
└── 📚 Documentation
    ├── README.md
    ├── ARCHITECTURE.md
    ├── ARCHITECTURE_VISUAL.md
    ├── PERFORMANCE_GUIDE.md
    └── TOKEN_ESTIMATION.md
```

## 🔀 Component Interactions

```
┌─────────────┐
│  ChatbotApp │
└──────┬──────┘
       │
       ├─► ChatHistoryManager ──────┐
       │                            │
       ├─► GeminiChatService ───┐   │
       │                        │   │
       ├─► ResponseHandler ◄────┤   │
       │                        │   │
       ├─► ChatUI              │   │
       │   ├─ render_header()   │   │
       │   ├─ render_messages()◄┼───┤
       │   ├─ get_user_input()  │   │
       │   └─ display_stream()  │   │
       │                        │   │
       └─► SidebarUI            │   │
           ├─ render_settings()◄┼───┘
           ├─ render_about()    │
           └─ render_tips()     │
                                │
    Gemini API ◄────────────────┘
```

## 🎯 Design Patterns Applied

```
┌────────────────────────────────────────────────────────┐
│                  FACADE PATTERN                         │
│                                                         │
│  ChatUI, SidebarUI                                     │
│  - Simple interfaces hiding complexity                 │
│  - Easy to use, hard to misuse                        │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                 SERVICE PATTERN                         │
│                                                         │
│  GeminiChatService, ChatHistoryManager                 │
│  - Encapsulate business logic                          │
│  - Reusable across features                           │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│               DEPENDENCY INJECTION                      │
│                                                         │
│  ResponseHandler(chat_service)                         │
│  - Loose coupling                                      │
│  - Easy to test and swap implementations              │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│                STATIC METHODS                           │
│                                                         │
│  ChatUI.render_header()                                │
│  - Stateless utilities                                 │
│  - No instantiation needed                            │
└────────────────────────────────────────────────────────┘
```

## 📈 Scalability Points

```
Current State          Future Extensions
─────────────         ──────────────────

ChatbotApp            + FileUploadApp
    │                 + AnalyticsApp
    │                 + MultiSessionApp
    │
GeminiChatService     + ClaudeChatService
    │                 + OpenAIChatService
    │                 + LocalLLMService
    │
ChatUI                + VoiceUI
    │                 + MobileUI
    │                 + DashboardUI
    │
ChatHistoryManager    + DatabaseManager
    │                 + CloudStorageManager
    │                 + SessionManager
```

## 🧩 Modularity Benefits

```
┌──────────────────────────────────────────────────────┐
│  Want to add CSV analysis?                           │
│                                                       │
│  1. Create: src/services/csv_service.py             │
│  2. Create: src/ui/csv_upload.py                    │
│  3. Import in app.py                                 │
│  4. Done! No changes to existing code               │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  Want to switch UI framework?                        │
│                                                       │
│  1. Keep: Models and Services (unchanged)           │
│  2. Replace: UI layer only                          │
│  3. Update: app.py imports                          │
│  4. 80% of code stays the same!                     │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│  Want to add testing?                                │
│                                                       │
│  1. Test services independently                      │
│  2. Mock dependencies easily                         │
│  3. No need to test UI separately                   │
│  4. Clear boundaries make testing easy              │
└──────────────────────────────────────────────────────┘
```

## 🎨 Clean Architecture Visualization

```
        ┌─────────────────────────────────┐
        │     External Dependencies       │
        │  (Streamlit, Gemini API, etc.)  │
        └───────────────┬─────────────────┘
                        │
        ┌───────────────▼─────────────────┐
        │         UI Layer (src/ui)       │
        │    - Streamlit components       │
        │    - User interactions          │
        └───────────────┬─────────────────┘
                        │
        ┌───────────────▼─────────────────┐
        │    Services Layer (src/services)│
        │    - Business logic             │
        │    - Data processing            │
        │    - External API calls         │
        └───────────────┬─────────────────┘
                        │
        ┌───────────────▼─────────────────┐
        │    Models Layer (src/models)    │
        │    - Data structures            │
        │    - Constants                  │
        │    - Pure Python                │
        └─────────────────────────────────┘

Dependencies flow inward →
Inner layers have no knowledge of outer layers
```

## 🔍 Code Complexity Comparison

```
BEFORE (Monolithic)
───────────────────
app.py: 296 lines
└─ Everything mixed together
   ├─ Hard to find things
   ├─ Hard to test
   └─ Hard to modify

AFTER (Modular)
───────────────
app.py: 79 lines
src/
├─ models/: ~60 lines total
├─ services/: ~150 lines total
└─ ui/: ~120 lines total

Total: ~400 lines (more code but much cleaner!)
Benefits:
✅ Easy to navigate
✅ Easy to test
✅ Easy to modify
✅ Easy to extend
```

## 🚀 Development Workflow

```
New Feature Request
        │
        ▼
    Identify Layer
        │
   ┌────┴────┬────────┬────────┐
   │         │        │        │
   ▼         ▼        ▼        ▼
Model?   Service?   UI?    Multiple?
   │         │        │        │
   ▼         ▼        ▼        ▼
Create    Create   Create   Create
 file      file     file    all needed
   │         │        │        │
   └─────────┴────────┴────────┘
             │
             ▼
      Update app.py
             │
             ▼
         Test feature
             │
             ▼
          Deploy! 🎉
```

This architecture makes development fast, safe, and enjoyable! 🚀
