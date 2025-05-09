from gensim.models import KeyedVectors

# Загрузка предобученной модели (например, rusvectores)
model = KeyedVectors.load_word2vec_format('model.bin', binary=True)

def get_similar_words(word, topn=5):
        return model.most_similar(word, topn=topn)

# Пример использования
print(get_similar_words("человек_NOUN"))
