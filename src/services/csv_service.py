"""
CSV service for loading and processing CSV files.
"""

import pandas as pd
import streamlit as st
from typing import Union, Optional
from logger_config import get_logger

logger = get_logger(__name__)


class CSVService:
    """Handles CSV file loading and processing."""
    
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
            # Check if it's an uploaded file or a URL string
            if isinstance(file_or_url, str):
                # It's a URL
                logger.info(f"Loading CSV from URL (length: {len(file_or_url)} chars)")
                
                if not file_or_url.strip():
                    logger.warning("Empty URL provided")
                    st.error("❌ Please provide a valid URL")
                    return None
                
                # Attempt to load from URL
                df = pd.read_csv(file_or_url)
                logger.info(f"CSV loaded successfully from URL: {df.shape[0]} rows, {df.shape[1]} columns")
                
            else:
                # It's an uploaded file
                logger.info(f"Loading CSV from uploaded file: {file_or_url.name}")
                
                # Read the uploaded file
                df = pd.read_csv(file_or_url)
                logger.info(f"CSV loaded successfully from file: {df.shape[0]} rows, {df.shape[1]} columns")
            
            # Validate the DataFrame
            if df.empty:
                logger.warning("Loaded CSV is empty")
                st.error("❌ The CSV file is empty")
                return None
            
            # Check for reasonable size (prevent memory issues)
            if df.shape[0] > 1000:
                logger.warning(f"Large CSV detected: {df.shape[0]} rows")
                st.warning(f"⚠️ Large file detected: {df.shape[0]:,} rows. This may affect performance.")
            
            return df
            
        except pd.errors.ParserError as e:
            logger.error(f"CSV parsing error: {str(e)}", exc_info=True)
            st.error(f"❌ **CSV Parsing Error**\n\nThe file could not be parsed as a valid CSV.\n\nDetails: {str(e)}")
            return None
            
        except pd.errors.EmptyDataError as e:
            logger.error(f"Empty data error: {str(e)}", exc_info=True)
            st.error("❌ **Empty File**\n\nThe CSV file contains no data.")
            return None
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}", exc_info=True)
            st.error("❌ **File Not Found**\n\nThe specified file could not be found.")
            return None
            
        except pd.errors.ParserError as e:
            logger.error(f"URL fetch error: {str(e)}", exc_info=True)
            st.error(f"❌ **URL Error**\n\nCould not fetch data from the URL.\n\nPlease check:\n- URL is correct\n- URL is accessible\n- File is a valid CSV\n\nDetails: {str(e)}")
            return None
            
        except ValueError as e:
            logger.error(f"Value error loading CSV: {str(e)}", exc_info=True)
            st.error(f"❌ **Invalid Data**\n\n{str(e)}")
            return None
            
        except Exception as e:
            logger.error(f"Unexpected error loading CSV: {str(e)}", exc_info=True)
            st.error(f"❌ **Error Loading CSV**\n\nAn unexpected error occurred.\n\nDetails: {str(e)}")
            return None
    
    @staticmethod
    def get_dataframe_info(df: pd.DataFrame) -> dict:
        """
        Get summary information about a DataFrame.
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Dictionary with DataFrame information
        """
        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": list(df.columns),
            "dtypes": df.dtypes.to_dict(),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "has_nulls": df.isnull().any().any()
        }
    
    @staticmethod
    def format_dataframe_summary(df: pd.DataFrame) -> str:
        """
        Format a human-readable summary of the DataFrame.
        
        Args:
            df: Pandas DataFrame
            
        Returns:
            Formatted string summary
        """
        info = CSVService.get_dataframe_info(df)
        
        summary = f"""
**Dataset Summary:**
- 📊 **Rows:** {info['rows']:,}
- 📋 **Columns:** {info['columns']}
- 💾 **Memory:** {info['memory_usage'] / 1024:.2f} KB
- ❓ **Has Missing Values:** {'Yes' if info['has_nulls'] else 'No'}

**Columns:** {', '.join(info['column_names'])}
        """
        
        return summary.strip()
    
    @staticmethod
    def generate_context_for_ai(df: pd.DataFrame, max_rows: int = 1000) -> str:
        """
        Generate a comprehensive context string from a DataFrame for AI analysis.
        
        This method creates a detailed text representation of the CSV data
        that can be sent to an AI model for analysis and question answering.
        
        Gemini-2.5-pro accepts 250,000 tokens per minute, so we can safely
        send large datasets (default: 1,000 rows).
        
        Args:
            df: Pandas DataFrame to generate context from
            max_rows: Maximum number of rows to include (default: 1000)
            
        Returns:
            Formatted string with complete dataset information
        """
        import io
        
        # Get basic info
        rows, cols = df.shape
        columns = list(df.columns)
        dtypes = df.dtypes.to_dict()
        
        # Capture df.info() output
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        
        # Determine how many rows to send
        rows_to_send = min(rows, max_rows)
        
        # Build comprehensive context
        context = f"""You are a helpful data analyst. A user has loaded a CSV, and they want to ask questions about it.

Here is the data's schema and summary statistics:

**Dataset Overview:**
- Total Rows: {rows:,}
- Columns: {cols}
- Column Names: {', '.join(columns)}

**Data Schema (df.info()):**
```
{info_str}
```

**Statistical Summary (df.describe()):**
```
{df.describe().to_string()}
```

**First 3 Rows (df.head(3)):**
```
{df.head(3).to_string()}
```

**Complete Dataset ({rows_to_send:,} of {rows:,} rows):**
```
{df.head(rows_to_send).to_string()}
```
"""
        
        # Add missing values information - ALWAYS include this section
        missing = df.isnull().sum()
        context += "\n**Missing Values Analysis:**\n"
        if missing.any():
            # Sort by count descending to show most missing first
            missing_sorted = missing[missing > 0].sort_values(ascending=False)
            for col, count in missing_sorted.items():
                context += f"- {col}: {count} missing values ({count/rows*100:.1f}%)\n"
        else:
            context += "- No missing values found in any column\n"
        
        # Add note if dataset was truncated
        if rows > max_rows:
            context += f"\n**Note:** Dataset truncated to {max_rows:,} rows for AI analysis. Full dataset has {rows:,} rows.\n"
        
        return context
