"""A simple API to track writing."""

from flask import Flask, request

from entry_functions import (
    load_all_entries,
    save_new_entry,
    is_valid_entry
)

api = Flask(__name__)

@api.get("/")
def index():
    # All routes will return json data.
    return {
        "message" : "Welcome to the Writing App API."
    }

@api.route("/entries", methods=["GET", "POST"])
def get_or_create_entries():

    if request.method == "GET":
        entries = load_all_entries()
        args = request.args

        if "author" in args:
            author = args["author"]
            entries = [entry for entry in entries
                       if entry["author"].lower() == author.lower()]

        return entries
    else:
        new_entry = request.json
        if is_valid_entry(new_entry):
            created_entry = save_new_entry(new_entry)
            return created_entry, 201
        else:
            return {"error": True, "error_message": "Invalid entry."}, 400


if __name__ == "__main__":
    
    api.run(port=8080, debug=True)
