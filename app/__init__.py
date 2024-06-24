import os
from flask import Flask, render_template, request
from jinja2 import Environment, PackageLoader, select_autoescape
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))