"""
CSV service for loading, processing, and uploading CSV files for AI analysis.
"""

import pandas as pd
import streamlit as st
import tempfile
from typing import Union, Optional
from logger_config import get_logger

logger = get_logger(__name__)


class CSVService:
    """
    Handles CSV file operations for AI-powered data analysis.
    
    This service provides:
    - CSV loading from file uploads or URLs
    - DataFrame information extraction
    - File upload to Gemini API for direct analysis
    """
    
    @staticmethod
    def load_csv(file_or_url: Union[st.runtime.uploaded_file_manager.UploadedFile, str, None]) -> Optional[pd.DataFrame]:
        """
        Load a CSV file from either an uploaded file or a URL.
        
        Args:
            file_or_url: Either an uploaded file object or a URL string
            
        Returns:
            DataFrame if successful, None if failed
            
        Raises:
            Various exceptions that are caught and logged
        """
        if file_or_url is None:
            return None
        
        try:
            # Load CSV from URL or file
            if isinstance(file_or_url, str):
                if not file_or_url.strip():
                    st.error("❌ Please provide a valid URL")
                    return None
                df = pd.read_csv(file_or_url)
                logger.info(f"CSV loaded from URL: {df.shape[0]} rows × {df.shape[1]} cols")
            else:
                df = pd.read_csv(file_or_url)
                logger.info(f"CSV loaded from file: {df.shape[0]} rows × {df.shape[1]} cols")
            
            # Validate
            if df.empty:
                st.error("❌ The CSV file is empty")
                return None
            
            return df
            
        except Exception as e:
            logger.error(f"Error loading CSV: {str(e)}")
            st.error(f"❌ **Error Loading CSV**\n\n{str(e)}")
            return None
    
    @staticmethod
    def estimate_csv_tokens(df: pd.DataFrame) -> int:
        """
        Estimate the number of tokens in a CSV DataFrame.
        
        Uses a conservative estimate where 1 token ≈ 4 characters.
        This includes all data, column names, and CSV formatting.
        
        Args:
            df: Pandas DataFrame to estimate
            
        Returns:
            Estimated number of tokens
        """
        try:
            # Convert DataFrame to CSV string (in-memory)
            import io
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_string = csv_buffer.getvalue()
            # Calculate total characters and estimate tokens (1 token ≈ 4 chars)
            estimated_tokens = len(csv_string) // 4
            logger.info(f"Estimated tokens: ~{estimated_tokens:,}")
            return estimated_tokens
            
        except Exception as e:
            logger.error(f"Error estimating tokens: {str(e)}")
            return 1_000_000  # Safe fallback
    
    @staticmethod
    def validate_token_limit(df: pd.DataFrame, prompt_text: str = "", max_tokens: int = 1_000_000) -> dict:
        """Validate CSV and prompt won't exceed token limits."""
        csv_tokens = CSVService.estimate_csv_tokens(df)
        prompt_tokens = len(prompt_text) // 4
        total_tokens = csv_tokens + prompt_tokens
        is_valid = total_tokens <= max_tokens
        
        if is_valid:
            percentage = (total_tokens / max_tokens) * 100
            message = f"✅ ~{total_tokens:,} / {max_tokens:,} tokens ({percentage:.1f}%)"
        else:
            message = f"❌ Exceeded by ~{total_tokens - max_tokens:,} tokens"
        
        return {
            'is_valid': is_valid,
            'estimated_csv_tokens': csv_tokens,
            'estimated_prompt_tokens': prompt_tokens,
            'estimated_total_tokens': total_tokens,
            'max_tokens': max_tokens,
            'message': message
        }
    
    @staticmethod
    def upload_csv_to_gemini(df: pd.DataFrame):
        """Upload CSV to Gemini API for file-based analysis (supports up to 2GB)."""
        try:
            from google import genai
            import os
            from dotenv import load_dotenv
            import time
            
            load_dotenv()
            
            upload_start = time.time()
            logger.info(f"[UPLOAD] Starting CSV upload: {df.shape[0]} rows × {df.shape[1]} cols")
            
            # Create temp CSV file
            csv_start = time.time()
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp_file:
                csv_path = tmp_file.name
                df.to_csv(tmp_file, index=False)
            csv_time = time.time() - csv_start
            
            size_mb = os.path.getsize(csv_path) / (1024 * 1024)
            logger.info(f"[UPLOAD] CSV file created in {csv_time:.2f}s ({size_mb:.2f} MB)")
            
            # Upload to Gemini
            api_start = time.time()
            client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
            uploaded_file = client.files.upload(file=csv_path, config={'mime_type': 'text/csv'})
            api_time = time.time() - api_start
            logger.info(f"[UPLOAD] API upload completed in {api_time:.2f}s")
            
            os.unlink(csv_path)  # Clean up immediately
            
            # Wait for processing (max 60s)
            process_start = time.time()
            check_count = 0
            while uploaded_file.state.name == "PROCESSING":
                if time.time() - process_start > 60:
                    logger.error(f"[UPLOAD] Timeout after 60s ({check_count} checks)")
                    st.error("❌ Upload timeout - please try a smaller file")
                    return None
                time.sleep(0.5)
                check_count += 1
                uploaded_file = client.files.get(name=uploaded_file.name)
            process_time = time.time() - process_start
            logger.info(f"[UPLOAD] File processing completed in {process_time:.2f}s ({check_count} checks)")
            
            if uploaded_file.state.name == "FAILED":
                logger.error(f"[UPLOAD] Upload failed with state: {uploaded_file.state.name}")
                st.error("❌ Upload failed - please try reloading the CSV")
                return None
            
            total_time = time.time() - upload_start
            logger.info(f"[UPLOAD] ✅ Total upload time: {total_time:.2f}s (file: {uploaded_file.name})")
            return uploaded_file
            
        except Exception as e:
            logger.error(f"[UPLOAD] Error: {str(e)}", exc_info=True)
            try:
                if 'csv_path' in locals():
                    os.unlink(csv_path)
            except Exception:
                pass
            return None
