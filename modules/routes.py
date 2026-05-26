from flask import request, render_template, redirect, url_for
from .services import get_tasks, add_task, remove_task_at_index


def register_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            task_content = request.form['task']
            if task_content:
                add_task(task_content)  # ✅ без request.session
            return redirect(url_for('index'))

        tasks = get_tasks()  # ✅ без request.session
        return render_template('index.html', tasks=tasks)

    @app.route('/delete/<int:index>')
    def delete_task(index):
        remove_task_at_index(index)  # ✅ без request.session
        return redirect(url_for('index'))