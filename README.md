# Student Performance Level Prediction Using Machine Learning
> **Course:** Bachelor of Computer Applications (BCA) College Project  
> **Technologies:** Python Flask, Scikit-learn, Pandas, HTML5, CSS3, JavaScript  
> **Algorithm:** Decision Tree Classifier  

---

## 📖 Project Overview

**Student Performance Level Prediction** is a modern, responsive web application designed for academic institutions to assess, predict, and monitor student academic standing. Using student demographic data (gender, parental level of education, lunch category, test preparation course status) alongside scores in **Mathematics, Reading, and Writing**, the system classifies each student into one of three distinct performance tiers:

* 🔴 **Low Performance:** Average marks below 50%
* 🟡 **Medium Performance:** Average marks between 50% and 74%
* 🟢 **High Performance:** Average marks 75% or above

---

## 🎯 Key Highlights & Features

1. **Clean & Modern Educational Theme:** Designed with a white and light-blue educational theme, rounded action buttons, accessible typography, and smooth micro-animations.
2. **Dual-Mode Prediction Engine:**
   - **Machine Learning Mode:** Utilizes a trained `DecisionTreeClassifier` from Scikit-learn with 95.5% test accuracy.
   - **Rule-Based Benchmark Prototype:** Fallback calculation based directly on threshold criteria, ensuring the application remains 100% operational even without `model.pkl`.
3. **Dynamic 3-Page Flow:**
   - **Page 1 (Home):** Project introduction, feature cards, and direct call-to-action button.
   - **Page 2 (Predict Performance):** Interactive input form with quick demo preset buttons (*High, Medium, Low*), real-time average calculation preview, and validation.
   - **Page 3 (Prediction Result):** Dynamic color-coded result card (Red/Yellow/Green), detailed score breakdown bars, recommendation message, and "Predict Again" capability.
4. **Beginner-Friendly Codebase:** Cleanly commented, modular Python and frontend code that is easy to understand and explain during university viva presentations.

---

## 📂 Project Directory Structure

```text
BCA project/
│
├── StudentsPerformance.csv     # Dataset containing 1,000 student records
├── generate_dataset.py         # Script used to generate the dataset
├── train_model.py              # ML script: trains DecisionTree & saves model.pkl
├── model.pkl                   # Trained Machine Learning model package
├── app.py                      # Flask web application backend
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation & Viva Q&A
│
├── static/
│   ├── css/
│   │   └── style.css           # White and light-blue responsive stylesheet
│   └── js/
│       └── script.js           # Client navigation, live previews, and API caller
│
└── templates/
    └── index.html              # Modern single-page application template
```

---

## 🚀 How to Run the Project

### Prerequisites
* Python 3.8 or higher installed on your computer.
* VS Code or Antigravity IDE.

---

### Step 1: Open the Project in VS Code / Antigravity IDE
Open your terminal inside the project directory:
```bash
cd "BCA project"
```

---

### Step 2: Install Required Libraries
Install the lightweight dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```
*(Or install manually: `pip install flask scikit-learn pandas numpy`)*

---

### Step 3: (Optional) Re-Train the Machine Learning Model
The repository already includes a pre-trained `model.pkl`. If you wish to demonstrate the training step to your professor, run:
```bash
python train_model.py
```
**Output:**
```text
============================================================
STUDENT PERFORMANCE LEVEL PREDICTION - MODEL TRAINING
============================================================
[Step 1] Loading StudentsPerformance.csv dataset...
[Step 2] Calculating average score and assigning performance level labels...
[Step 3] Encoding categorical features for Machine Learning...
[Step 4] Splitting dataset: 80% Training, 20% Testing...
[Step 5] Training Decision Tree Classifier...
Accuracy Score: 95.50%
[Step 6] Saving trained model and metadata to 'model.pkl'...
Success: 'model.pkl' created and ready for Flask web application!
============================================================
```

---

### Step 4: Start the Flask Web Application
Run the backend server:
```bash
python app.py
```

You will see output similar to:
```text
============================================================
 Student Performance Level Prediction - Server Started
 Access website in your browser at: http://127.0.0.1:5050
============================================================
```

---

### Step 5: Open in Your Web Browser
Open your preferred browser (Google Chrome, Microsoft Edge, Safari) and navigate to:
```
http://127.0.0.1:5050
```

---

## 💡 Viva Voce / Presentation Questions & Answers (For BCA Students)

Here are the most common questions college examiners ask during project presentations:

### Q1. Why did you choose a Decision Tree Classifier for this project?
> **Answer:**  
> A Decision Tree is an intuitive, supervised learning algorithm that splits data based on feature thresholds (e.g., math score, reading score). It closely mimics human decision-making, requires minimal data preprocessing, and is easy to interpret and visualize, making it ideal for educational performance classification.

### Q2. What are the features (inputs) and target (output) of your ML model?
> **Answer:**  
> - **Input Features (7):** Gender, Parental Level of Education, Lunch Type, Test Preparation Course, Mathematics Score, Reading Score, Writing Score.  
> - **Target (Output):** Student Performance Category (`Low`, `Medium`, or `High`).

### Q3. What is the difference between Classification and Regression in Machine Learning?
> **Answer:**  
> - **Regression:** Predicts continuous numerical values (e.g., predicting exact marks like 82.4%).  
> - **Classification:** Predicts discrete categorical labels (e.g., classifying a student into `High`, `Medium`, or `Low` categories). Our project is a **multi-class classification problem**.

### Q4. How does the system handle situations where the ML model file (`model.pkl`) is missing?
> **Answer:**  
> The system has a built-in **Rule-Based Prototype Engine**. If `model.pkl` is not found, the website automatically falls back to calculating performance levels directly from the student's average marks:
> - Average < 50% ➔ `Low`
> - Average 50% to 74% ➔ `Medium`
> - Average ≥ 75% ➔ `High`  
> This ensures that the college demonstration never crashes or fails.

### Q5. What is the role of Flask in this project?
> **Answer:**  
> Flask is a lightweight Python Web Framework (WSGI). It serves the frontend HTML/CSS/JS templates and exposes a RESTful API endpoint (`/api/predict`) that receives student data via HTTP POST requests, feeds it to the Scikit-learn model, and returns JSON prediction results to the user interface.

---

## 📜 Academic Declaration
This project is developed as an academic prototype for the Bachelor of Computer Applications (BCA) curriculum, showcasing the practical integration of Machine Learning algorithms with web application development.
