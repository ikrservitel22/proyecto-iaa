import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def retrain():
    df = pd.read_csv("data.csv")

    if "text" not in df.columns:
        raise Exception("CSV mal formado: falta header text,label")

    texts = df["text"]
    labels = df["label"]

    vectorizer = CountVectorizer(ngram_range=(1,2))
    X = vectorizer.fit_transform(texts)

    model = MultinomialNB()
    model.fit(X, labels)

    pickle.dump((vectorizer, model), open("models/model.pkl", "wb"))

    print("Modelo reentrenado con", len(df), "ejemplos")