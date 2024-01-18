from API import app


@app.route('/')
def hello():
    return 'Hello, Flask!'


if __name__ == '__main__':
    app.run()
