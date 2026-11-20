import os
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


class TaskClassifier:

    def __init__(self):
        self.model = Pipeline([
            ("vectorizer", TfidfVectorizer()),
            ("classifier", LogisticRegression(max_iter=1000))
        ])

        self.model_path = os.path.join(
            os.path.dirname(__file__),
            "task_classifier.pkl"
        )

        self.is_trained = False

    def train(self):

        training_data = [
            "customer cannot login to account",
            "reset my password",
            "user having authentication issue",
            "payment transaction failed",
            "refund money for failed payment",
            "billing issue with invoice",
            "website page is not loading",
            "application server error",
            "system performance is slow",
            "send monthly sales report",
            "generate business analytics report",
            "prepare customer data report"
        ]

        labels = [
            "support",
            "support",
            "support",
            "payment",
            "payment",
            "payment",
            "technical",
            "technical",
            "technical",
            "report",
            "report",
            "report"
        ]

        self.model.fit(training_data, labels)
        self.is_trained = True

        joblib.dump(self.model, self.model_path)

        return "ML model trained successfully!"

    def predict(self, task_description):

        if not self.is_trained:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                self.is_trained = True
            else:
                self.train()

        prediction = self.model.predict([task_description])

        return prediction[0]


task_classifier = TaskClassifier()