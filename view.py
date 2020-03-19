from flask import render_template, request, redirect, session, flash

from app import app
from config import LENGTH
from models import quiz_factory


@app.route('/')
@app.route('/home')
def home():
    session['session'] = quiz_factory(LENGTH)
    session['score'] = 0
    session['round'] = 0
    return render_template('home.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if session['round'] < LENGTH:
        card = session.get('session').get('quiz_queue')
        card = card[session['round']]
    else:
        return redirect('endscreen')

    if request.method == "POST":
        if str(card.get('answer_index')) == request.form.get('answer'):
            flash('Correct')
            session['score'] = session.get('score') + 1

        else:
            flash('Wong')
        session['round'] = session.get('round') + 1
        return redirect('quiz')

    return render_template('quiz.html', title='Викторина', data=card)


@app.route('/endscreen')
def endscreen():
    return render_template('endgame.html', title='Викторина', score=session['score'])


@app.route('/about')
def about():
    return render_template('about.html', title='О нас')