# 🚀 ExaHub: Enhanced GitHub Search

<div align="center">

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub API](https://img.shields.io/badge/GitHub%20API-v3-orange.svg)](https://docs.github.com/en/rest)
[![Exa AI](https://img.shields.io/badge/Exa%20AI-1.0.6-purple.svg)](https://exa.ai)

<img src="https://via.placeholder.com/800x400?text=ExaHub" alt="ExaHub Banner" width="800px">

### Supercharge your GitHub searches with semantic AI

</div>

## ✨ Features

- 🔍 **Advanced GitHub Search** - Find repositories, code, issues, and users with GitHub's powerful search syntax
- 🧠 **AI-Powered Semantic Enhancement** - Leverage Exa's semantic AI to discover conceptually relevant results
- 🎯 **Customizable Filters** - Refine results with filters for language, stars, forks, dates, and more
- 💻 **Modern UI** - Beautiful and responsive interface built with Bootstrap 5
- 🔌 **RESTful API** - Seamlessly integrate search capabilities into your applications
- 🔗 **URL Similarity Search** - Find websites similar to any GitHub project
- 🌐 **Content Similarity Search** - Discover conceptually related content across the web
- 📊 **Rate Limiting** - Built-in protection against API abuse
- 📝 **Comprehensive Logging** - Detailed logs for monitoring and debugging

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- GitHub API token (recommended to avoid rate limits)
- Exa API key (required for semantic search capabilities)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/ExaHub.git
cd ExaHub
```

2. **Create and activate a virtual environment**

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:

```
GITHUB_TOKEN=your_github_token
EXA_API_KEY=your_exa_api_key
SECRET_KEY=a_secure_random_string
FLASK_ENV=development
```

5. **Start the application**

```bash
python run.py
```

6. **Open your browser**

Navigate to <http://localhost:5000> to start searching!

## 🧩 How It Works

ExaHub combines the power of GitHub's traditional search with Exa AI's semantic understanding:

1. Your search query is processed through the GitHub API to find exact matches
2. Exa AI enhances these results by identifying semantically related content
3. Results are ranked by relevance, with highlighted matches
4. Additional metadata enriches each result for better context

## 🔍 Search Capabilities

### GitHub Search Syntax

```
keyword                   # Search for a keyword
"exact phrase"            # Search for the exact phrase
repo:owner/name           # Filter by repository
user:username             # Filter by user
org:organization          # Filter by organization
language:python           # Filter by language
stars:>1000               # Repositories with more than 1000 stars
created:>2022-01-01       # Created after January 1, 2022
pushed:>2023-01-01        # Last updated after January 1, 2023
topic:machine-learning    # Filter by topic
is:public                 # Only public repositories
fork:true                 # Include forks
```

### Semantic Search

ExaHub integrates Exa AI to enhance search results by:

- Finding conceptually similar results beyond exact keyword matches
- Ranking results based on semantic relevance to your query
- Highlighting the most relevant sections of the code or text
- Discovering content that traditional keyword search might miss

## 🔌 API Usage

### Search Repositories

```python
import requests
import json

# Example search parameters
search_data = {
    "query": "machine learning",
    "type": "repositories",
    "language": "python",
    "stars": [100, null],  # Repos with at least 100 stars
    "topics": ["ai", "deep-learning"],
    "enhance_with_exa": true,
    "page": 1,
    "per_page": 10
}

# Send the request
response = requests.post(
    "http://localhost:5000/search/api",
    json=search_data,
    headers={"Content-Type": "application/json"}
)

# Process the results
results = response.json()
```

### Find Similar URLs

```python
# Find websites similar to a GitHub repository
url_data = {
    "url": "https://github.com/tensorflow/tensorflow",
    "num_results": 5
}

response = requests.post(
    "http://localhost:5000/api/similar-urls",
    data=url_data
)
```

### Similarity Search

```python
# Find content similar to a concept
similarity_data = {
    "prompt": "Transformer architecture for natural language processing",
    "num_results": 10,
    "search_type": "neural"
}

response = requests.post(
    "http://localhost:5000/api/similarity-search",
    data=similarity_data
)
```

## 🔧 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `GITHUB_TOKEN` | GitHub API token | None |
| `EXA_API_KEY` | Exa API key | None |
| `SECRET_KEY` | Flask secret key | 'dev' |
| `FLASK_ENV` | Environment (development/production) | 'development' |
| `HOST` | Server host | '0.0.0.0' |
| `PORT` | Server port | 5000 |
| `FLASK_CONFIG` | Configuration profile to use | 'default' |

## 🛠️ Project Structure

```
ExaHub/
├── app/                          # Application package
│   ├── __init__.py               # Flask app initialization
│   ├── config.py                 # Configuration settings
│   ├── routes/                   # Route definitions
│   │   ├── main.py               # Main/index routes
│   │   ├── search.py             # Search routes
│   │   └── api.py                # API routes
│   ├── models/                   # Data models
│   │   ├── search_params.py      # Search parameters model
│   │   └── search_result.py      # Search results model
│   ├── services/                 # Service layer
│   │   ├── search_service.py     # GitHub search service
│   │   └── similarity_service.py # Exa AI service
│   ├── static/                   # Static assets
│   └── templates/                # HTML templates
│       ├── base.html             # Base template
│       ├── index.html            # Home page
│       ├── results.html          # Search results
│       └── api_playground.html   # API testing page
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables
└── README.md                     # Project documentation
```

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
coverage run -m pytest
coverage report
```

### Rate Limiting

ExaHub includes built-in rate limiting to prevent API abuse:

- Global: 200 requests per day, 50 per hour
- Search API: 30 requests per minute
- Similarity search: 20 requests per minute
- Web interface: 60 searches per hour

### Logging

The application includes comprehensive logging:

- Development: Console logging at DEBUG level
- Production: Rotating file logs (10MB max size, 10 backups)
- Log location: `instance/logs/exahub.log`

## 🔑 Getting API Keys

### GitHub API Token

1. Go to [GitHub Developer Settings](https://github.com/settings/tokens)
2. Generate a new token with `repo` and `read:user` scopes
3. Copy the token to your `.env` file

### Exa API Key

1. Visit [Exa.ai](https://exa.ai) to sign up for an account
2. Navigate to your profile settings to create an API key
3. Add the key to your `.env` file

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [GitHub API](https://docs.github.com/en/rest) for repository search capabilities
- [Exa AI](https://exa.ai) for semantic search technology

---

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/yourusername">Dustin Smith</a></p>
  <p>
    <a href="https://github.com/yourusername/ExaHub/issues">Report Bug</a> •
    <a href="https://github.com/yourusername/ExaHub/issues">Request Feature</a>
  </p>
</div>
