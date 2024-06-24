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

@app.route('/about')
def about():
    return render_template('about.html', title="About Us")

@app.route('/experiences')
def experience():
    work_experiences = [
        {
            'title': 'Software Engineer Intern',
            'company': 'Verizon',
            'description': 'Collaborate with the Customer Experience team to develop and enhance software solutions, to improve user satisfaction and streamline customer interactions'
        },
        {
            'title': 'Full Stack Software Engineer Intern',
            'company': 'CTP',
            'description': 'Developed a high-performance workspace management application using Java, Spring Boot, and React.'
        },
        {
            'title': 'Software Engineer Intern',
            'company': 'City of New York',
            'description': 'Led an Agile team in developing a full-stack application for the City of New York, utilizing React.js, PostgreSQL, Express, and Node.js to connect NYC residents with the city s extensive alumni network, serving over 8.5 million potential users.'
        },
    ]
    return render_template('exp.html', title="Work Experiences", work_experiences=work_experiences)

@app.route('/hobbies')
def hobbies():
    # Mock data
    hobbies = [
        {
            'name': 'Working Out',
            'description': 'I love working out and doing other outdoor activities.',
            'image': 'img/gym.webp'
        },
        {
            'name': 'Trying new Foods',
            'description': 'One of my biggest hobbies is trying new food places and new cuisines.',
            'image': 'img/food.webp'
        },
        {
            'name': 'Computer Science Content Creation',
            'description': 'I enjoy creating content that is helpful for computer science students on LinkedIn',
            'image': 'img/cont.webp'
        },
    ]
    return render_template('hobbies.html', title="Hobbies", hobbies=hobbies)