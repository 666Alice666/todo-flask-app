from flask import Flask, session
from config import Config
from modules.routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)


@app.before_request
def init_session():
    if 'tasks' not in session:
        session['tasks'] = []


register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)