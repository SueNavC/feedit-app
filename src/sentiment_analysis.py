"""
This module contains the functions to analyze the sentiment of a comment.
"""

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Polarity analysis with keywords
def analyze_sentiment_keywords(comment: str) -> str:
    """
    This function analyzes the sentiment of a comment based on the presence of certain keywords
    :param comment:
    :return: "positive" if the comment contains "good" or "great", "negative" if it contains "bad" or "terrible", "neutral" otherwise
    """
    if "good" in comment.lower() or "great" in comment.lower():
        return "positive"
    elif "bad" in comment.lower() or "terrible" in comment.lower():
        return "negative"
    return "neutral"

# Polarity analysis with TextBlob
def analyze_sentiment_textblob(comment: str) -> str:
    """
    This function analyzes the sentiment of a comment using TextBlob
    :param comment:
    :return: "positive" if the polarity is greater than 0, "negative" if the polarity is less than 0, "neutral" otherwise
    """
    analysis = TextBlob(comment)
    polarity = analysis.sentiment.polarity
    if polarity > 0:
        return "positive"
    elif polarity < 0:
        return "negative"
    return "neutral"

# Polarity analysis with VADER
def analyze_sentiment_vader(comment: str) -> str:
    """
    This function analyzes the sentiment of a comment using VADER
    :param comment:
    :return: "positive" if the compound score is greater than 0.05, "negative" if the compound score is less than -0.05, "neutral" otherwise
    """
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(comment)["compound"]
    if score >= 0.05:
        return "positive"
    elif score <= -0.05:
        return "negative"
    return "neutral"