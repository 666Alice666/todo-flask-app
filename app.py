from flask import Flask, session, request, render_template, redirect, url_for
from config import CONFIG
from models import db, Task
import time
import logging

logging.basicConfig(level=logging.INFO)

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
                print("Database tables created successfully.")
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(2)
        else:
            print("Failed to connect to DB after several attempts.")
            raise RuntimeError("Could not connect to database after retries.")
        first_request_handled = True

@app.route('/', methods=['GET', 'POST'])
def index():
    ensure_tables()

    if request.method == 'POST':
        task_content = request.form['task']
        if task_content:
            new_task = Task(content=task_content)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('index'))

    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = CONFIG['PORT']
    app.run(host='0.0.0.0', port=port, debug=CONFIG['DEBUG'])