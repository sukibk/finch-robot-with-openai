# **FinchRobot: Generative AI-Powered Robot Controller**

This project demonstrates the integration of **Generative AI** to process natural language commands and translate them into Python code for controlling the **Finch robot**. It was created as part of my final college presentation on:

**"Generative AI and Its Advancements in Uncrewed Systems"**

---

## **Features**

- Accepts **natural language commands** such as:
  > "Move Finch forward for 20 centimeters, turn left, and set the LED color to blue."
- Converts the commands into Python code using **OpenAI's GPT-4 model**.
- Executes the generated Python code to control the **Finch robot** in real time.
- Automatically turns off the Finch robot's LED after completing execution.

---

## **Project Structure**

```plaintext
FinchRobot/
├── backend/
│   ├── app.py                 # Flask backend for processing commands
│   ├── BirdBrain.py           # Finch robot API library
│   ├── FinchTest.py           # Finch robot testing script
│   ├── requirements.txt       # Python dependencies
│   ├── LICENSE.txt            # License information
│   └── README.md              # Project documentation
├── frontend/
│   ├── app/
│   │   ├── layout.jsx         # Layout configuration for the frontend
│   │   ├── page.jsx           # Main user interface page
│   │   ├── fonts/             # Fonts for styling
│   └── components/            # React components for frontend modularization


