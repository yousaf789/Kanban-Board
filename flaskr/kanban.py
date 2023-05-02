from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('kanban', __name__)

@bp.route('/')
def index():
    return render_template('kanban/index.html')

@bp.route('/board', methods=('GET', 'POST'))
@login_required
def board():
    db = get_db()
    posts = db.execute(
        'SELECT t.id, title, description, created, category, creator_id, due_date, username'
        ' FROM task t JOIN user u ON t.creator_id = u.id WHERE creator_id = ?'
        ' ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        due_date = request.form['time']
        error = None

        if not title:
            error = 'Title is required.'

        if not category:
            error = 'Category is required.'
        
        # if not due_date:
        #     error = 'Due date is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO task (title, description, category, due_date, creator_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, description, category, due_date, g.user['id'])
            )
            db.commit()
            return redirect(url_for('kanban.board'))

    return render_template('kanban/board.html', posts=posts)


def get_task(id, check_author=True):
    task = get_db().execute(
        'SELECT t.id, title, description, category, created, creator_id, due_date, username'
        ' FROM task t JOIN user u ON t.creator_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if task is None:
        abort(404, f"Task id {id} doesn't exist.")

    if check_author and task['creator_id'] != g.user['id']:
        abort(403)

    return task


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    task = get_task(id)

    if request.method == 'POST':
        # title = request.form['title']
        # description = request.form['description']
        category = request.args['category']
        error = None

        # if not title:
        #     error = 'Title is required.'

        if not category:
            error = 'Category is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE task SET category = ?'
                ' WHERE id = ?',
                (category, id)
            )
            db.commit()
            return redirect(url_for('kanban.board'))

    return render_template('kanban/board.html')


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_task(id)
    db = get_db()
    db.execute('DELETE FROM task WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('kanban.board'))
