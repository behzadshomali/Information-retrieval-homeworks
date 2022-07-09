# "hazm" is a library used for
# processing Persian text data
import hazm as hzm


def stemmer(data):
    stemmer = hzm.Stemmer()
    stem_list = []
    for i in data:
        stem_list.append(stemmer.stem(i))
    return stem_list


def lemma(text_tokens):
    lemmatizer = hzm.Lemmatizer()
    temp = []
    for word in text_tokens:
        temp.append(lemmatizer.lemmatize(word))

    return temp


def normalizer(data):
    """
    data: a row of the dataframe
    """
    normalizer = hzm.Normalizer()
    return normalizer.normalize(data)


def removeStopWords(text_tokens):
    tokens_without_sw = [
        word for word in text_tokens if not word in hzm.stopwords_list()
    ]
    return tokens_without_sw


def remove_punctuations(text_tokens):
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
    for token in text_tokens:
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
    df,
    output,  # output is a list used to store the result of each thread
    normalize_flag=True,
    remove_stop_words_flag=False,
    remove_punctuations_flag=False,
    lemmatize_flag=False,
    stemmer_flag=False,
    show_logs=False,
):
    """
    input text 
        ↳ [normalize]
            ↳ tokenize
                ↳ [remove punctuations] 
                    ↳ [remove stop words]
                        ↳ [lemmatize]
                            ↳ [stemmer]
                                ↳ output text
    """
    for index in df.index:
        text = df.loc[index, "content"]
        if normalize_flag:
            text = normalizer(df["content"][index])

        text_tokens = hzm.word_tokenize(text)

        if remove_punctuations_flag:
            text_tokens = remove_punctuations(text_tokens)

        if remove_stop_words_flag:
            text_tokens = removeStopWords(text_tokens)

        if lemmatize_flag:
            text_tokens = lemma(text_tokens)

        if stemmer_flag:
            text_tokens = stemmer(text_tokens)
        
        df["preprocessed"][index] = "/".join(text_tokens)

        if show_logs:
            print(f"Preprocessed {index}")

    output.append(df)


def invert_indexing(df, show_logs=False):
    inverted_index = {}
    for index in df.index:
        try:
            text_tokens = df.loc[index, "preprocessed"]
            for token in set(text_tokens.split("/")):
                inverted_index.setdefault(token, [])
                inverted_index[token].append(index)
            if show_logs:
                print(f"Inverted indexing {index}")
        except:
            pass
    return inverted_index
