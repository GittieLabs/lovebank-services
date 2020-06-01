from lovebank_services import app, db    # import app from services/__init__.py

# Run app
if __name__ == "__main__":
    app.run(debug=True, port=5000) # Turn on debug mode and run on port 5000
