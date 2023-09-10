from app import create_app

if __name__ == '__main__':
    print("Application has started!")
    app = create_app()
    app.run(host='0.0.0.0',port=5000,debug=False, use_reloader=False)
