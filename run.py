import os
from dotenv import load_dotenv
from exa_github_search.app import create_app

# Load environment variables from .env file if it exists
load_dotenv()

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the application in debug mode if in development
    debug = os.environ.get("FLASK_ENV") == "development"

    # Get host and port from environment variables or use defaults
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))

    # Print a helpful message
    print(f"Starting Exa GitHub Search on http://{host}:{port}")
    print(f"Debug mode: {'on' if debug else 'off'}")

    # Start the Flask application
    app.run(host=host, port=port, debug=debug)
