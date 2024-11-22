<h1>FinchRobot: Generative AI-Powered Robot Controller</h1>

<p>This project demonstrates the integration of <strong>Generative AI</strong> to process natural language commands and translate them into Python code for controlling the <strong>Finch robot</strong>. It was created as part of my final college presentation on:</p>

<p><strong>"Generative AI and Its Advancements in Uncrewed Systems"</strong></p>

<hr />

<h2>Features</h2>

<ul>
  <li>
    Accepts <strong>natural language commands</strong> such as:
    <blockquote>
      "Move Finch forward for 20 centimeters, turn left, and set the LED color to blue."
    </blockquote>
  </li>
  <li>Converts the commands into Python code using <strong>OpenAI's GPT-4 model</strong>.</li>
  <li>Executes the generated Python code to control the <strong>Finch robot</strong> in real time.</li>
  <li>Automatically turns off the Finch robot's LED after completing execution.</li>
</ul>

<hr />

<h2>Project Structure</h2>

<pre><code>
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
</code></pre>

<hr />

<h2>Setup Instructions</h2>

<h3>Backend Setup</h3>

<h4>Clone the Repository:</h4>

<pre><code class="language-bash">
git clone https://github.com/your-repository/FinchRobot.git
cd FinchRobot/backend
</code></pre>

<h4>Create a Virtual Environment:</h4>

<pre><code class="language-bash">
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
</code></pre>

<h4>Install Dependencies:</h4>

<pre><code class="language-bash">
pip install -r requirements.txt
</code></pre>

<h4>Set Up Your OpenAI API Key:</h4>

<p>Obtain your API key from the OpenAI platform.</p>

<p>Export it as an environment variable:</p>

<p>For Unix/Linux:</p>

<pre><code class="language-bash">
export OPENAI_API_KEY="your-api-key"
</code></pre>

<p>For Windows:</p>

<pre><code class="language-bash">
set OPENAI_API_KEY="your-api-key"
</code></pre>

<h4>Run the Backend Server:</h4>

<pre><code class="language-bash">
python app.py
</code></pre>

<p>The backend server will start on <a href="http://localhost:5001">http://localhost:5001</a>.</p>

<h3>Frontend Setup</h3>

<h4>Navigate to the Frontend Directory:</h4>

<pre><code class="language-bash">
cd FinchRobot/frontend
</code></pre>

<h4>Install Dependencies:</h4>

<pre><code class="language-bash">
npm install
</code></pre>

<h4>Run the Frontend:</h4>

<pre><code class="language-bash">
npm run dev
</code></pre>

<p>The frontend will start on <a href="http://localhost:3000">http://localhost:3000</a>.</p>

<hr />

<h2>Dependencies</h2>

<h3>Backend (Python)</h3>

<p>The backend requires the following Python libraries, specified in <code>requirements.txt</code>:</p>

<pre><code>
blinker==1.9.0
click==8.1.7
Flask==3.1.0
Flask-Cors==5.0.0
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==3.0.2
Werkzeug==3.1.3
openai==0.28.0
</code></pre>

<h3>Frontend (JavaScript)</h3>

<p>The frontend uses:</p>

<ul>
  <li><strong>React</strong></li>
  <li><strong>Next.js</strong></li>
  <li><strong>Tailwind CSS</strong></li>
</ul>

<p>Install all dependencies using:</p>

<pre><code class="language-bash">
npm install
</code></pre>

<hr />

<h2>Usage</h2>

<ol>
  <li>
    <strong>Start the backend server:</strong>
    <pre><code class="language-bash">
python app.py
    </code></pre>
  </li>
  <li>
    <strong>Start the frontend server:</strong>
    <pre><code class="language-bash">
npm run dev
    </code></pre>
  </li>
  <li>
    <strong>Open your browser and navigate to</strong> <a href="http://localhost:3000">http://localhost:3000</a>.
  </li>
  <li>
    <strong>Enter natural language commands to control the Finch robot.</strong>
  </li>
</ol>

<hr />

<h2>Acknowledgments</h2>

<p>This project was developed as part of my final college presentation on <strong>Advancements in Generative AI and its Potential in Uncrewed Systems</strong>. It demonstrates the practical application of AI in robotics by bridging natural language processing and robot control.</p>

<hr />

<h2>License</h2>

<p>This project is licensed under the MIT License. See the <code>LICENSE.txt</code> file for details.</p>

<hr />

<h2>Contact</h2>

<p>For inquiries or suggestions, please contact:</p>

<p><strong>Your Name</strong></p>

<ul>
  <li><strong>Email:</strong> mjsudar21@catawba.edu</li>
  <li><strong>GitHub:</strong> <a href="https://github.com/sukibk">sukibk</a></li>
</ul>

<hr />
