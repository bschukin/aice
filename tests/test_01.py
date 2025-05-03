import json
import spacy
from natasha import (
    Doc,
    Segmenter,
    NewsEmbedding,  # Для современных моделей
    NewsMorphTagger,
    MorphVocab,
    NewsSyntaxParser
)

def map_entity(word: str, dictionary: dict) -> str:
    for en_term, ru_terms in dictionary.items():
        if word.lower() in ru_terms:
            return en_term
    return None  # Если не найдено

def test_one():
    print()
    nlp = spacy.load("ru_core_news_lg")

    with open('entities.json', 'r', encoding='utf-8') as f:
        entities_dict = json.load(f)

    text = "Открой договор, где сумма больше 100"
    doc = nlp(text)

    entities = []
    for token in doc:
        print(token, token.pos_, token.lemma_)
        # if token.pos_ in ["NOUN", "PROPN"]:  # Существительные
        #     print(token.text, token.pos_)
        #     entity = map_entity(token.text, entities_dict)
        #     if entity:
        #         entities.append(entity)

    #print(entities)

def test_2():
    print()
    segmenter = Segmenter()
    emb = NewsEmbedding()  # Современная модель эмбеддингов
    morph_tagger = NewsMorphTagger(emb)  # Морфологический анализатор
    morph_vocab = MorphVocab()  # Для лемматизации
    syntax_parser = NewsSyntaxParser(emb)  # Синтаксический парсер

    with open('entities.json', 'r', encoding='utf-8') as f:
        entities_dict = json.load(f)

    text = "Пользователи, с именем на А"

    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)  # Синтаксический разбор

    entities = []
    for token in doc.tokens:
        token.lemmatize( )
        print(token)
        # if token.pos_ in ["NOUN", "PROPN"]:  # Существительные
        #     print(token.text, token.pos_)
        #     entity = map_entity(token.text, entities_dict)
        #     if entity:
        #         entities.append(entity)

    #print(entities)