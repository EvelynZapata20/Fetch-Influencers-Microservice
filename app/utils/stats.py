def calculate_averages(metrics: dict, total_videos: int) -> dict:
    """
    Calculates the average likes, comments, shares, and saves.

    Args:
        metrics (dict): Dictionary containing total values for each metric.
        total_videos (int): The total number of analyzed videos.

    Returns:
        dict: Dictionary with the average values of each metric.
    """
    total_videos = max(total_videos, 1)
    
    return {f"avg_{key}": value / total_videos for key, value in metrics.items()}
