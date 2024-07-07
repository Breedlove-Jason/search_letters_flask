from flask import Flask, render_template, request
from markupsafe import escape
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


def log_request(req: "flask_request", res: str) -> None:
    with open("vsearch.log", "a") as log:
        print(req.form, req.remote_addr, req.user_agent, res, file=log, sep="|")


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
    log_request(request, search_results)

    # Render the results template with the search results
    return render_template(
        "results.html",
        the_title="Here are your results:",
        the_phrase=phrase,
        the_letters=letters,
        the_results=str(search_results),
    )


@app.route("/viewlog")
def viewlog() -> 'html':
    contents = []
    with open("vsearch.log") as log:
        for line in log:
            contents.append([])
            for item in line.split("|"):
                contents[-1].append(escape(item))
    titles = ("Form Data", "Remote_addr", "User_agent", "Results")
    return render_template("viewlog.html", the_title="View Log", the_row_titles=titles, the_data=contents)


# Run the Flask application with debug mode enabled on port 5005
if __name__ == "__main__":
    app.run(debug=True)
