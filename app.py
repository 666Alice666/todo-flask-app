from flask import Flask, session
from config import CONFIG
from modules.routes import register_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = CONFIG['SECRET_KEY']


@app.before_request
def init_session():
    if 'tasks' not in session:
        session['tasks'] = []


register_routes(app)

if __name__ == '__main__':
    port = CONFIG['PORT']
    app.run(host='0.0.0.0', port=port, debug=CONFIG['DEBUG'])