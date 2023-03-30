from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ollyluvspeeps'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def show_survey_home():
    """Shows the title of the survey, instructions, and a button to start the survey"""
    
    return render_template('survey-home.html', survey=survey)

@app.route('/start', methods=["POST"])
def start_survey():
    return redirect('/question/0')


@app.route('/question/<int:question_id>')
def show_question(question_id):
    """Display the current question"""
    if (responses == None):
        return redirect('/')
    
    if (len(responses) == len(survey.questions)):
        return redirect('/completed-survey')

    if (len(responses) != question_id):
        flash(f"Invalid question id: {question_id}")
        return redirect(f"/question/{len(responses)}")

    question =survey.questions[question_id]
    return render_template('question.html', question_num=question_id, question=question)

@app.route('/answer', methods=["POST"])
def handle_question():
    """Save the response and redirect to next question"""  
    choice = request.form['answer']
    responses.append(choice)

    if(len(responses) == len(survey.questions)):
        return redirect('/completed-survey')
    else:
        return redirect(f"/question/{len(responses)}")

@app.route('/completed-survey')    
def complete():
    """Survey is complete so display completion page"""
    return render_template('completed-survey.html')