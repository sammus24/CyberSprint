from flask import Flask, request, jsonify, session
from flask_cors import CORS
import time

app = Flask(__name__)
app.secret_key = "super_secret_key"
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# Users dictionary
users = {}

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get("team_name")
        password = data.get("password")

        if not username or not password:
            return jsonify({"status": "error", "message": "Username and password are required"}), 400

        if username in users:
            return jsonify({"status": "error", "message": "Username already exists"}), 409

        users[username] = {
            "password": password,
            "score": 0,
            "challenges_solved": 0,
            "time_taken": "00:00:00"
        }

        return jsonify({"status": "success", "message": "Registration successful!", "username": username})

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error: {str(e)}"}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password are required"}), 400

    if username in users and users[username]["password"] == password:
        session["username"] = username
        return jsonify({"status": "success", "message": "Login successful!", "username": username})

    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@app.route('/submit', methods=['POST'])
def submit_answer():
    try:
        data = request.get_json()
        username = data.get("username")
        problem_id = data.get("problemId")
        answer = data.get("answer")

        if username not in users:
            return jsonify({"status": "error", "message": "User not found"}), 404

        correct_answers = {
    "problem_id_1": "adminpanel",
    "problem_id_2": "reversingflag",
    "problem_id_3": "reversingflag",
    "problem_id_4": "reversingflag",
    "problem_id_5": "reversingflag",
    "problem_id_6": "reversingflag"
}


        if problem_id in correct_answers and answer.strip().lower() == correct_answers[problem_id].strip().lower():
            users[username]["score"] += 10
            users[username]["challenges_solved"] += 1
            users[username]["time_taken"] = time.strftime("%H:%M:%S", time.localtime())

            return jsonify({"status": "correct", "message": "Correct answer!", "updated_score": users[username]["score"]})

        return jsonify({"status": "incorrect", "message": "Wrong answer!"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error processing submission: {str(e)}"}), 500

@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    # Sort users by score in descending order
    sorted_users = sorted(users.items(), key=lambda x: x[1]['score'], reverse=True)
    
    # Prepare a response list for leaderboard
    leaderboard_data = [{'username': user[0], 
                         'score': user[1]['score'], 
                         'challenges_solved': user[1]['challenges_solved'], 
                         'time_taken': user[1].get('time_taken', 'N/A')} for user in sorted_users]
    return jsonify(leaderboard_data)


if __name__ == '__main__':
    app.run(debug=True)
