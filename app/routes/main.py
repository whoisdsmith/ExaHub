from flask import Blueprint, render_template, current_app

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Render the home page with search form."""
    github_token_available = bool(current_app.config.get('GITHUB_TOKEN'))
    exa_api_key_available = bool(current_app.config.get('EXA_API_KEY'))

    return render_template(
        'index.html',
        github_token_available=github_token_available,
        exa_api_key_available=exa_api_key_available
    )


@bp.route('/api-playground')
def api_playground():
    """Render the API playground page."""
    github_token_available = bool(current_app.config.get('GITHUB_TOKEN'))
    exa_api_key_available = bool(current_app.config.get('EXA_API_KEY'))

    return render_template(
        'api_playground.html',
        github_token_available=github_token_available,
        exa_api_key_available=exa_api_key_available
    )
