from API import app
from API.utils.tokenizer import admin_required

# @app.route('/dashboard')
# @admin_required
# def hello():
#     return 'Hello'

# @app.route('/')
# def homepage():
#     return 'it work'

if __name__ == '__main__':
    app.run(debug=True)
