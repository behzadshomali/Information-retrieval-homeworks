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

def remove_punctuations(text_tokens):
  punctuations_list = ['،', '.', ':', '؛', '؟', '!', '\'', '\\', '/', '-', 'ـ', '+', '=', '*', ',', '٪', '$', '#', '@', '÷', '<', '>', '|', '}', '{', ']', ']', ')', '(', '\'', '…']
  tokens_without_punc = []

  for token in text_tokens:
    '''
      this if-statement is to remove
      the tokens that are of punctuations
    '''
    if token not in punctuations_list:
      '''
        this for-loop is to replace the 
        punctuations appearing in the middle
        of tokens with a space so we can then
        split the tokens by space and seperately
        extract the words
      '''
      for delimiter in punctuations_list:
        token = token.replace(delimiter, ' ')
      
      for word in token.split():
        tokens_without_punc.append(word.strip())
      
  return tokens_without_punc

def lemma(text_tokens):
  lemmatizer = hzm.Lemmatizer()
  temp = []
  for word in text_tokens:
    temp.append(lemmatizer.lemmatize(word))
  return temp

def preprocess_pipeline(
  df,
  normalize_flag=True,
  remove_stop_words_flag=False,
  remove_punctuations_flag=False,
  lemmatize_flag=False,
):
  
  for index in df.index:
    text = df.loc[index, 'content']
    if normalize_flag:
      text = normalizer(df['content'][index])

    text_tokens = hzm.word_tokenize(text)
  
    if remove_punctuations_flag:
      text_tokens = remove_punctuations(text_tokens)

    if remove_stop_words_flag:  
      text_tokens = removeStopWords(text_tokens)
      df['stop_word'][index] = '/'.join(text_tokens)

    if lemmatize_flag:
      text_tokens = lemma(text_tokens)
      df['lemmatizer'][index] = '/'.join(text_tokens)

    print(f'Preprocessing {index}')

  # df.to_excel("preprocessed_data.xlsx")
