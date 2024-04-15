from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similar_courses(corpus, prompt):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    vectorized_sentence = vectorizer.transform([prompt])
    similarities = cosine_similarity(vectorized_sentence, X).flatten()
    similarity_threshold = 0.1
    similar_indices = [i for i, value in enumerate(similarities) if value >= similarity_threshold]
    similar_sentences = [corpus[i] for i in similar_indices]
    return similar_sentences