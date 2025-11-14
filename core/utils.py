"""
Core utilities for the Super-Codex-AI system
"""
import hashlib
import secrets
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
import json
import logging


def generate_unique_id() -> str:
    """Generate a unique identifier"""
    return str(uuid.uuid4())


def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure random token"""
    return secrets.token_urlsafe(length)


def generate_hash(data: str, algorithm: str = "sha256") -> str:
    """Generate a hash of the given data"""
    if algorithm == "sha256":
        return hashlib.sha256(data.encode()).hexdigest()
    elif algorithm == "md5":
        return hashlib.md5(data.encode()).hexdigest()
    elif algorithm == "sha1":
        return hashlib.sha1(data.encode()).hexdigest()
    else:
        raise ValueError(f"Unsupported hashing algorithm: {algorithm}")


def get_utc_timestamp() -> datetime:
    """Get current UTC timestamp"""
    return datetime.now(timezone.utc)


def format_timestamp(timestamp: datetime, format_string: str = "%Y-%m-%d %H:%M:%S UTC") -> str:
    """Format a timestamp to a string"""
    return timestamp.strftime(format_string)


def parse_timestamp(timestamp_str: str, format_string: str = "%Y-%m-%d %H:%M:%S UTC") -> datetime:
    """Parse a timestamp string to datetime"""
    return datetime.strptime(timestamp_str, format_string).replace(tzinfo=timezone.utc)


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename by removing dangerous characters"""
    import re
    # Remove or replace dangerous characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    sanitized = re.sub(r'^\.+', '_', sanitized)  # Remove leading dots
    sanitized = sanitized.strip()
    return sanitized[:255] if sanitized else "unnamed_file"


def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate a string if it exceeds max_length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string, returning default on error"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def safe_json_dumps(data: Any, default: str = "{}") -> str:
    """Safely dump data to JSON string, returning default on error"""
    try:
        return json.dumps(data, default=str, ensure_ascii=False)
    except (TypeError, ValueError):
        return default


def extract_file_extension(filename: str) -> str:
    """Extract file extension from filename"""
    import os
    return os.path.splitext(filename)[1].lower()


def calculate_file_checksum(filepath: str, algorithm: str = "sha256") -> str:
    """Calculate checksum of a file"""
    hash_func = getattr(hashlib, algorithm)()
    
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")
    except PermissionError:
        raise PermissionError(f"Permission denied: {filepath}")


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """Set up a logger with the specified name and level"""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def chunks(lst: List[Any], chunk_size: int):
    """Yield successive chunks from a list"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def retry_with_backoff(func, max_retries: int = 3, backoff_factor: float = 1.0):
    """Retry a function with exponential backoff"""
    import time
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            wait_time = backoff_factor * (2 ** attempt)
            time.sleep(wait_time)


class Timer:
    """Context manager for timing operations"""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        print(f"{self.name} took {duration:.3f} seconds")
    
    @property
    def duration(self) -> float:
        """Get the duration in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0