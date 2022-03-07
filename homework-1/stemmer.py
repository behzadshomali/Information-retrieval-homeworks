import hazm as hzm
import pandas as pd
def stemmer(data):
  stemmer = hzm.Stemmer()
  stem_list = [None] * len(data)
  for i in range(len(data)):
    stem_list[i] = stemmer.stem(data[i])
  return stem_list
