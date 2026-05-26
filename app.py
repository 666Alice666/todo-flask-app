from flask import Flask, session
from config import Config
from modules.routes import register_routes
import os

app = Flask(__name__)
app.config.from_object(Config)


@app.before_request
def init_session():
    if 'tasks' not in session:
        session['tasks'] = []


register_routes(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)