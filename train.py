import pandas as pd
import joblib

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Load dataset
data = pd.read_csv("dataset/yoruba_commands.csv")

X = data["text"]
y = data["intent"]

# Create model
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

# Train
model.fit(X, y)

# Save
joblib.dump(model, "models/intent_model.pkl")

print("Training completed successfully.")