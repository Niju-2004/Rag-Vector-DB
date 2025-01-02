from flask import Flask, render_template, request, jsonify
import model  # Import your model.py script

app = Flask(__name__)

# Route to display the webpage (index.html)
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle user queries
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json  # Fetch JSON data from the request
        user_query = data.get('query')  # Safely extract the 'query' field
        
        if not user_query:
            return jsonify({'response': "No query provided!"}), 400

        # Initialize the model and process the query
        sentence_model, content, index = model.initialize_system()
        response = model.query_system(user_query, sentence_model, index, content)
        
        return jsonify({'response': response})
    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    port = 343  # Define the port for the application
    print(f"The app is running on http://127.0.0.1:{port}")
    app.run(debug=True, host="0.0.0.0", port=port)
