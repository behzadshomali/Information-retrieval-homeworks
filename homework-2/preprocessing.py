import hazm as hzm


def stemmer(tokens):
    stemmer = hzm.Stemmer()
    stem_list = []
    for token in tokens:
        stem_list.append(stemmer.stem(token))
    return stem_list


def lemma(tokens):
    lemmatizer = hzm.Lemmatizer()
    lemm_list = []
    for word in tokens:
        lemm_list.append(lemmatizer.lemmatize(word))

    return lemm_list


def normalizer(text):
    normalizer = hzm.Normalizer()
    return normalizer.normalize(text)


def removeStopWords(tokens):
    tokens_without_sw = [token for token in tokens if not token in hzm.stopwords_list()]
    return tokens_without_sw


def remove_punctuations(tokens):
    punctuations_list = [
        "،",
        ".",
        ":",
        "؛",
        "؟",
        "!",
        "'",
        "\\",
        "/",
        "-",
        "ـ",
        "+",
        "=",
        "*",
        ",",
        "٪",
        "$",
        "#",
        "@",
        "÷",
        "<",
        ">",
        "|",
        "}",
        "{",
        "[",
        "]",
        ")",
        "(",
        "…",
    ]
    delimiters_list = [
        "،",
        ".",
        ":",
        "؛",
        "؟",
        "!",
        "'",
        "\\",
        "/",
        "-",
        "ـ",
        ",",
        "|",
        "}",
        "{",
        "[",
        "]",
        ")",
        "(",
        "…",
    ]

    tokens_without_punc = []
    for token in tokens:
        if token not in punctuations_list:
            """
            the following for-loop is to replace 
            the punctuations appearing in the middle
            of tokens with a space so we can later
            split the tokens by space and separately
            extract the words
            """
            for delimiter in delimiters_list:
                token = token.replace(delimiter, " ")

            for word in token.split():
                tokens_without_punc.append(word.strip())

    return tokens_without_punc


def preprocess_pipeline(
    query,
    normalize_flag=True,
    remove_stop_words_flag=True,
    remove_punctuations_flag=True,
    lemmatize_flag=True,
    stemmer_flag=True,
):

    if normalize_flag:
        text = normalizer(query)

    query_tokens = hzm.word_tokenize(text)

    if remove_punctuations_flag:
        query_tokens = remove_punctuations(query_tokens)

    if remove_stop_words_flag:
        query_tokens = removeStopWords(query_tokens)

    if lemmatize_flag:
        query_tokens = lemma(query_tokens)

    if stemmer_flag:
        query_tokens = stemmer(query_tokens)

    return query_tokens
