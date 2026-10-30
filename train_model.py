"""
=============================================================================
Student Performance Level Prediction - Model Training Script
BCA Final Year / College Project
Algorithm: Decision Tree Classifier (Scikit-learn)
Dataset: StudentsPerformance.csv
=============================================================================
"""

import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report


def assign_performance_level(avg_score):
    """
    Rule definition based on project specifications:
    - Low Performance: Average marks below 50
    - Medium Performance: Average marks from 50 to below 75
    - High Performance: Average marks 75 or above
    """
    if avg_score < 50:
        return 'Low'
    elif avg_score < 75:
        return 'Medium'
    else:
        return 'High'


def train():
    print("=" * 60)
    print("STUDENT PERFORMANCE LEVEL PREDICTION - MODEL TRAINING")
    print("=" * 60)

    # 1. Load dataset
    print("\n[Step 1] Loading StudentsPerformance.csv dataset...")
    df = pd.read_csv("StudentsPerformance.csv")
    print(f"Dataset successfully loaded with {df.shape[0]} rows and {df.shape[1]} columns.")

    # 2. Calculate average score and performance label
    print("\n[Step 2] Calculating average score and assigning performance level labels...")
    df['average score'] = (df['math score'] + df['reading score'] + df['writing score']) / 3.0
    df['performance level'] = df['average score'].apply(assign_performance_level)

    print("Performance Level Distribution in Dataset:")
    print(df['performance level'].value_counts())

    # 3. Feature Selection & Categorical Mapping
    # Standardize column mappings so inputs from the web form are easily processed
    print("\n[Step 3] Encoding categorical features for Machine Learning...")

    # Define standard mappings (simple, beginner-friendly dictionary mappings)
    gender_map = {'female': 0, 'male': 1}
    lunch_map = {'free/reduced': 0, 'standard': 1}
    test_prep_map = {'none': 0, 'completed': 1}
    parent_edu_map = {
        'some high school': 0,
        'high school': 1,
        'some college': 2,
        "associate's degree": 3,
        "bachelor's degree": 4,
        "master's degree": 5
    }

    # Clean strings to lowercase and strip whitespace
    df_clean = df.copy()
    df_clean['gender'] = df_clean['gender'].str.strip().str.lower().map(gender_map)
    df_clean['lunch'] = df_clean['lunch'].str.strip().str.lower().map(lunch_map)
    df_clean['test preparation course'] = df_clean['test preparation course'].str.strip().str.lower().map(test_prep_map)
    df_clean['parental level of education'] = df_clean['parental level of education'].str.strip().str.lower().map(parent_edu_map)

    feature_cols = [
        'gender',
        'parental level of education',
        'lunch',
        'test preparation course',
        'math score',
        'reading score',
        'writing score'
    ]

    X = df_clean[feature_cols]
    y = df_clean['performance level']

    # 4. Train-Test Split (80% Training, 20% Testing)
    print("\n[Step 4] Splitting dataset: 80% Training, 20% Testing...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training samples: {len(X_train)} | Testing samples: {len(X_test)}")

    # 5. Train Decision Tree Classifier
    print("\n[Step 5] Training Decision Tree Classifier...")
    # Using max_depth=5 prevents overfitting and creates human-interpretable decision boundaries
    model = DecisionTreeClassifier(
        criterion='gini',
        max_depth=5,
        min_samples_split=4,
        random_state=42
    )
    model.fit(X_train, y_train)

    # 6. Model Evaluation
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Evaluation Result:")
    print(f"Accuracy Score: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 7. Save model and metadata package into model.pkl
    print("\n[Step 6] Saving trained model and metadata to 'model.pkl'...")
    model_package = {
        'model': model,
        'feature_cols': feature_cols,
        'gender_map': gender_map,
        'lunch_map': lunch_map,
        'test_prep_map': test_prep_map,
        'parent_edu_map': parent_edu_map,
        'accuracy': round(accuracy * 100, 2),
        'algorithm': 'Decision Tree Classifier (Scikit-learn)',
        'max_depth': 5,
        'trained_samples': len(X_train),
        'test_samples': len(X_test)
    }

    with open("model.pkl", "wb") as f:
        pickle.dump(model_package, f)

    print("Success: 'model.pkl' created and ready for Flask web application!")
    print("=" * 60)


if __name__ == '__main__':
    train()
