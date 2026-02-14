"""
Vision2Struct - Web Service Layer
----------------------------------
Flask API that orchestrates:

1. Image scraping
2. LLM-based image analysis
3. Structured CSV generation

This file serves as the application entry point.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import download_bulk_images
from analyzer import analyze_folder

app = Flask(__name__)

# Enable cross-origin requests (useful if frontend is separate)
CORS(app)


# ---------------------------------------------------------
# Route: /scrape
# Description:
# Accepts a keyword and image limit,
# downloads images, runs AI analysis,
# and returns structured CSV file path.
# ---------------------------------------------------------
@app.route('/scrape', methods=['POST'])
def handle_scrape():
    try:
        data = request.json

        # Basic input validation
        if not data or 'keyword' not in data:
            return jsonify({"status": "Error", "message": "Keyword is required"}), 400

        keyword = data.get('keyword')
        limit = int(data.get('limit', 10))

        # Step 1: Scrape images based on keyword
        saved_path = download_bulk_images(keyword, limit)

        # Step 2: Run AI-powered metadata extraction
        csv_file = analyze_folder(saved_path)

        return jsonify({
            "status": "Success",
            "message": "Pipeline executed successfully",
            "csv": csv_file
        })

    except Exception as e:
        # Generic error handler for unexpected failures
        return jsonify({"status": "Error", "message": str(e)}), 500


# ---------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------
if __name__ == "__main__":
    app.run(port=5000, debug=False)
