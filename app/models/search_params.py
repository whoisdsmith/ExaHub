from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict, Any


@dataclass
class GitHubSearchParams:
    """Model for GitHub advanced search parameters."""

    def __init__(self, query: str, type: str = "repositories", language: Optional[str] = None,
                 stars: Optional[Tuple[Optional[int], Optional[int]]] = None,
                 forks: Optional[Tuple[Optional[int], Optional[int]]] = None,
                 created: Optional[str] = None, pushed: Optional[str] = None,
                 user: Optional[str] = None, org: Optional[str] = None,
                 is_public: bool = True, include_forks: bool = False,
                 topics: Optional[List[str]] = None, subtopics: Optional[List[str]] = None,
                 tags: Optional[List[str]] = None, exclude_topics: Optional[List[str]] = None):
        """
        Initialize search parameters.

        Args:
            query: The search query
            type: Type of search (repositories, code, issues, users)
            language: Programming language filter
            stars: Tuple of (min_stars, max_stars)
            forks: Tuple of (min_forks, max_forks)
            created: Creation date filter (e.g., >2022-01-01)
            pushed: Last update date filter (e.g., >2023-01-01)
            user: Filter by username
            org: Filter by organization
            is_public: Whether to only include public repositories
            include_forks: Whether to include forked repositories
            topics: List of topics to include in search
            subtopics: List of subtopics to include in search
            tags: List of tags to include in search
            exclude_topics: List of topics to exclude from search
        """
        self.query = query
        self.type = type
        self.language = language
        self.stars = stars
        self.forks = forks
        self.created = created
        self.pushed = pushed
        self.user = user
        self.org = org
        self.is_public = is_public
        self.include_forks = include_forks
        self.topics = topics or []
        self.subtopics = subtopics or []
        self.tags = tags or []
        self.exclude_topics = exclude_topics or []

    def build_github_query(self) -> str:
        """
        Build a GitHub search query string based on the parameters.

        Returns:
            GitHub search query string
        """
        components = []

        # Add main query
        if self.query:
            components.append(self.query)

        # Add type-specific qualifiers
        if self.language:
            components.append(f"language:{self.language}")

        if self.stars:
            min_stars, max_stars = self.stars
            if min_stars is not None and max_stars is not None:
                components.append(f"stars:{min_stars}..{max_stars}")
            elif min_stars is not None:
                components.append(f"stars:>={min_stars}")
            elif max_stars is not None:
                components.append(f"stars:<={max_stars}")

        if self.forks:
            min_forks, max_forks = self.forks
            if min_forks is not None and max_forks is not None:
                components.append(f"forks:{min_forks}..{max_forks}")
            elif min_forks is not None:
                components.append(f"forks:>={min_forks}")
            elif max_forks is not None:
                components.append(f"forks:<={max_forks}")

        if self.created:
            components.append(f"created:{self.created}")

        if self.pushed:
            components.append(f"pushed:{self.pushed}")

        if self.user:
            components.append(f"user:{self.user}")

        if self.org:
            components.append(f"org:{self.org}")

        # Add visibility qualifier
        if self.is_public:
            components.append("is:public")

        # Add fork qualifier
        if not self.include_forks:
            components.append("fork:false")

        # Add topic qualifiers
        for topic in self.topics:
            components.append(f"topic:{topic}")

        # Add subtopic qualifiers as part of topics with specific prefixes
        for subtopic in self.subtopics:
            components.append(f"topic:subtopic-{subtopic}")

        # Add tag qualifiers
        for tag in self.tags:
            components.append(f"topic:tag-{tag}")

        # Add excluded topics
        for topic in self.exclude_topics:
            components.append(f"-topic:{topic}")

        return " ".join(components)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert search parameters to a dictionary.

        Returns:
            Dictionary representation of search parameters
        """
        return {
            "query": self.query,
            "type": self.type,
            "language": self.language,
            "stars": self.stars,
            "forks": self.forks,
            "created": self.created,
            "pushed": self.pushed,
            "user": self.user,
            "org": self.org,
            "is_public": self.is_public,
            "include_forks": self.include_forks,
            "topics": self.topics,
            "subtopics": self.subtopics,
            "tags": self.tags,
            "exclude_topics": self.exclude_topics
        }
