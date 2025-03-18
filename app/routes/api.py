from app.services.similarity_service import SimilarityService
from flask import Blueprint, request, jsonify, current_app
import requests
from app import limiter

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/similarity-search', methods=['POST'])
@limiter.limit("20 per minute")
def similarity_search():
    """Handle content similarity search requests."""
    # Check if Exa API key is available
    exa_api_key = current_app.config.get('EXA_API_KEY')
    if not exa_api_key:
        return jsonify({"error": "Exa API key not configured"}), 400

    # Extract basic parameters from request
    prompt = request.form.get('prompt')
    num_results = int(request.form.get('num_results', 5))
    search_type = request.form.get('search_type', 'neural')
    use_autoprompt = request.form.get('use_autoprompt') == 'on'

    # Extract filter parameters
    site_restrict = request.form.get('site_restrict', '')
    excluded_sites = request.form.get('excluded_sites', '')
    content_types = request.form.getlist('content_types')
    language = request.form.get('language', '')
    date_start = request.form.get('date_start', '')
    date_end = request.form.get('date_end', '')

    # Extract display options
    include_domains = request.form.get('include_domains') == 'on'
    include_snippets = request.form.get('include_snippets') == 'on'
    highlight = request.form.get('highlight') == 'on'

    # Validate required parameters
    if not prompt:
        return jsonify({"error": "Search prompt is required"}), 400

    # Create similarity service and perform search
    similarity_service = SimilarityService(exa_api_key=exa_api_key)

    try:
        # Process site restrictions
        include_domains_list = [
            domain.strip() for domain in site_restrict.split(',') if domain.strip()]
        exclude_domains_list = [
            domain.strip() for domain in excluded_sites.split(',') if domain.strip()]

        # Process content types
        content_type_filter = content_types if content_types else None

        # Process date range
        start_date = date_start if date_start else None
        end_date = date_end if date_end else None

        results = similarity_service.search_similar_content(
            prompt=prompt,
            num_results=num_results,
            search_type=search_type,
            use_autoprompt=use_autoprompt,
            include_domains=include_domains_list if include_domains_list else None,
            exclude_domains=exclude_domains_list if exclude_domains_list else None,
            content_types=content_type_filter,
            language=language if language else None,
            start_date=start_date,
            end_date=end_date,
            text=include_snippets
        )

        # Convert results to serializable format
        serializable_results = []
        for result in results:
            res_dict = {
                'title': result.title,
                'url': result.url,
                'score': result.score,
                'published_date': getattr(result, 'published_date', None),
                'domain': getattr(result, 'domain', None) if include_domains else None,
                'text': getattr(result, 'text', None) if include_snippets else None
            }
            serializable_results.append(res_dict)

        return jsonify({"results": serializable_results})

    except requests.RequestException as e:
        current_app.logger.error(
            f"Request error for similarity search: {str(e)}")
        return jsonify({"error": f"External API request failed: {str(e)}"}), 503
    except ValueError as e:
        current_app.logger.error(
            f"Value error for similarity search: {str(e)}")
        return jsonify({"error": f"Invalid parameter value: {str(e)}"}), 400
    except KeyError as e:
        current_app.logger.error(
            f"Missing key for similarity search: {str(e)}")
        return jsonify({"error": f"Missing required parameter: {str(e)}"}), 400
    except Exception as e:
        current_app.logger.exception(
            f"Unexpected error in similarity search: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@bp.route('/similar-urls', methods=['POST'])
@limiter.limit("20 per minute")
def similar_urls():
    """Handle URL similarity search requests."""
    # Check if Exa API key is available
    exa_api_key = current_app.config.get('EXA_API_KEY')
    if not exa_api_key:
        return jsonify({"error": "Exa API key not configured"}), 400

    # Extract basic parameters from request
    url = request.form.get('url')
    num_results = int(request.form.get('num_results', 5))

    # Extract filter parameters
    site_restrict = request.form.get('site_restrict', '')
    excluded_sites = request.form.get('excluded_sites', '')
    language = request.form.get('language', '')
    date_start = request.form.get('date_start', '')
    date_end = request.form.get('date_end', '')

    # Extract options
    text_similarity = request.form.get('text_similarity') == 'on'
    include_domains = request.form.get('include_domains') == 'on'
    include_snippets = request.form.get('include_snippets') == 'on'

    # Validate required parameters
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Create similarity service and perform search
    similarity_service = SimilarityService(exa_api_key=exa_api_key)

    try:
        # Process site restrictions
        include_domains_list = [
            domain.strip() for domain in site_restrict.split(',') if domain.strip()]
        exclude_domains_list = [
            domain.strip() for domain in excluded_sites.split(',') if domain.strip()]

        # Process date range
        start_date = date_start if date_start else None
        end_date = date_end if date_end else None

        results = similarity_service.find_similar_links(
            url=url,
            num_results=num_results,
            include_domains=include_domains_list if include_domains_list else None,
            exclude_domains=exclude_domains_list if exclude_domains_list else None,
            language=language if language else None,
            start_date=start_date,
            end_date=end_date,
            text_similarity=text_similarity,
            text=include_snippets
        )

        # Convert results to serializable format
        serializable_results = []
        for result in results:
            res_dict = {
                'title': result.title,
                'url': result.url,
                'score': result.score,
                'published_date': getattr(result, 'published_date', None),
                'domain': getattr(result, 'domain', None) if include_domains else None,
                'text': getattr(result, 'text', None) if include_snippets else None
            }
            serializable_results.append(res_dict)

        return jsonify({"results": serializable_results})

    except requests.RequestException as e:
        current_app.logger.error(
            f"Request error for similarity search: {str(e)}")
        return jsonify({"error": f"External API request failed: {str(e)}"}), 503
    except ValueError as e:
        current_app.logger.error(
            f"Value error for similarity search: {str(e)}")
        return jsonify({"error": f"Invalid parameter value: {str(e)}"}), 400
    except KeyError as e:
        current_app.logger.error(
            f"Missing key for similarity search: {str(e)}")
        return jsonify({"error": f"Missing required parameter: {str(e)}"}), 400
    except Exception as e:
        current_app.logger.exception(
            f"Unexpected error in similarity search: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
