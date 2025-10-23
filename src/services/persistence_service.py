"""
Persistence service for saving and loading chat history to/from JSON files.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import base64
from logger_config import get_logger

logger = get_logger(__name__)


class PersistenceService:
    """Handles saving and loading chat history from JSON files."""
    
    # Directory to store chat sessions
    SESSIONS_DIR = "chat_sessions"
    
    # Maximum age of sessions before auto-cleanup (in days)
    MAX_SESSION_AGE_DAYS = 7
    
    @staticmethod
    def initialize() -> None:
        """Initialize the persistence service by creating necessary directories."""
        os.makedirs(PersistenceService.SESSIONS_DIR, exist_ok=True)
        logger.info(f"Persistence service initialized - sessions dir: {PersistenceService.SESSIONS_DIR}")
        
        # Cleanup old sessions on initialization
        PersistenceService._cleanup_old_sessions()
    
    @staticmethod
    def generate_session_id() -> str:
        """
        Generate a unique session ID based on timestamp.
        
        Returns:
            Unique session ID string
        """
        return datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    
    @staticmethod
    def save_session(session_id: str, messages: List[Dict]) -> bool:
        """
        Save chat session to JSON file.
        
        Args:
            session_id: Unique identifier for the session
            messages: List of message dictionaries to save
            
        Returns:
            True if save was successful, False otherwise
        """
        try:
            filepath = os.path.join(PersistenceService.SESSIONS_DIR, f"{session_id}.json")
            
            # Convert binary data to base64 for JSON serialization
            serializable_messages = []
            for msg in messages:
                msg_copy = msg.copy()
                
                # Convert plots (list of bytes) to base64
                if 'plots' in msg_copy and msg_copy['plots']:
                    msg_copy['plots'] = [
                        base64.b64encode(plot).decode('utf-8') 
                        for plot in msg_copy['plots']
                    ]
                
                # Convert image (bytes) to base64
                if 'image' in msg_copy and msg_copy['image']:
                    msg_copy['image'] = base64.b64encode(msg_copy['image']).decode('utf-8')
                
                serializable_messages.append(msg_copy)
            
            # Save to file with metadata
            data = {
                'session_id': session_id,
                'created_at': datetime.now().isoformat(),
                'message_count': len(messages),
                'messages': serializable_messages
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Session saved: {session_id} ({len(messages)} messages)")
            return True
            
        except Exception as e:
            logger.error(f"Error saving session {session_id}: {str(e)}", exc_info=True)
            return False
    
    @staticmethod
    def load_session(session_id: str) -> Optional[List[Dict]]:
        """
        Load chat session from JSON file.
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            List of message dictionaries, or None if load failed
        """
        try:
            filepath = os.path.join(PersistenceService.SESSIONS_DIR, f"{session_id}.json")
            
            if not os.path.exists(filepath):
                logger.warning(f"Session file not found: {session_id}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            messages = data.get('messages', [])
            
            # Convert base64 back to binary data
            for msg in messages:
                # Convert plots from base64 to bytes
                if 'plots' in msg and msg['plots']:
                    msg['plots'] = [
                        base64.b64decode(plot) 
                        for plot in msg['plots']
                    ]
                
                # Convert image from base64 to bytes
                if 'image' in msg and msg['image']:
                    msg['image'] = base64.b64decode(msg['image'])
            
            logger.info(f"Session loaded: {session_id} ({len(messages)} messages)")
            return messages
            
        except Exception as e:
            logger.error(f"Error loading session {session_id}: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def delete_session(session_id: str) -> bool:
        """
        Delete a chat session file.
        
        Args:
            session_id: Unique identifier for the session
            
        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            filepath = os.path.join(PersistenceService.SESSIONS_DIR, f"{session_id}.json")
            
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Session deleted: {session_id}")
                return True
            else:
                logger.warning(f"Session file not found for deletion: {session_id}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting session {session_id}: {str(e)}", exc_info=True)
            return False
    
    @staticmethod
    def _cleanup_old_sessions() -> None:
        """Clean up session files older than MAX_SESSION_AGE_DAYS."""
        try:
            if not os.path.exists(PersistenceService.SESSIONS_DIR):
                return
            
            cutoff_date = datetime.now() - timedelta(days=PersistenceService.MAX_SESSION_AGE_DAYS)
            deleted_count = 0
            
            for filename in os.listdir(PersistenceService.SESSIONS_DIR):
                if not filename.endswith('.json'):
                    continue
                
                filepath = os.path.join(PersistenceService.SESSIONS_DIR, filename)
                
                # Check file modification time
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_mtime < cutoff_date:
                    os.remove(filepath)
                    deleted_count += 1
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} old session(s) older than {PersistenceService.MAX_SESSION_AGE_DAYS} days")
                
        except Exception as e:
            logger.error(f"Error during session cleanup: {str(e)}", exc_info=True)
    
    @staticmethod
    def list_sessions() -> List[Dict]:
        """
        List all available sessions with metadata.
        
        Returns:
            List of session metadata dictionaries
        """
        sessions = []
        
        try:
            if not os.path.exists(PersistenceService.SESSIONS_DIR):
                return sessions
            
            for filename in os.listdir(PersistenceService.SESSIONS_DIR):
                if not filename.endswith('.json'):
                    continue
                
                filepath = os.path.join(PersistenceService.SESSIONS_DIR, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    sessions.append({
                        'session_id': data.get('session_id', filename.replace('.json', '')),
                        'created_at': data.get('created_at'),
                        'message_count': data.get('message_count', 0)
                    })
                except Exception:
                    # Skip corrupted or invalid session files
                    continue
            
            # Sort by creation time (newest first)
            sessions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            
        except Exception as e:
            logger.error(f"Error listing sessions: {str(e)}", exc_info=True)
        
        return sessions
