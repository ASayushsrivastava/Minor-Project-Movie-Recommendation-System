from flask import Flask, render_template, request, jsonify
import fetchmovies  # Assumes fetchmovies.py is in the same directory
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")  # Serves the main page with the form/input field

    # Handle POST request for movie recommendation or search
    data = request.get_json()  # Retrieves JSON data from the client-side request
    if not data:
        return jsonify({"error": "No data provided"}), 400  # Return an error if no data received

    if 'is_rec' in data and data['is_rec']:
        # Recommendation request
        try:
            titles, posters, movie_ids = fetchmovies.reccomendMovies(data['str'])
            response_data = {'titles': titles, 'posters': posters, 'movie_ids': movie_ids}
            return jsonify(response_data)
        except Exception as e:
            # Handles errors in the recommendation function
            return jsonify({"error": str(e)}), 500
    else:
        # Search request
        try:
            search_results = fetchmovies.searchMovies(data['str'])
            return jsonify(search_results)
        except Exception as e:
            # Handles errors in the search function
            return jsonify({"error": str(e)}), 500

# To run the app
if __name__ == "__main__":
    app.run(debug=True)
