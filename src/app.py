from flask import Flask, render_template, request, jsonify
import model  # Import your model.py script

app = Flask(__name__)

# Route to display the webpage (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle user queries
# Route to handle user queries
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json  # Fetch JSON data from the request
        user_query = data.get('query')  # Safely extract the 'query' field
        
        if not user_query:
            return jsonify({'response': "No query provided!"}), 400

        # Check if the query is the same as the previous one
        if hasattr(ask, 'previous_query') and ask.previous_query == user_query:
            return jsonify({'response': "Please enter a new query!"}), 400

        # Store the current query as the previous query
        ask.previous_query = user_query

        # Initialize the model and process the query
        sentence_model, content, index = model.initialize_system()
        response = model.query_system(user_query, sentence_model, index, content)
        
        return jsonify({'response': {'title': '', 'causes': '', 'treatment': response}})
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    port = 343  # Define the port for the application
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    print(f"The app is running on http://{ip}:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)