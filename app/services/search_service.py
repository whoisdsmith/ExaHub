import os
import requests
from typing import Dict, Any, Optional, List, Union
import logging
from exa_github_search.app.models.search_params import GitHubSearchParams
from exa_github_search.app.models.search_result import SearchResults, GitHubRepository, GitHubCodeResult, GitHubIssueResult, GitHubUserResult

logger = logging.getLogger(__name__)


class SearchService:
    """Service for handling search operations with GitHub and Exa APIs."""

    def __init__(self, github_token: Optional[str] = None, exa_api_key: Optional[str] = None):
        """Initialize the search service with API credentials."""
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        self.exa_api_key = exa_api_key or os.environ.get('EXA_API_KEY')

        if not self.github_token:
            logger.warning(
                "GitHub token not provided. GitHub API functionality will be limited.")

        if not self.exa_api_key:
            logger.warning(
                "Exa API key not provided. Exa search capabilities will be disabled.")

    def github_search(self, search_params: GitHubSearchParams, page: int = 1, per_page: int = 10) -> Optional[SearchResults]:
        """
        Perform a search using the GitHub API.

        Args:
            search_params: Search parameters object
            page: Page number for paginated results
            per_page: Number of results per page

        Returns:
            SearchResults or None if the request failed
        """
        if not search_params.query:
            logger.error("No search query provided")
            return None

        # Validate GitHub token
        if not self.github_token:
            logger.error(
                "GitHub API token not provided. Cannot perform GitHub search.")
            return None

        # Build the GitHub search URL
        search_type = search_params.type or "repositories"
        base_url = f"https://api.github.com/search/{search_type}"

        # Prepare headers
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }

        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"

        # Prepare parameters
        params = {
            "q": search_params.build_github_query(),
            "page": page,
            "per_page": per_page
        }

        try:
            response = requests.get(base_url, headers=headers, params=params)
            response.raise_for_status()

            data = response.json()
            return SearchResults.from_github_api(
                data=data,
                search_type=search_type,
                query=search_params.query,
                page=page,
                per_page=per_page
            )

        except requests.exceptions.RequestException as e:
            logger.error(f"Error during GitHub API request: {e}")
            return None

    def exa_search(self, query: str, num_results: int = 10) -> Optional[List[Dict[str, Any]]]:
        """
        Perform a semantic search using the Exa API.

        Args:
            query: Search query
            num_results: Number of results to return

        Returns:
            List of search results or None if the request failed
        """
        if not self.exa_api_key:
            logger.error("Exa API key not provided")
            return None

        headers = {
            "x-api-key": self.exa_api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "query": query,
            "numResults": num_results,
            "useAutoprompt": True
        }

        try:
            response = requests.post(
                "https://api.exa.ai/search",
                headers=headers,
                json=payload
            )
            response.raise_for_status()

            return response.json().get("results", [])

        except requests.exceptions.RequestException as e:
            logger.error(f"Error during Exa API request: {e}")
            return None

    def combined_search(self, search_params: GitHubSearchParams, page: int = 1, per_page: int = 10,
                        enhance_with_exa: bool = True) -> Optional[SearchResults]:
        """
        Perform a combined search using both GitHub and Exa APIs.

        Args:
            search_params: Search parameters object
            page: Page number for paginated results
            per_page: Number of results per page
            enhance_with_exa: Whether to enhance results with Exa API

        Returns:
            Enhanced SearchResults or None if both searches failed
        """
        # First, perform the GitHub search
        github_results = self.github_search(search_params, page, per_page)

        # If GitHub search failed or no Exa enhancement requested, return GitHub results
        if not github_results or not enhance_with_exa or not self.exa_api_key:
            return github_results

        # Perform Exa search to enhance results
        exa_results = self.exa_search(
            search_params.query, num_results=per_page)

        if not exa_results:
            return github_results

        # Process results based on search type
        if search_params.type == "repositories":
            self._enhance_repository_results(github_results, exa_results)
        elif search_params.type == "code":
            self._enhance_code_results(github_results, exa_results)
        elif search_params.type == "issues":
            self._enhance_issue_results(github_results, exa_results)
        elif search_params.type == "users":
            self._enhance_user_results(github_results, exa_results)

        return github_results

    def _enhance_repository_results(self, github_results: SearchResults, exa_results: List[Dict[str, Any]]):
        """Enhance repository search results with Exa data."""
        for repo in github_results.repositories:
            # Find matching repository in Exa results by URL or name
            for exa_result in exa_results:
                if (exa_result.get("url") == repo.html_url or
                        repo.full_name.lower() in exa_result.get("url", "").lower()):

                    repo.relevance_score = exa_result.get("score")
                    repo.semantic_similarity = exa_result.get("similarity", 0)
                    repo.exa_content = exa_result.get("text")
                    break

    def _enhance_code_results(self, github_results: SearchResults, exa_results: List[Dict[str, Any]]):
        """Enhance code search results with Exa data."""
        for code in github_results.code_results:
            # Find matching code in Exa results by URL
            for exa_result in exa_results:
                if code.html_url == exa_result.get("url"):
                    code.relevance_score = exa_result.get("score")
                    code.semantic_similarity = exa_result.get("similarity", 0)
                    code.exa_content = exa_result.get("text")
                    break

    def _enhance_issue_results(self, github_results: SearchResults, exa_results: List[Dict[str, Any]]):
        """Enhance issue search results with Exa data."""
        for issue in github_results.issues:
            # Find matching issue in Exa results by URL
            for exa_result in exa_results:
                if issue.html_url == exa_result.get("url"):
                    issue.relevance_score = exa_result.get("score")
                    issue.semantic_similarity = exa_result.get("similarity", 0)
                    issue.exa_content = exa_result.get("text")
                    break

    def _enhance_user_results(self, github_results: SearchResults, exa_results: List[Dict[str, Any]]):
        """Enhance user search results with Exa data."""
        for user in github_results.users:
            # Find matching user in Exa results by URL
            for exa_result in exa_results:
                if user.html_url == exa_result.get("url"):
                    user.relevance_score = exa_result.get("score")
                    user.semantic_similarity = exa_result.get("similarity", 0)
                    user.exa_content = exa_result.get("text")
                    break
