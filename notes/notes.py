import sqlite3
from flask import Flask, render_template, g, url_for, request, flash, redirect, session, \
        abort
from time import strftime

app = Flask(__name__)
DATABASE = 'notes.db'
app.secret_key = 'G\xf0\xb6D\xdd\t\\\xd5\xde\xd3\xb1\x0e\xc8\x05\x01\x1f>\xb5\x10\xbf\xb8\xber\n'

@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('select id, time, note from entries order by id desc')
	entries = cur.fetchall()
	return render_template('notes.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
	db = get_db()
	#not valid insert?
	db.execute('insert into entries (time, note) values (?, ?)',
		[strftime('%Y-%m-%d %H:%M:%S'), request.form['text']] )
	db.commit()
	flash('New entry was added')
	return redirect(url_for('show_entries'))
	
@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.cli.command('initdb')
def initdb_command():
	init_db()
	print('Initialized the database.')

def connect_db():
	rv = sqlite3.connect(DATABASE)
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


