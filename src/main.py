# Project: Engineering Challenge
# Description: The task is to design and develop a microservice application that offers a RESTful API.
# This API will analyze comments within a given "subfeddit" (a mock Reddit category) to determine if the comments are positive or negative.
# By Susana Navarro
# 25/10/2024


# Importing the necessary libraries
from fastapi import FastAPI, Query
from sentiment_analysis import analyze_sentiment_keywords, analyze_sentiment_textblob, analyze_sentiment_vader

# Creating the FastAPI app
app = FastAPI()

# Defining the root endpoint
@app.get("/")
async def root():
    return {"message": "Hello, Feddit API!"}

# Defining the analyze endpoint
@app.post("/analyze/")
async def analyze_comment(comment: str, method: str = Query("textblob", enum=["keywords", "textblob", "vader"])):
    if method == "keywords":
        polarity = analyze_sentiment_keywords(comment)
    elif method == "textblob":
        polarity = analyze_sentiment_textblob(comment)
    elif method == "vader":
        polarity = analyze_sentiment_vader(comment)
    else:
        polarity = "unknow" #Valor predeterminado
    return {"comment": comment, "polarity": polarity, "method": method}
