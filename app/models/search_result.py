from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class GitHubRepository:
    """Model for GitHub repository search results."""
    id: int
    name: str
    full_name: str
    html_url: str
    description: Optional[str] = None
    owner: Dict[str, Any] = field(default_factory=dict)

    # Repository stats
    stargazers_count: int = 0
    watchers_count: int = 0
    forks_count: int = 0
    open_issues_count: int = 0

    # Repository details
    language: Optional[str] = None
    topics: List[str] = field(default_factory=list)
    license: Optional[Dict[str, Any]] = None

    # Dates
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    pushed_at: Optional[str] = None

    # Additional flags
    fork: bool = False
    archived: bool = False
    disabled: bool = False
    is_template: bool = False

    # Exa analysis
    relevance_score: Optional[float] = None
    semantic_similarity: Optional[float] = None
    exa_content: Optional[str] = None

    @classmethod
    def from_github_api(cls, data: Dict[str, Any]):
        """Create a repository object from GitHub API data."""
        return cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            full_name=data.get('full_name', ''),
            html_url=data.get('html_url', ''),
            description=data.get('description'),
            owner=data.get('owner', {}),
            stargazers_count=data.get('stargazers_count', 0),
            watchers_count=data.get('watchers_count', 0),
            forks_count=data.get('forks_count', 0),
            open_issues_count=data.get('open_issues_count', 0),
            language=data.get('language'),
            topics=data.get('topics', []),
            license=data.get('license'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            pushed_at=data.get('pushed_at'),
            fork=data.get('fork', False),
            archived=data.get('archived', False),
            disabled=data.get('disabled', False),
            is_template=data.get('is_template', False)
        )


@dataclass
class GitHubCodeResult:
    """Model for GitHub code search results."""
    name: str
    path: str
    sha: str
    url: str
    html_url: str
    repository: Dict[str, Any]
    score: float

    # Additional fields
    text_matches: List[Dict[str, Any]] = field(default_factory=list)

    # Exa analysis
    relevance_score: Optional[float] = None
    semantic_similarity: Optional[float] = None
    exa_content: Optional[str] = None

    @classmethod
    def from_github_api(cls, data: Dict[str, Any]):
        """Create a code result object from GitHub API data."""
        return cls(
            name=data.get('name', ''),
            path=data.get('path', ''),
            sha=data.get('sha', ''),
            url=data.get('url', ''),
            html_url=data.get('html_url', ''),
            repository=data.get('repository', {}),
            score=data.get('score', 0.0),
            text_matches=data.get('text_matches', [])
        )


@dataclass
class GitHubIssueResult:
    """Model for GitHub issue search results."""
    id: int
    number: int
    title: str
    html_url: str
    state: str
    user: Dict[str, Any]
    body: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    closed_at: Optional[str] = None
    repository_url: Optional[str] = None
    labels: List[Dict[str, Any]] = field(default_factory=list)

    # Additional fields
    comments: int = 0
    pull_request: Optional[Dict[str, Any]] = None

    # Exa analysis
    relevance_score: Optional[float] = None
    semantic_similarity: Optional[float] = None
    exa_content: Optional[str] = None

    @classmethod
    def from_github_api(cls, data: Dict[str, Any]):
        """Create an issue result object from GitHub API data."""
        return cls(
            id=data.get('id', 0),
            number=data.get('number', 0),
            title=data.get('title', ''),
            html_url=data.get('html_url', ''),
            state=data.get('state', ''),
            user=data.get('user', {}),
            body=data.get('body'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at'),
            closed_at=data.get('closed_at'),
            repository_url=data.get('repository_url'),
            labels=data.get('labels', []),
            comments=data.get('comments', 0),
            pull_request=data.get('pull_request')
        )


@dataclass
class GitHubUserResult:
    """Model for GitHub user search results."""
    id: int
    login: str
    html_url: str
    type: str
    score: float

    # Additional fields
    name: Optional[str] = None
    company: Optional[str] = None
    blog: Optional[str] = None
    location: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    public_repos: int = 0
    public_gists: int = 0
    followers: int = 0
    following: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # Exa analysis
    relevance_score: Optional[float] = None
    semantic_similarity: Optional[float] = None
    exa_content: Optional[str] = None

    @classmethod
    def from_github_api(cls, data: Dict[str, Any]):
        """Create a user result object from GitHub API data."""
        return cls(
            id=data.get('id', 0),
            login=data.get('login', ''),
            html_url=data.get('html_url', ''),
            type=data.get('type', ''),
            score=data.get('score', 0.0),
            name=data.get('name'),
            company=data.get('company'),
            blog=data.get('blog'),
            location=data.get('location'),
            email=data.get('email'),
            bio=data.get('bio'),
            public_repos=data.get('public_repos', 0),
            public_gists=data.get('public_gists', 0),
            followers=data.get('followers', 0),
            following=data.get('following', 0),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )


@dataclass
class SearchResults:
    """Container for search results of all types."""
    query: str
    search_type: str
    total_count: int = 0

    # Results by type
    repositories: List[GitHubRepository] = field(default_factory=list)
    code_results: List[GitHubCodeResult] = field(default_factory=list)
    issues: List[GitHubIssueResult] = field(default_factory=list)
    users: List[GitHubUserResult] = field(default_factory=list)

    # Pagination
    page: int = 1
    per_page: int = 10
    has_next_page: bool = False

    @property
    def results(self):
        """Return the appropriate results based on the search type."""
        if self.search_type == "repositories":
            return self.repositories
        elif self.search_type == "code":
            return self.code_results
        elif self.search_type == "issues":
            return self.issues
        elif self.search_type == "users":
            return self.users
        return []

    @classmethod
    def from_github_api(cls, data: Dict[str, Any], search_type: str, query: str, page: int, per_page: int):
        """Create a search results object from GitHub API data."""
        results = cls(
            query=query,
            search_type=search_type,
            total_count=data.get('total_count', 0),
            page=page,
            per_page=per_page
        )

        # Calculate pagination
        results.has_next_page = results.total_count > page * per_page

        # Parse items based on search type
        items = data.get('items', [])

        if search_type == "repositories":
            results.repositories = [
                GitHubRepository.from_github_api(item) for item in items]
        elif search_type == "code":
            results.code_results = [
                GitHubCodeResult.from_github_api(item) for item in items]
        elif search_type == "issues":
            results.issues = [
                GitHubIssueResult.from_github_api(item) for item in items]
        elif search_type == "users":
            results.users = [GitHubUserResult.from_github_api(
                item) for item in items]

        return results
