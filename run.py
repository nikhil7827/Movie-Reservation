from app import create_app

# Initialize the Flask app
app = create_app()

# Debug: Print template folder and available templates
if app:
    print("Template folder:", app.template_folder)
    print("Available templates:", app.jinja_env.list_templates())
else:
    print("Error: Flask app failed to initialize. Check create_app() in app/__init__.py.")

# Run the application
if __name__ == '__main__':
    if app:
        with app.app_context():
            from app import seed_initial_data
            seed_initial_data()
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        print("Cannot run the app because initialization failed.")