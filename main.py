from app import create_app

if __name__ == '__main__':
    print("Application has started!")
    app = create_app()
    app.run(debug=True, use_reloader=False)
