import os

def retrieve_timelapse(date_str):
    """
    Retrieve the timelapse video for the given date.
    
    Args:
        date_str (str): The selected date in 'YYYY-MM-DD' format.
        
    Returns:
        str: The path to the timelapse video file if it exists, or None if it doesn't exist.
    """
    formatted_date = date_str.replace('-', '_')
    video_filename = f'timelapse_{formatted_date}.mp4'
    video_folder = os.path.join('static', 'videos')
    video_path = os.path.join(video_folder, video_filename)
    
    if os.path.exists(video_path):
        return video_path
    else:
        return None