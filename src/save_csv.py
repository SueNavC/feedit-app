"""
This Module for save the comments in a CSV file.
"""
# Save the comments in a CSV file.
# By Susana Navarro
# 25/10/2024

# Importing the necessary libraries
import csv
from datetime import datetime
from typing import List, Dict

# Function to save analyzed comments to a CSV file

def save_comments_csv(analyzed_comments: List[Dict[str, str]],
                      subreddit_id: List[int]) -> str:

    """
    Saves analyzed comments to a CSV file.
    :param analyzed_comments: A list of dictionaries.
    :param subreddit_id: The name of the subreddit.
    :return: The filename of the saved CSV file.
    """
    csv_filename = f"analyzed_comments_{subreddit_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"

    # Open the file in write mode
    # Create a CSV DictWriter object

    with open(csv_filename, mode="w",
              newline="",
              encoding="utf-8") as csv_file:

        writer = csv.DictWriter(csv_file,
                                fieldnames=["id", "timestamp", "text", "polarity"])
        writer.writeheader()
        writer.writerows(analyzed_comments)
    return csv_filename
