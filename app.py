from flask import Flask, session, request, render_template, redirect, url_for
from config import CONFIG
from models import db, Task
import time
import logging
import json
import sys
import uuid
from datetime import datetime

# --- Логирование ---
class StructuredLogger:
    def __init__(self, service_name):
        self.service_name = service_name

    def _log(self, level, message, **kwargs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.upper(),
            "service": self.service_name,
            "message": message,
            **kwargs
        }
        print(json.dumps(log_entry), flush=True)

    def info(self, message, **kwargs):
        self._log("info", message, **kwargs)

    def error(self, message, **kwargs):
        self._log("error", message, **kwargs)

logger = StructuredLogger("todo-service")

# --- Flask App ---
app = Flask(__name__)
app.config['SECRET_KEY'] = CONFIG['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

first_request_handled = False

def ensure_tables():
    global first_request_handled
    if not first_request_handled:
        max_retries = 30
        for attempt in range(max_retries):
            try:
                db.create_all()
                logger.info("Database tables created successfully.")
                break
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)
        else:
            logger.error("Failed to connect to DB after several attempts.")
            raise RuntimeError("Could not connect to database after retries.")
        first_request_handled = True

# --- Middleware для request ID ---
@app.before_request
def add_request_id():
    request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
    request.request_id = request_id
    logger.info("Request started", request_id=request_id, method=request.method, path=request.path)

@app.after_request
def log_response(response):
    logger.info("Request finished", request_id=request.request_id, status_code=response.status_code)
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    ensure_tables()

    if request.method == 'POST':
        task_content = request.form['task']
        if task_content:
            new_task = Task(content=task_content)
            db.session.add(new_task)
            db.session.commit()
            logger.info("Task added", request_id=request.request_id, task_id=new_task.id, content=new_task.content)
        return redirect(url_for('index'))

    tasks = Task.query.all()
    logger.info("Tasks retrieved", request_id=request.request_id, count=len(tasks))
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    logger.info("Task deleted", request_id=request.request_id, task_id=id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = CONFIG['PORT']
    app.run(host='0.0.0.0', port=port, debug=CONFIG['DEBUG'])