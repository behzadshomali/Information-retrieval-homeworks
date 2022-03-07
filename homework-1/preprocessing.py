import hazm as hzm
import pandas as pd


def stemmer(data):
  stemmer = hzm.Stemmer()
  stem_list = [None] * len(data)
  for i in range(len(data)):
    stem_list[i] = stemmer.stem(data[i])
  return stem_list

def normalizer(data):
  '''
  data would be a single 
  row of dataframe
  '''
  normalizer = hzm.Normalizer()
  return normalizer.normalize(data)

def removeStopWords(text_tokens):
  tokens_without_sw = [word for word in text_tokens if not word in hzm.stopwords_list()]
  return tokens_without_sw

def lemma(text_tokens):
  lemmatizer = hzm.Lemmatizer()
  temp = []
  for word in text_tokens:
    temp.append(lemmatizer.lemmatize(word))
  return temp

def process_normal_sw_lemma(data):
  for index in data.index:
    normalized = normalizer(data['content'][index])
    text_tokens_normal = hzm.word_tokenize(normalized)
    tokens_normal_without_sw = removeStopWords(text_tokens_normal)
    data['stop_word'][index] = ' '.join(tokens_normal_without_sw)

    lemmatized_tokens = lemma(tokens_normal_without_sw)
    data['lemmatizer'][index] = ' '.join(lemmatized_tokens)

  data.to_excel("data_norm_stopWord_lemm.xlsx")


