from flask import Blueprint, render_template, request, current_app, jsonify, abort
from exa_github_search.app.models.search_params import GitHubSearchParams
from exa_github_search.app.services.search_service import SearchService
from exa_github_search.app import limiter

bp = Blueprint('search', __name__, url_prefix='/search')


def parse_comma_separated_list(input_str):
    """Parse a comma-separated string into a list of trimmed values."""
    if not input_str or not input_str.strip():
        return []
    return [item.strip() for item in input_str.split(',') if item.strip()]


@bp.route('/', methods=['GET', 'POST'])
@limiter.limit("60 per hour")
def search():
    """Handle search requests and render results."""
    # If POST request, process the form
    if request.method == 'POST':
        # Parse the search parameters from the form
        query = request.form.get('query')
        search_type = request.form.get('type', 'repositories')
        language = request.form.get('language')

        # Handle star counts
        min_stars = request.form.get('min_stars')
        max_stars = request.form.get('max_stars')
        stars = None
        if min_stars or max_stars:
            try:
                min_stars_int = int(
                    min_stars) if min_stars and min_stars.strip() else None
                max_stars_int = int(
                    max_stars) if max_stars and max_stars.strip() else None
                stars = [min_stars_int, max_stars_int]
            except ValueError:
                # Log the error but continue with None values
                current_app.logger.warning(
                    f"Invalid star count values: min={min_stars}, max={max_stars}")
                stars = [None, None]

        # Handle fork counts
        min_forks = request.form.get('min_forks')
        max_forks = request.form.get('max_forks')
        forks = None
        if min_forks or max_forks:
            try:
                min_forks_int = int(
                    min_forks) if min_forks and min_forks.strip() else None
                max_forks_int = int(
                    max_forks) if max_forks and max_forks.strip() else None
                forks = [min_forks_int, max_forks_int]
            except ValueError:
                # Log the error but continue with None values
                current_app.logger.warning(
                    f"Invalid fork count values: min={min_forks}, max={max_forks}")
                forks = [None, None]

        # Handle dates
        created = request.form.get('created')
        pushed = request.form.get('pushed')

        # Handle user/org filters
        user = request.form.get('user')
        org = request.form.get('org')

        # Handle boolean filters
        is_public = request.form.get('is_public') == 'on'
        include_forks = request.form.get('include_forks') == 'on'

        # Handle topics, subtopics, and tags
        topics = parse_comma_separated_list(request.form.get('topics'))
        subtopics = parse_comma_separated_list(request.form.get('subtopics'))
        tags = parse_comma_separated_list(request.form.get('tags'))
        exclude_topics = parse_comma_separated_list(
            request.form.get('exclude_topics'))

        # Create search params object
        search_params = GitHubSearchParams(
            query=query,
            type=search_type,
            language=language,
            stars=stars,
            forks=forks,
            created=created,
            pushed=pushed,
            user=user,
            org=org,
            is_public=is_public,
            include_forks=include_forks,
            topics=topics,
            subtopics=subtopics,
            tags=tags,
            exclude_topics=exclude_topics
        )

        # Check if query is provided
        if not query:
            return render_template('index.html', error="Please provide a search query"), 400

        # Get page number
        page = int(request.form.get('page', 1))
        per_page = int(request.form.get('per_page', 10))

        # Determine if Exa enhancement is requested
        enhance_with_exa = request.form.get('enhance_with_exa') == 'on'

        # Create search service
        search_service = SearchService(
            github_token=current_app.config.get('GITHUB_TOKEN'),
            exa_api_key=current_app.config.get('EXA_API_KEY')
        )

        # Perform search
        results = search_service.combined_search(
            search_params=search_params,
            page=page,
            per_page=per_page,
            enhance_with_exa=enhance_with_exa
        )

        if not results:
            return render_template('index.html', error="No results found or an error occurred"), 404

        # Render results template
        return render_template(
            'results.html',
            results=results,
            search_params=search_params,
            page=page,
            per_page=per_page,
            enhance_with_exa=enhance_with_exa,
            max=max,  # Provide the max function to the template
            min=min   # Provide the min function to the template
        )

    # If GET request, redirect to home page
    return render_template('index.html')


@bp.route('/api', methods=['POST'])
@limiter.limit("30 per minute")
def api_search():
    """Handle API search requests and return JSON response."""
    # Check for JSON in request
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Extract search parameters
    query = data.get('query')
    if not query:
        return jsonify({"error": "Search query is required"}), 400

    # Process topics, subtopics, and tags
    topics = data.get('topics', [])
    subtopics = data.get('subtopics', [])
    tags = data.get('tags', [])
    exclude_topics = data.get('exclude_topics', [])

    # Get pagination parameters
    page = int(data.get('page', 1))
    per_page = int(data.get('per_page', 10))

    # Validate and convert numeric parameters
    stars_data = data.get('stars')
    forks_data = data.get('forks')

    stars = None
    if stars_data:
        try:
            if isinstance(stars_data, list) and len(stars_data) == 2:
                min_stars = int(
                    stars_data[0]) if stars_data[0] is not None else None
                max_stars = int(
                    stars_data[1]) if stars_data[1] is not None else None
                stars = [min_stars, max_stars]
            else:
                current_app.logger.warning(
                    f"Invalid stars format: {stars_data}")
        except (ValueError, TypeError) as e:
            current_app.logger.warning(f"Error converting stars values: {e}")

    forks = None
    if forks_data:
        try:
            if isinstance(forks_data, list) and len(forks_data) == 2:
                min_forks = int(
                    forks_data[0]) if forks_data[0] is not None else None
                max_forks = int(
                    forks_data[1]) if forks_data[1] is not None else None
                forks = [min_forks, max_forks]
            else:
                current_app.logger.warning(
                    f"Invalid forks format: {forks_data}")
        except (ValueError, TypeError) as e:
            current_app.logger.warning(f"Error converting forks values: {e}")

    # Create search parameters object
    search_params = GitHubSearchParams(
        query=query,
        type=data.get('type', 'repositories'),
        language=data.get('language'),
        stars=stars,
        forks=forks,
        created=data.get('created'),
        pushed=data.get('pushed'),
        user=data.get('user'),
        org=data.get('org'),
        is_public=data.get('is_public', True),
        include_forks=data.get('include_forks', False),
        topics=topics,
        subtopics=subtopics,
        tags=tags,
        exclude_topics=exclude_topics
    )

    # Determine if Exa enhancement is requested
    enhance_with_exa = data.get('enhance_with_exa', True)

    # Create search service
    search_service = SearchService(
        github_token=current_app.config.get('GITHUB_TOKEN'),
        exa_api_key=current_app.config.get('EXA_API_KEY')
    )

    # Perform search
    results = search_service.combined_search(
        search_params=search_params,
        page=page,
        per_page=per_page,
        enhance_with_exa=enhance_with_exa
    )

    if not results:
        return jsonify({"error": "No results found or an error occurred"}), 404

    # Return results as JSON
    return jsonify({
        "query": search_params.query,
        "search_type": search_params.type,
        "total_count": results.total_count,
        "page": page,
        "per_page": per_page,
        "has_next_page": results.has_next_page,
        "results": [vars(result) for result in results.results]
    })
