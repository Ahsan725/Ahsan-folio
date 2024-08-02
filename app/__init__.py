import os
import datetime
from playhouse.shortcuts import model_to_dict
from peewee import *
from flask import Flask, render_template, request, jsonify
from jinja2 import Environment, PackageLoader, select_autoescape
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__) 
if os.getenv("FLASK_ENV") == "testing":
    mydb = SqliteDatabase(':memory:')
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
                         user=os.getenv("MYSQL_USER"),
                         passwd=os.getenv("MYSQL_PASSWORD"),
                         host=os.getenv("MYSQL_HOST"),
                         port=3306
                         )

print(mydb)

env = Environment(
    loader=PackageLoader('app', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

if os.getenv('FLASK_ENV') != 'testing':
    mydb.connect()
    mydb.create_tables([TimelinePost], safe=True)

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

@app.route('/education')
def education():
    # Mock data for education
    education = [
        {
            'degree': 'Bachelor of Science in Computer Science',
            'institution': 'Brooklyn College',
            'description': 'Focused on software engineering, algorithms, and data structures. Will graduate with honors in May 2025.'
        },
        {
            'degree': 'High School Diploma',
            'institution': 'FDR High School Brooklyn',
            'description': 'Graduated with a weighted GPA of of 105 out of 100. Salutatorian from a class of 3800 students.'
        },
    ]
    return render_template('education.html', title="Education", education=education)

@app.route('/travel')
def travel():
    return render_template('travel.html', title="Travel")

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb



@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        
        # Validate inputs
        if not name:
            return jsonify({"error": "Invalid name"}), 400
        if not content:
            return jsonify({"error": "Invalid content"}), 400
        if '@' not in email or '.' not in email.split('@')[-1]:
            return jsonify({"error": "Invalid email"}), 400
        
        # Create and save the TimelinePost
        timeline_post = TimelinePost(name=name, email=email, content=content)
        timeline_post.save()
        
        return jsonify(model_to_dict(timeline_post)), 201
    
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e.args[0]}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return{
        'timeline_posts': [
            model_to_dict(p)
            for p in 
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }