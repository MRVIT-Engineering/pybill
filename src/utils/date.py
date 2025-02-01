from datetime import datetime, timedelta

def get_first_day_of_month(month: str) -> str:
    """
    Convert month string (e.g., 'January', 'Feb', '03') to first day of that month.
    Returns date in format YYYY-MM-DD
    """
    try:
        # Try parsing as month name or abbreviation
        date = datetime.strptime(month, '%B')  # Full month name
    except ValueError:
        try:
            date = datetime.strptime(month, '%b')  # Abbreviated month name
        except ValueError:
            # Try parsing as month number
            date = datetime.strptime(month, '%m')
    
    # Get current year and set it
    current_year = datetime.now().year
    first_day = date.replace(year=current_year)
    
    return first_day.strftime('%Y-%m-%d')

def get_last_day_of_month(month: str) -> str:
    """
    Get the last day of the specified month.
    Returns date in format YYYY-MM-DD
    """
    first_day = datetime.strptime(get_first_day_of_month(month), '%Y-%m-%d')
    
    if first_day.month == 12:
        next_month = first_day.replace(year=first_day.year + 1, month=1)
    else:
        next_month = first_day.replace(month=first_day.month + 1)
    
    last_day = next_month - timedelta(days=1)
    return last_day.strftime('%Y-%m-%d')
