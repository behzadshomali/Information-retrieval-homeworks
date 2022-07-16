import os
import pandas as pd
import numpy as np
import convert_numbers



def collect_data():
    """
    combine all textbooks together also the same happens to audiobooks.
    :return:
        text_df: all textbooks
        audio_df: all audiobooks.
    """
    text_df = None
    audio_df = None

    for dir_name in os.listdir():
        if "(" in dir_name:
            for file_name in os.listdir(dir_name):
                print(file_name)

                df = pd.read_csv(f"{dir_name}/{file_name}")

                if "audio" in file_name:
                    if audio_df is None:
                        audio_df = df
                    else:
                        audio_df = pd.concat([audio_df, df])

                elif "text" in file_name:
                    if text_df is None:
                        text_df = df
                    else:
                        text_df = pd.concat([text_df, df])

    print(text_df.shape)
    print(audio_df.shape)
    return text_df, audio_df




def preprocess():
    """
    preprocess data for saving to the elasticsearch that we can query on it.
    :return:
    """
    text_df, audio_df = collect_data()
    text_df.rename(columns={"Unnamed: 0": "index"}, inplace=True)
    audio_df.rename(columns={"Unnamed: 0": "index"}, inplace=True)
    text_df["index"] = range(1, 1 + len(text_df))
    audio_df["index"] = range(1, 1 + len(audio_df))

    text_df = text_df.replace(to_replace="None", value=np.NaN)
    audio_df = audio_df.replace(to_replace="None", value=np.NaN)

    print(text_df.isnull().sum())
    print(audio_df.isnull().sum())

    print("=" * 20)

    no_value_cols = ["translator", "description", "cover_loc"]

    for column in text_df.columns:
        if column in no_value_cols:
            text_df[column] = text_df[column].fillna("ندارد")
        else:
            text_df[column] = text_df[column].fillna("نامشخص")

    for column in audio_df.columns:
        if column in no_value_cols:
            audio_df[column] = audio_df[column].fillna("ندارد")
        else:
            audio_df[column] = audio_df[column].fillna("نامشخص")

    print(text_df.isnull().sum())
    print(audio_df.isnull().sum())

    text_df["price"] = text_df["price"].apply(
        lambda x: x
        if x == "نامشخص" or type(x) == float
        else convert_numbers.persian_to_english(x)
    )
    text_df["price_printed"] = text_df["price_printed"].apply(
        lambda x: x
        if x == "نامشخص" or type(x) == float
        else convert_numbers.persian_to_english(x)
    )
    audio_df["price"] = audio_df["price"].apply(
        lambda x: x
        if x == "نامشخص" or type(x) == float
        else convert_numbers.persian_to_english(x)
    )

    print(text_df.shape)
    print(audio_df.shape)

    text_df.to_csv("data/total_text_books.csv")
    audio_df.to_csv("data/total_audio_books.csv")
