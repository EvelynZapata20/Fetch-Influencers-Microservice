def format_metric(metric_text: str) -> int:
    """
    Converts a metric string with K/M suffix to its numerical value.
    
    Args:
        metric_text (str): Text representation of a number, potentially with K or M suffix
        
    Returns:
        float: The numerical value after converting K/M multipliers
    """
    if not any(char.isdigit() for char in metric_text):  
        return 0  
    if 'K' in metric_text:
        return float(metric_text.replace('K', '')) * 1000
    elif 'M' in metric_text:
        return float(metric_text.replace('M', '')) * 1000000
    
    return float(metric_text)