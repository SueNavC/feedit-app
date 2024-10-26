import unittest
from sentiment_analysis import analyze_sentiment_keywords, analyze_sentiment_textblob, analyze_sentiment_vader


class TestSentimentAnalysis(unittest.TestCase):
    """
    This class contains the unit tests for the sentiment analysis functions.
    """

    # Test for the keyword-based sentiment analysis function
    def test_analyze_sentiment_keywords(self):
        self.assertEqual(analyze_sentiment_keywords("This is a good product"), "positive")
        self.assertEqual(analyze_sentiment_keywords("This is a bad product"), "negative")

    # Test for the TextBlob sentiment analysis function
    def test_analyze_sentiment_textblob(self):
        self.assertEqual(analyze_sentiment_textblob("I love this!"), "positive")
        self.assertEqual(analyze_sentiment_textblob("I hate this!"), "negative")

    # Test for the VADER sentiment analysis function
    def test_analyze_sentiment_vader(self):
        self.assertEqual(analyze_sentiment_vader("Absolutely fantastic experience!"), "positive")
        self.assertEqual(analyze_sentiment_vader("This was terrible..."), "negative")


if __name__ == '__main__':
    unittest.main()
