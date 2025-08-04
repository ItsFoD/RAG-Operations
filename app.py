from flask import Flask, request, jsonify, render_template
import requests
from keys import endpoint_url, promptflow_api_key

app = Flask(__name__)
promptflow = promptflow_api_key
endpoint = endpoint_url

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        user_input = request.form['user_input']
        bot_response = generate_bot_response(user_input)
        return jsonify({'response': bot_response})
    return render_template('chatbot.html')

def generate_bot_response(user_input):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {promptflow}",
        "azureml-model-deployment": "rag-trial-0"
    }

    data = {
        "question": user_input,
        "chat_history": []
    }

    try:
        response = requests.post(endpoint, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Print the full result for debugging
        print("🔍 Raw Prompt Flow response:", result)

        # Try all common options in order
        if isinstance(result, dict):
            if "output" in result:
                return result["output"]
            elif "answer" in result:
                return result["answer"]
            elif "outputs" in result:
                if "output" in result["outputs"]:
                    return result["outputs"]["output"]
                elif "answer" in result["outputs"]:
                    return result["outputs"]["answer"]
            # Fallback for dict without known fields
            return str(result)
        else:
            # It might be just a plain string
            return str(result)

    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
