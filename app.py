from flask import Flask, render_template, request, redirect, session, url_for
from modules import auth_module, emotion_detector, music_recommender, history_tracker
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if auth_module.login(username, password):
            session['username'] = username
            return redirect('/land')
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    if auth_module.signup(username, password):
        session['username'] = username
        return redirect('/land')
    else:
        return render_template('login.html', error="Username already exists")

@app.route('/land', methods=['GET'])
def land():
    if 'username' not in session:
        return redirect('/')
    return render_template('land.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'username' not in session:
        return redirect('/')

    input_method = request.form.get('input_method')
    mood = "neutral"
    text_input = ""

    if input_method == "text":
        text_input = request.form.get('text_input', '')
        mood = emotion_detector.detect_text_mood(text_input)

    elif input_method == "voice":
        text_input = emotion_detector.voice_to_text()
        mood = emotion_detector.detect_text_mood(text_input)

    elif input_method == "face":
        mood = emotion_detector.detect_face_mood()

    history_tracker.save_mood(session['username'], mood)
    return render_template("result.html", mood=mood, spoken_text=text_input, songs=None, preference=None)

@app.route('/recommend', methods=['POST'])
def recommend():
    if 'username' not in session:
        return redirect('/')
    
    mood = request.form['mood']
    preference = request.form['preference']

    # Get songs based on preference
    songs = music_recommender.get_recommendations(mood, preference)

    return render_template("result.html", mood=mood, spoken_text="", songs=songs, preference=preference)


@app.route('/history')
def history():
    if 'username' not in session:
        return redirect('/')
    data, plot_path = history_tracker.get_history(session['username'])
    return render_template("history.html", mood_data=data, plot_path=plot_path)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/aboubt')
def aboubt():
    return render_template('aboubt.html')


@app.route('/meet')
def meet():
    if 'username' in session:
        return render_template('meet.html')
    else:
        flash('Please login first')
        return redirect(url_for('land'))

@app.route('/ai-mood-detection')
def ai_mood():
    if 'username' in session:
        return render_template('ai_mood.html')
    else:
        flash('Please login first')
        return redirect(url_for('land'))

@app.route('/machine-learning')
def ml_tech():
    if 'username' in session:
        return render_template('ml_tech.html')
    else:
        flash('Please login first')
        return redirect(url_for('land'))

@app.route('/spotify-integration')
def spotify_tech():
    if 'username' in session:
        return render_template('spotify_tech.html')
    else:
        flash('Please login first')
        return redirect(url_for('land'))

@app.route('/youtube-integration')
def youtube_tech():
    if 'username' in session:
        return render_template('youtube_tech.html')
    else:
        flash('Please login first')
        return redirect(url_for('land'))

if __name__ == "__main__":
    if not os.path.exists("static"):
        os.makedirs("static")
    app.run(debug=False)
