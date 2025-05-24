from flask import render_template
from . import main

@main.route('/')
def index():  # Changed from 'home' to 'index'
    return render_template('index.html', active='home')

@main.route('/contact')
def contact():
    return render_template('contact.html', active='contact')

@main.route('/projects')
def projects():
    return render_template('projects.html', active='projects')