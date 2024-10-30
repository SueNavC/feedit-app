"""
This Module for ingesting data from ProgreSQL database.
"""
# Ingests data from a PostgreSQL database.
# By Susana Navarro
# 25/10/2024

# Importing the necessary libraries
import psycopg2
from typing import List, Dict

# Function to fetch comments from a PostgreSQL database

def fetch_comments(subfeddit_id: list,
                   after: int,
                   before: int,
                   limit: int = 25,
                   keyword: str = None) -> List[Dict]:


    """
    Fetches recent comments from a PostgreSQL database.
    :param subfeddit_id: The ID of the subreddit to fetch comments from.
    :param after: Fetch comments after this date (epoch timestamp).
    :param before: Fetch comments before this date (epoch timestamp).
    :param limit: The maximum number of comments to retrieve.
    :param keyword: A keyword to filter comments.
    :return: A list of dictionaries containing the fetched comments.
    """
    cursor = None
    conn = None
    try:
        # connect to the database
        conn = psycopg2.connect(
            port="5434",  # Mapping local port
            database="postgres",
            user="postgres",
            password="mysecretpassword"
        )
        cursor = conn.cursor()
        print("Connection successful!")
        # Connect to the database
        query = """
            SELECT id, text, created_at
            FROM comment
            WHERE subfeddit_id = ANY(%s)
              AND created_at >= %s
              AND created_at <= %s
        """

        params = [subfeddit_id, after, before]

        if keyword:
            query += " AND text ILIKE %s"
            params.append(f"%{keyword}%")

        query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)

        print("Executing query with params:", params)
        # Query execution
        cursor.execute(query, tuple(params))
        fetched_comments = [
            {"id": row[0], "text": row[1], "created_at": row[2]}
            for row in cursor.fetchall()]
        print(f"Found {len(fetched_comments)} comments")
        return fetched_comments

    except Exception as e:
        print(f"Error during data fetching: {e}")
        returns = []
        # Return an empty list in case of an error

    finally:
        # Safely close the cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
