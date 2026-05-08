def predict(text):
    input_emb = model.encode([text])

    best_label = None
    best_score = -1

    for label, vecs in embeddings.items():
        scores = cosine_similarity(input_emb, vecs)[0]
        if max(scores) > best_score:
            best_score = max(scores)
            best_label = label

    return best_label