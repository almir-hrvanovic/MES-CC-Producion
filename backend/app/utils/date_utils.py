"""
Date utility functions
"""
from datetime import datetime, date, timedelta
from typing import Optional


def parse_date_string(date_str: str) -> Optional[date]:
    """Parse date string in various formats"""
    if not date_str:
        return None
    
    formats = [
        "%Y-%m-%d",
        "%d.%m.%Y",
        "%d/%m/%Y",
        "%m/%d/%Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    
    return None


def format_date_for_display(date_obj: Optional[date]) -> Optional[str]:
    """Format date for display in UI"""
    if not date_obj:
        return None
    
    return date_obj.strftime("%d.%m.%Y")


def calculate_working_days(start_date: date, end_date: date) -> int:
    """Calculate number of working days between two dates (excluding weekends)"""
    if start_date > end_date:
        return 0
    
    working_days = 0
    current_date = start_date
    
    while current_date <= end_date:
        # Monday = 0, Sunday = 6
        if current_date.weekday() < 5:  # Monday to Friday
            working_days += 1
        current_date += timedelta(days=1)
    
    return working_days


def get_next_working_day(date_obj: date) -> date:
    """Get next working day (skip weekends)"""
    next_day = date_obj + timedelta(days=1)
    
    # If it's Saturday (5) or Sunday (6), move to Monday
    while next_day.weekday() >= 5:
        next_day += timedelta(days=1)
    
    return next_day


def is_working_day(date_obj: date) -> bool:
    """Check if date is a working day (Monday to Friday)"""
    return date_obj.weekday() < 5


def add_working_days(start_date: date, working_days: int) -> date:
    """Add working days to a date (skip weekends)"""
    current_date = start_date
    days_added = 0
    
    while days_added < working_days:
        current_date += timedelta(days=1)
        if is_working_day(current_date):
            days_added += 1
    
    return current_date