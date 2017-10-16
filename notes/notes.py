import sqlite3
from flask import Flask, render_template, g, url_for, request, flash, redirect, session, \
        abort

app = Flask(__name__)
DATABASE = 'notes.db'


@app.route('/')
def notes():
	return "Notes here"

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


