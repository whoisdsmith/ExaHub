"""
Similarity Service for Exa API

This service implements similarity search functionality using the Exa API.
"""
from datetime import datetime
from typing import List, Optional, Any
import os
import logging
import requests
try:
    from exa import Exa
except ImportError:
    # Fallback to exa_py for backward compatibility
    try:
        from exa_py import Exa
    except ImportError:
        raise ImportError(
            "Neither 'exa' nor 'exa_py' package is installed. "
            "Please install one of them using: pip install exa-py or pip install exa"
        )

logger = logging.getLogger(__name__)


class SimilarityService:
    """Service for handling similarity search operations with Exa API."""

    def __init__(self, exa_api_key: Optional[str] = None):
        """Initialize the similarity service with the Exa API key."""
        self.exa_api_key = exa_api_key or os.environ.get('EXA_API_KEY')
        self.exa_client = None

        if not self.exa_api_key:
            logger.warning(
                "Exa API key not provided. Exa search capabilities will be disabled.")
        else:
            # Initialize the Exa client
            self.exa_client = Exa(self.exa_api_key)

    def validate_api_key(self) -> bool:
        """Validate that the Exa API key is available."""
        if not self.exa_api_key:
            logger.error("Exa API key is required but not provided")
            return False
        return True

    def search_similar_content(
        self,
        prompt: str,
        num_results: int = 5,
        search_type: str = "neural",
        use_autoprompt: bool = True,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        content_types: Optional[List[str]] = None,
        language: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        text: bool = True,
        highlight: bool = False
    ) -> List[Any]:
        """
        Search for content similar to the user prompt using the Exa API.

        Args:
            prompt: The search query
            num_results: Number of results to return
            search_type: Type of search ('neural', 'keyword', or 'auto')
            use_autoprompt: Whether to use autoprompt to improve the query
            include_domains: List of domains to restrict search to
            exclude_domains: List of domains to exclude from search
            content_types: List of content types to include (html, pdf, doc, text)
            language: Language code to filter results
            start_date: Start date for publication date filter (YYYY-MM-DD)
            end_date: End date for publication date filter (YYYY-MM-DD)
            text: Whether to include text content in results
            highlight: Whether to highlight matching text

        Returns:
            A list of search result objects
        """
        # Validate API key
        if not self.validate_api_key():
            raise ValueError("Exa API key is required for similarity search")

        try:
            # Build search parameters
            params = {
                "type": search_type,
                "use_autoprompt": use_autoprompt,
                "num_results": num_results,
                "text": text,
                "highlight": highlight
            }

            # Add optional parameters
            if include_domains:
                params["include_domains"] = include_domains

            if exclude_domains:
                params["exclude_domains"] = exclude_domains

            if content_types:
                params["content_types"] = content_types

            if language:
                params["language"] = language

            if start_date:
                params["start_date"] = start_date

            if end_date:
                params["end_date"] = end_date

            # Execute search
            results = self.exa_client.search_and_contents(prompt, **params)
            return results.results
        except Exception as e:
            # Log the error
            logging.error(f"Error occurred during search: {e}")
            raise e

    def find_similar_links(
        self,
        url: str,
        num_results: int = 5,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        language: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        text_similarity: bool = True,
        text: bool = False
    ) -> List[Any]:
        """
        Find links similar to the provided URL using the Exa API.

        Args:
            url: The URL to find similar content for
            num_results: Number of results to return
            include_domains: List of domains to restrict search to
            exclude_domains: List of domains to exclude from search
            language: Language code to filter results
            start_date: Start date for publication date filter (YYYY-MM-DD)
            end_date: End date for publication date filter (YYYY-MM-DD)
            text_similarity: Whether to use text similarity
            text: Whether to include text content in results

        Returns:
            A list of similar URL result objects
        """
        try:
            # Build parameters
            params = {
                "num_results": num_results,
                "text": text
            }

            # Add optional parameters
            if include_domains:
                params["include_domains"] = include_domains

            if exclude_domains:
                params["exclude_domains"] = exclude_domains

            if language:
                params["language"] = language

            if start_date:
                params["start_date"] = start_date

            if end_date:
                params["end_date"] = end_date

            if text_similarity is not None:
                params["text_similarity"] = text_similarity

            # Execute search
            results = self.exa_client.find_similar(url=url, **params)
            return results.results
        except Exception as e:
            # Log the error
            logging.error(f"Error occurred while finding similar links: {e}")
            raise e

    def filter_results(
        self,
        results: List[Any],
        min_date: Optional[datetime] = None,
        max_date: Optional[datetime] = None,
        min_score: Optional[float] = None
    ) -> List[Any]:
        """
        Filter results based on date and score.

        Args:
            results: The results to filter
            min_date: Minimum publication date
            max_date: Maximum publication date
            min_score: Minimum relevance score

        Returns:
            A list of filtered result objects
        """
        if not results:
            return []

        filtered_results = []

        for result in results:
            # Check if result meets all filter criteria
            include = True

            # Filter by published date
            if min_date and hasattr(result, 'published_date') and result.published_date:
                try:
                    # Convert string date to datetime object
                    pub_date = datetime.strptime(
                        result.published_date, "%Y-%m-%d")
                    if pub_date < min_date:
                        include = False
                except (ValueError, TypeError):
                    # If date parsing fails, skip date filtering for this result
                    pass

            if max_date and hasattr(result, 'published_date') and result.published_date:
                try:
                    # Convert string date to datetime object
                    pub_date = datetime.strptime(
                        result.published_date, "%Y-%m-%d")
                    if pub_date > max_date:
                        include = False
                except (ValueError, TypeError):
                    # If date parsing fails, skip date filtering for this result
                    pass

            # Filter by score
            if min_score is not None and hasattr(result, 'score') and result.score < min_score:
                include = False

            if include:
                filtered_results.append(result)

        return filtered_results
