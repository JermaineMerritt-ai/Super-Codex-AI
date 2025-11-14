# Utility functions for Super-Codex-AI
import os
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import uuid

class CodexUtils:
    """Utility functions for the Codex system"""
    
    @staticmethod
    def generate_id() -> str:
        """Generate a unique ID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_timestamp() -> str:
        """Generate ISO format timestamp"""
        return datetime.now().isoformat()
    
    @staticmethod
    def hash_content(content: str) -> str:
        """Generate SHA-256 hash of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    @staticmethod
    def ensure_directory(path: str) -> None:
        """Ensure directory exists"""
        Path(path).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def load_json(file_path: str) -> Optional[Dict[str, Any]]:
        """Safely load JSON file"""
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON from {file_path}: {e}")
            return None
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str, indent: int = 2) -> bool:
        """Safely save JSON file"""
        try:
            # Ensure directory exists
            CodexUtils.ensure_directory(os.path.dirname(file_path))
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent)
            return True
        except Exception as e:
            print(f"Error saving JSON to {file_path}: {e}")
            return False
    
    @staticmethod
    def append_jsonl(data: Dict[str, Any], file_path: str) -> bool:
        """Append data to JSONL file"""
        try:
            # Ensure directory exists
            CodexUtils.ensure_directory(os.path.dirname(file_path))
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data) + '\n')
            return True
        except Exception as e:
            print(f"Error appending to JSONL file {file_path}: {e}")
            return False
    
    @staticmethod
    def read_jsonl(file_path: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Read JSONL file and return list of records"""
        if not os.path.exists(file_path):
            return []
        
        records = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if limit and i >= limit:
                        break
                    
                    try:
                        record = json.loads(line.strip())
                        records.append(record)
                    except json.JSONDecodeError:
                        continue  # Skip malformed lines
        except Exception as e:
            print(f"Error reading JSONL file {file_path}: {e}")
        
        return records
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe filesystem usage"""
        # Remove or replace unsafe characters
        unsafe_chars = '<>:"/\\|?*'
        for char in unsafe_chars:
            filename = filename.replace(char, '_')
        
        # Remove leading/trailing whitespace and periods
        filename = filename.strip(' .')
        
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename
    
    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"
    
    @staticmethod
    def get_file_info(file_path: str) -> Optional[Dict[str, Any]]:
        """Get file information"""
        if not os.path.exists(file_path):
            return None
        
        try:
            stat = os.stat(file_path)
            return {
                "size": stat.st_size,
                "size_formatted": CodexUtils.format_file_size(stat.st_size),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_file": os.path.isfile(file_path),
                "is_dir": os.path.isdir(file_path)
            }
        except Exception as e:
            print(f"Error getting file info for {file_path}: {e}")
            return None
    
    @staticmethod
    def validate_realm_id(realm_id: str) -> bool:
        """Validate realm ID format (e.g., PL-001, ST-007)"""
        if not realm_id or len(realm_id) != 6:
            return False
        
        if not realm_id[2] == '-':
            return False
        
        prefix = realm_id[:2]
        number = realm_id[3:]
        
        return prefix.isalpha() and number.isdigit()
    
    @staticmethod
    def validate_capsule_name(capsule: str) -> bool:
        """Validate capsule name"""
        if not capsule or len(capsule) < 3:
            return False
        
        # Basic validation - no special characters except spaces
        return capsule.replace(' ', '').replace('-', '').replace('_', '').isalnum()
    
    @staticmethod
    def generate_ceremony_id(realm: str) -> str:
        """Generate ceremonial operation ID"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        random_suffix = str(uuid.uuid4())[:8]
        return f"AXF-{date_str}-{random_suffix}".upper()
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text for processing"""
        if not text:
            return ""
        
        # Basic text cleaning
        text = text.strip()
        text = ' '.join(text.split())  # Normalize whitespace
        
        return text
    
    @staticmethod
    def paginate_results(results: List[Any], page: int = 1, 
                        per_page: int = 20) -> Dict[str, Any]:
        """Paginate results"""
        total = len(results)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        paginated = results[start_idx:end_idx]
        
        return {
            "items": paginated,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page,
                "has_next": end_idx < total,
                "has_prev": page > 1
            }
        }