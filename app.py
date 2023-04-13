from flask import Flask, request, jsonify, g, render_template, send_from_directory, redirect, url_for, flash
from flask_restful import Resource, Api
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import openai
import sqlite3
import youtube_dl
import pafy
import requests
from bs4 import BeautifulSoup
from video_analysis import analyze_video, VideoAnalysis
from learn_characters import Game, Game1, Game2, FrameData
from dotenv import load_dotenv


app = Flask(__name__, template_folder='templates')
DATABASE = 'ai_app.db'
api = Api(app)

api.add_resource(VideoAnalysis, '/analyze_video')


# Set up OpenAI API
openai.api_key = "your_openai_api_key"

# function to get database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# function to close database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# function to initialize the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# function to query the database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# function to insert data into the database
def insert_data(table, columns, data):
    db = get_db()
    db.execute(f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join(['?'] * len(data))})", data)
    db.commit()

# function to update data in the database
def update_data(table, columns, data, condition):
    db = get_db()
    db.execute(f"UPDATE {table} SET {','.join([f'{col} = ?' for col in columns])} WHERE {condition}", data)
    db.commit()

# function to delete data from the database
def delete_data(table, condition):
    db = get_db()
    db.execute(f"DELETE FROM {table} WHERE {condition}")
    db.commit()

# Call this function only once to initialize the database
init_db()

# function to perform chat functionality with AI
def chat_with_ai(user_input):
    # Combine prompt, chat history, and user input
    full_conversation = f"{prompt}\n\n{chat_history}\nUser: {user_input}\nAssistant:"

    response = openai.Completion.create(
        engine=model_engine,
        prompt=full_conversation,
        max_tokens=token_limit,
        n=1,
        stop=None,
        temperature=0.8,
    )

    reply_text = response.choices[0].text.strip()
    return reply_text

# Start the Flask application

@app.route('/')
def index():
    return render_template('index.html')

# route for AI chat functionality
@app.route("/ai_chat", methods=["POST"])
def ai_chat():
    # Receive user input from the frontend
    data = request.json
    user_input = data["userInput"]

    # Perform chat functionality with AI
    response = chat_with_ai(user_input)

    # Return the AI response to the frontend
    return jsonify({"response": response})


# route for video analysis functionality
@app.route("/video_analysis", methods=["POST"])
def video_analysis():
    # Receive video URL from the frontend
    data = request.json
    video_url = data["videoUrl"]

    # Perform video analysis
    results = analyze_video(video_url)

    # Return the analysis results to the frontend
    return jsonify({"results": results})

# route to store frame data in the database
@app.route('/store_frame_data', methods=['POST'])
def store_frame_data():
    game = request.form['game']
    character = request.form['character']
    frame_data = request.form['frame_data']
    insert_data('characters', ['game', 'name', 'frame_data'], [game, character, frame_data])
    return "Data stored successfully"

# route to get frame data from the database
@app.route('/get_frame_data', methods=['POST'])
def get_frame_data():
    game = request.form['game']
    character = request.form['character']
    frame_data = query_db('SELECT frame_data FROM characters WHERE game = ? AND name = ?', [game, character], one=True)
    if frame_data:
        return json.dumps(frame_data[0])
    else:
        abort(400, description="Character not found")

if __name__ == "__main__":
    app.run(debug=True)

