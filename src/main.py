# Project: Engineering Challenge
# Description: The task is to design and develop a microservice application that offers a FAST API.
### This API will analyze comments within a given subfeddit (a mock Reddit category) to determine
### if the comments are positive or negative.
#Alternative2: NO use a database to store and retrieve comments for the subfeddit.

# By Susana Navarro
# 25/10/2024

from datetime import datetime, timezone
from typing import Optional, List, Dict, Literal
from src.data_ingestion import fetch_comments
from fastapi import FastAPI, Query, HTTPException

from src.save_csv import save_comments_csv
from src.sentiment_analysis import (analyze_sentiment_keywords,
                                    analyze_sentiment_textblob,
                                    analyze_sentiment_vader)

# Creating the FastAPI app
app = FastAPI()

# Root endpoint to verify the API is running
@app.get("/")
async def root():
    return {"message": "Hello, Feddit API!"}


# Endpoint to get the version of the API
@app.get("/api/v1/version")
async def get_version():
    return {"version": "0.1.0"}

# Endpoint to analyze comments within a given subreddit
@app.post("/analyze/")
async def analyze_comments(
    subfeddit_id: Optional[List[int]] = None,
    method: Literal["keywords", "textblob", "vader"] = Query(...),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    sort_by_polarity: bool = False,
    limit: int = 25,
    keyword: Optional[str] = None,
    save_to_csv: bool = False
):
    if subfeddit_id is None:
        subfeddit_id = [1, 2, 3]  # Default subfeddit IDs

    print(
        f"Parameters received - subfeddit_id: {subfeddit_id}, "
        f"method: {method}, "
        f"start_date: {start_date}, "
        f"end_date: {end_date}, "
        f"sort_by_polarity: {sort_by_polarity},"
        f" limit: {limit}, "
        f"keyword: {keyword}, "
        f"save_to_csv: {save_to_csv}"
    )

    try:
        # Convert start_date and end_date to epoch format for the API
        after = int(start_date.timestamp()) if start_date else int(datetime.now().timestamp() - 86400)
        before = int(end_date.timestamp()) if end_date else int(datetime.now().timestamp())

        # Fetch comments from the subreddit
        comments = fetch_comments(
            subfeddit_id=subfeddit_id,
            after=after,
            before=before,
            limit=limit,
            keyword=keyword
        )
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Analyze comments based on the specified method
    analyzed_comments = []
    for comment in comments:
        # Check for required fields in comment dictionary
        if not all(key in comment for key in ["id", "text", "created_at"]):
            raise HTTPException(status_code=500, detail="Invalid data format in comments")

        # Ensure text analysis based on method
        if method == "keywords":
            polarity = analyze_sentiment_keywords(comment["text"])
        elif method == "textblob":
            polarity = analyze_sentiment_textblob(comment["text"])
        elif method == "vader":
            polarity = analyze_sentiment_vader(comment["text"])
        else:
            polarity = "unknown" # Default to unknown if method is not recognized

        # Append analyzed comment to the list
        analyzed_comments.append({
            "id": comment["id"],
            "text": comment["text"],
            "timestamp": datetime.fromtimestamp(comment["created_at"], tz=timezone.utc).isoformat(),
            "polarity": polarity
        })
    # Sort comments by polarity if specified
    if sort_by_polarity:
        analyzed_comments.sort(key=lambda x: x["polarity"], reverse=True)

    # Save to CSV if requested
    if save_to_csv:
        csv_filename = save_comments_csv(analyzed_comments, subfeddit_id)
        return {"comments": analyzed_comments, "csv_file": csv_filename}

    return {"comments": analyzed_comments}