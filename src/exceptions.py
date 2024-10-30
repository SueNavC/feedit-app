"""
This is exception handling module.
"""
# Importing the necessary libraries
# src/exceptions.py
from fastapi import HTTPException, status

# Custom exception for handling errors during data ingestion
class CommentAnalysisException(HTTPException):

    def __init__(self, detail: str = "An error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail)
