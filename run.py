from app import create_app

app = create_app()

if __name__ == "__main__":
    is_debug = app.config["FLASK_DEBUG"]
    app.run(debug=is_debug) 