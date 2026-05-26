from flask import session


def get_tasks():
    return session.get('tasks', [])


def save_tasks(tasks):
    session['tasks'] = tasks


def add_task(task_content):
    tasks = get_tasks()
    tasks.append(task_content)
    save_tasks(tasks)


def remove_task_at_index(index):
    tasks = get_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)