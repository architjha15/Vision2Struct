<h1 align="center">Vision2Struct</h1>

<h2>🚀 Overview</h2>
<p>
Vision2Struct is a full-stack AI-powered image analysis system that converts 
unstructured image data into structured fashion attributes.
</p>

<ul>
  <li>Scrapes images based on user input</li>
  <li>Performs image preprocessing</li>
  <li>Uses Google Gemini AI to analyze images</li>
  <li>Extracts structured attributes:
    <ul>
      <li>Color</li>
      <li>Material</li>
      <li>Vibe</li>
      <li>Season</li>
    </ul>
  </li>
  <li>Stores results in CSV format for further analysis</li>
</ul>

<p>
This project demonstrates integration between frontend, backend, computer vision,
and generative AI.
</p>

<hr>

<h2>🖥 Demo Preview</h2>

<p><b>Frontend Interface</b></p>
<img width="1918" height="924" alt="image" src="https://github.com/user-attachments/assets/3ba51dd5-f4ea-4ecd-98cf-c902fd25b0df" />

<p><b>Generated CSV Output</b></p>
<img width="1919" height="1025" alt="image" src="https://github.com/user-attachments/assets/a0300690-53fa-48c8-8f23-1b8031fb7a24" />


<hr>

<h2>🧠 Problem Statement</h2>
<p>
Unstructured visual data cannot be directly used for analytics or automation.
Vision2Struct transforms raw image data into structured, machine-readable datasets
for:
</p>

<ul>
  <li>Fashion analytics</li>
  <li>Trend detection</li>
  <li>Recommendation systems</li>
  <li>Data pipelines</li>
</ul>

<hr>

<h2>🏗 Architecture Flow</h2>

<pre>
User Input (Prompt + Number of Images)
        ↓
Frontend (HTML, CSS, JS)
        ↓
Python Backend
        ↓
scrapper.py downloads N images
        ↓
OpenCV preprocessing
        ↓
Gemini AI image analysis
        ↓
Structured attributes extraction
        ↓
CSV output generation
</pre>

<hr>

<h2>🛠 Tech Stack</h2>

<h3>Frontend</h3>
<ul>
  <li>HTML</li>
  <li>CSS</li>
  <li>JavaScript</li>
</ul>

<h3>Backend</h3>
<ul>
  <li>Python</li>
</ul>

<h3>Libraries Used</h3>
<ul>
  <li>OpenCV (cv2)</li>
  <li>NumPy</li>
  <li>Pandas</li>
  <li>Pillow (PIL)</li>
  <li>dotenv</li>
  <li>os</li>
</ul>

<h3>AI Model</h3>
<ul>
  <li>Google Gemini API</li>
</ul>

<hr>

<h2>⚙️ Features</h2>
<ul>
  <li>Dynamic image scraping based on user input</li>
  <li>Image preprocessing using OpenCV</li>
  <li>AI-based image understanding</li>
  <li>Structured data extraction (Color, Material, Vibe, Season)</li>
  <li>CSV export for analytics</li>
  <li>Environment variable management using dotenv</li>
</ul>

<hr>

<h2>⚠️ Current Limitation</h2>
<p>
Due to Gemini API billing restrictions:
</p>
<ul>
  <li>Only 1 image is analyzed by AI at a time.</li>
  <li>Multiple images can still be scraped in batch.</li>
</ul>

<hr>

<h2>📂 Project Structure</h2>

<pre>
Vision2Struct/
│
├── downloads/              # Scraped images categorized by prompt
│   ├── denim/
│   ├── football/
│   ├── jeans/
│   ├── jersey/
│   ├── mustang/
│   ├── pants/
│   └── tshirt/
│
├── static/                 # Frontend static files
│   ├── script.js
│   └── style.css
│
├── templates/              # HTML templates (Flask)
│   └── index.html
│
├── app.py                  # Main Flask backend
├── scraper.py              # Image scraping logic
├── analyzer.py             # Gemini AI analysis logic
│
├── analysis_football.csv   # Example generated output
├── requirements.txt
├── .env
├── .gitignore
└── README.md
</pre>


<hr>

<h2>▶️ Installation & Setup</h2>

<pre>
git clone https://github.com/architjha15/Vision2Struct.git
cd Vision2Struct
pip install -r requirements.txt
</pre>

<p>Create a <code>.env</code> file:</p>

<pre>
GEMINI_API_KEY=your_api_key_here
</pre>

<p>Run backend:</p>

<pre>
python main.py
</pre>

<hr>

<h2>📊 Sample Output (CSV)</h2>

<table border="1" cellpadding="6" cellspacing="0">
<tr>
  <th>Image Name</th>
  <th>Color</th>
  <th>Material</th>
  <th>Vibe</th>
  <th>Season</th>
</tr>
<tr>
  <td>img1.jpg</td>
  <td>Black</td>
  <td>Cotton</td>
  <td>Casual</td>
  <td>Summer</td>
</tr>
</table>

<hr>

<h2>🔮 Future Improvements</h2>
<ul>
  <li>Enable multi-image parallel AI processing</li>
  <li>Deploy as a web application</li>
  <li>Add database storage (MongoDB / PostgreSQL)</li>
  <li>Build analytics dashboard</li>
  <li>Improve attribute extraction accuracy</li>
</ul>
