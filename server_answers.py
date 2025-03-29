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
    "problem_id_2": "adminpanel",
    "problem_id_3": "adminpanel",
    "problem_id_4": "pan, lan, man, wan",
    "problem_id_5": "ring",
    "problem_id_6": "[user_mac]",
    "problem_id_7": "[user_ipv4]",
    "problem_id_8": "[screenshot]",
    "problem_id_9": "netflix",
    "problem_id_10": "print('This program will ask the user for two variables then caculate the sum, difference, product, and quotient')
print('This program will also let you know if you picked large numbers or not')
print()
x = int(input('What is the first number? '))
y = int(input('What is the second number? '))
print()
print('The sum of the two numbers is', x+y)
print()
print('The difference of the two numbers is', x-y)
print()
print('The product of the two numbers is', x*y)
print()
print('The quotient of the two numbers is', x/y)
print()
if x > 100 or y > 100:
    print('Wow! You picked some pretty large numbers!')
if x < 100 or y < 100:
    print('Try picking larger numbers next time!')",
    "problem_id_11": "[user_name_code]",
    "problem_id_12": "4, 5, 1, 3, 2",
    "problem_id_13": "6",
    "problem_id_14": "The code checks for several password values and provides different messages. If the user types 'Cyber' or 'Security', they get a congrats message. If they type 'CyberSecurity', they get a star ASCII art. Otherwise, a failure message appears."
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
