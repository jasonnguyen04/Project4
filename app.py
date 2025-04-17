from flask import Flask, render_template, request, jsonify
import openai
import os
from flask_cors import CORS  # Added for handling Cross-Origin Resource Sharing (CORS)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend interaction

# Configure OpenAI API - you should set this as an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    data = request.json  # Parse the JSON request
    destination = data.get('destination')
    preferences = data.get('preferences', '')

    # Validate input
    if not destination:
        return jsonify({'error': 'Destination is required and cannot be empty'}), 400

    try:
        # Generate travel recommendations using GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a knowledgeable travel assistant that provides detailed recommendations for destinations."},
                {"role": "user",
                 "content": f"I'm planning a trip to {destination}. {preferences} Can you recommend things to do, places to eat, and sights to see? Please format your response with clear headings for 'Things to Do', 'Places to Eat', and 'Sights to See'."}
            ],
            temperature=0.7,
            max_tokens=300
        )

        # Retrieve recommendations from OpenAI response
        if 'choices' in response and len(response.choices) > 0:
            recommendations = response.choices[0].message.content
            return jsonify({'recommendations': recommendations})
        else:
            return jsonify({'error': 'No recommendations received from OpenAI.'}), 500

    except Exception as e:
        # Log error for debugging
        print(f"Error: {e}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    print("Starting Flask app with debug turned on...")
    print("Ensure API Key is loaded. Current API Key:", openai.api_key)  # For initial debugging
    app.run(debug=True)
