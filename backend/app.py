from flask import Flask, request, jsonify
from flask_cors import CORS
from BirdBrain import Finch  # Ensure BirdBrain.py contains the Finch class
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# Initialize the Finch robot
myFinch = Finch()  # Replace 'A' with your device identifier

@app.route('/process-natural-language', methods=['POST'])
def process_natural_language():
    try:
        # Step 1: Get user input
        data = request.json
        print("Received data:", data)  # Debug log
        prompt = data.get('prompt')
        print("Prompt:", prompt)  # Debug log

        # Step 2: Generate Finch commands using OpenAI
        finch_code = generate_finch_code(prompt)
        print("Generated Finch Code:", finch_code)  # Debug log

        # Step 3: Execute the generated Finch commands
        exec_result = execute_code(finch_code)
        print("Execution Result:", exec_result)  # Debug log

        return jsonify({"code": finch_code, "execution_result": exec_result})
    except Exception as e:
        print("Error:", str(e))  # Log the error
        return jsonify({"error": str(e)}), 500

# Initialize OpenAI client
client = OpenAI(api_key=("YOU_OPENAI_API_KEY"))

def generate_finch_code(prompt):
    """Use OpenAI API to convert natural language into Finch commands."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Python code generator for controlling a Finch robot. Convert natural language instructions into Python code using the Finch API. Only use the following methods:\n"
                               "- `myFinch.setMove(direction, distance, speed)`: Move forward/backward. `direction` is 'F' or 'B'. The `speed` parameter must always be set to 30.\n"
                               "- `myFinch.setTurn(direction, angle, speed)`: Turn right/left. `direction` is 'R' or 'L'. The `speed` parameter must always be set to 30.\n"
                               "- `myFinch.setBeak(red, green, blue)`: Set the LED color. Use values from 0 to 255 for each color channel.\n"
                               "- `myFinch.stop()`: Stop the robot's motion.\n"
                               "- `myFinch.getDistance()`: Get the distance reading from the Finch's distance sensor.\n"
                               "Make sure the generated Python code contains no extra comments or explanations, just the code itself."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        # Access and clean the response
        generated_code = response.choices[0].message.content.strip()

        # Remove Markdown-style code block delimiters if present
        if generated_code.startswith("```") and generated_code.endswith("```"):
            generated_code = generated_code.strip("```").strip("python").strip()

        # Ensure `speed` is always 30
        updated_code = []
        for line in generated_code.splitlines():
            if "myFinch.setMove" in line or "myFinch.setTurn" in line:
                parts = line.split(",")
                if len(parts) == 3:  # Ensure the line has the expected structure
                    parts[-1] = " 30);"  # Always set the last parameter to 30
                    line = ",".join(parts)
            updated_code.append(line)

        final_code = "\n".join(updated_code)
        print("Final Generated Code:", final_code)  # Debugging log
        return final_code
    except Exception as e:
        print("OpenAI API Error:", str(e))  # Debugging log
        raise



def execute_code(code):
    """Execute the generated Python code."""
    try:
        exec_globals = {"myFinch": myFinch}
        exec(code, exec_globals)
        myFinch.stop()
        myFinch.setBeak(0, 0, 0)

        return "Commands executed successfully"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
