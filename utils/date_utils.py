"""
Date and time utilities
"""
from datetime import datetime, timedelta
from typing import Optional


def format_date(date_str: str, format: str = "%B %d, %Y") -> str:
    """
    Format date string to human-readable format
    
    Args:
        date_str: Date in YYYY-MM-DD format
        format: Output format (default: "January 15, 2024")
    
    Returns:
        Formatted date string
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime(format)
    except:
        return date_str


def format_datetime(date_str: str, time_str: str) -> str:
    """
    Format date and time to readable format
    
    Args:
        date_str: Date in YYYY-MM-DD format
        time_str: Time in HH:MM format
    
    Returns:
        Formatted datetime string (e.g., "Jan 15, 2024 at 10:30 AM")
    """
    try:
        datetime_str = f"{date_str} {time_str}"
        dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except:
        return f"{date_str} {time_str}"


def time_ago(date_str: str) -> str:
    """
    Get human-readable time ago
    
    Args:
        date_str: Date in YYYY-MM-DD format
    
    Returns:
        Time ago string (e.g., "2 days ago", "3 months ago")
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        now = datetime.now()
        diff = now - date_obj
        
        if diff.days == 0:
            return "Today"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif diff.days < 365:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
    except:
        return date_str


def get_current_date() -> str:
    """Get current date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")


def get_current_time() -> str:
    """Get current time in HH:MM format"""
    return datetime.now().strftime("%H:%M")


def get_current_datetime() -> str:
    """Get current datetime in YYYY-MM-DD HH:MM:SS format"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def is_valid_date(date_str: str) -> bool:
    """Check if date string is valid"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string to datetime object"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None