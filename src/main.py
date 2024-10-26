# Project: Engineering Challenge
# Description: The task is to design and develop a microservice application that offers a RESTful API.
# This API will analyze comments within a given "subfeddit" (a mock Reddit category) to determine if the comments are positive or negative.
# By Susana Navarro
# 25/10/2024

# Importing the necessary libraries
from fastapi import FastAPI, Query
from typing import List, Dict, Optional
from src.sentiment_analysis import analyze_sentiment_keywords, analyze_sentiment_textblob, analyze_sentiment_vader
from datetime import datetime

# Creating the FastAPI app
app = FastAPI()


# Function to generate sample comments for a given subfeddit
def get_subfeddit_comments(subreddit_name: str) -> List[Dict]:
    """
    This function generates a list of 25 comments for the given subfeddit
    :param subreddit_name:
    :return: A list of 25 comments for the given subfeddit
    """
    comments = []
    for i in range(1, 26):  # Generate 25 comments
        comment_text = f"Comment {i} in {subreddit_name}. This is a sample comment."
        comments.append({
            "id": i,
            "text": comment_text,
            "timestamp": datetime(2024, 10, 25, 12, i % 60).isoformat() + "Z"  # Fixed timestamps for consistency
        })
    return comments


# Root endpoint to verify the API is running
@app.get("/")
async def root():
    return {"message": "Hello, Feddit API!"}


# Endpoint to analyze comments within a given subreddit
@app.post("/analyze/")
async def analyze_comments(
        subreddit_name: str,
        method: str = Query("keywords", enum=["keywords", "textblob", "vader"]),
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        sort_by_polarity: bool = False,
        limit: Optional[int] = 25
):
    # Get sample comments
    comments = get_subfeddit_comments(subreddit_name)

    # Filter and analyze comments
    analyzed_comments = []
    for comment in comments[:limit]:  # Apply limit to number of comments
        comment_timestamp = datetime.fromisoformat(comment["timestamp"].replace("Z", ""))

        # Filter comments by date range if specified
        if start_date and comment_timestamp < start_date:
            continue
        if end_date and comment_timestamp > end_date:
            continue

        # Sentiment analysis
        if method == "keywords":
            polarity = analyze_sentiment_keywords(comment["text"])
        elif method == "textblob":
            polarity = analyze_sentiment_textblob(comment["text"])
        elif method == "vader":
            polarity = analyze_sentiment_vader(comment["text"])
        else:
            polarity = "unknown"

        analyzed_comments.append({
            "id": comment["id"],
            "text": comment["text"],
            "timestamp": comment["timestamp"],
            "polarity": polarity
        })

    # Sort by polarity if enabled
    if sort_by_polarity:
        analyzed_comments.sort(key=lambda x: x["polarity"], reverse=True)

    return {"comments": analyzed_comments}
