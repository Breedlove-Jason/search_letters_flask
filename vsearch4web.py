from flask import Flask, render_template, request

from app import search_for_letters

app = Flask(__name__)


# Route for the entry page
@app.route("/")
@app.route("/entry")
def entry_page() -> "html":
    # Render the entry page template with a title
    return render_template(
        "entry.html", the_title="Welcome to search4letters on the web!"
    )


# Route to handle the search form submission
@app.route("/search4", methods=["POST"])
def do_search() -> str:
    # Extract phrase and letters from the submitted form
    phrase = request.form.get("phrase")
    letters = request.form.get("letters")

    # Check if both phrase and letters are provided
    if not phrase or not letters:
        # Handle the error case (could redirect or show an error message)
        return "Error: Both phrase and letters are required."

    # Perform the search
    search_results = search_for_letters(phrase, letters)

    # Render the results template with the search results
    return render_template(
        "results.html",
        the_title="Here are your results:",
        the_phrase=phrase,
        the_letters=letters,
        the_results=str(search_results),
    )


# Run the Flask application with debug mode enabled on port 5005
if __name__ == "__main__":
    app.run()
