# Information Retrieval (IR) Homework

In this repository, the result of our teamwork (Hojjat Rezaei, 
Navid All Gharaee, Amirali Vojdanifard, and I) for the Information Retrieval Course homework are gathered in the form of the following phases/directories:

* [Text preprocessing & indexing](#text-preprocessing--indexing)
* [Cosine distance & Query expansion](#cosine-distance--query-expansion)
* [Data crawling](#data-crawling)
* [Elastic search](#elastic-search)
* [Collaborative Filtering](#collaborative-filtering)

## Text preprocessing & indexing:
In this phase, we were supposed to work with a dataset containing information of 2824 provided in <a href="https://github.com/mohamad-dehghani/persian-pdf-books-dataset">here</a>. In this regard, first, we preprocessed and tokenized the content of each book. As the next step, we performed invert-indexing on the extracted tokens. 
Please note that since the process of preprocessing different pieces of text was completely independently done, in order to speed up the process, we performed preprocessing step via multiple threads (user can specify the number of threads by `--threads`)

### Preprocessing:
In this step, we performed various text preprocessing techniques such that users can enable/disable each of them, based on their needs, by passing a `True` flag while running the program.
       

       main.py [-h] [--raw-data-path RAW_DATA_PATH]
               [--preprocessed-data-path PREPROCESSED_DATA_PATH]
               [--indexed-data-path INDEXED_DATA_PATH]
               [--threads THREADS] [--normalize]
               [--remove-stop-words] [--remove-punctuations]
               [--lemmatize] [--stemmer] [-v]

The used text preprocessing techniques are as follows:
* normalize
* remove punctuations
* remove stop words
* lemmatize
* stemmer

### Invert indexing:
By having preprocessed tokens in hand, the invert-indexing step was so straightforward. We only had to create a dictionary such that its keys were tokens and its values were the index(ID) of each document containing that token.


## Cosine distance & Query expansion:
In this phase, we use the extracted tokens from [last phase](#text-preprocessing--indexing) to compute the cosine similarity between different documents. 

To do that, first we have to compute TF-IDF (<u>T</u>erm <u>F</u>requency <u>I</u>nverse <u>D</u>ocument <u>F</u>requency). To save computational resources and make it easier to compute TF-IDF, we implemented separate methods for computing TF-IDF for terms that appeared in documents and also appeared in input queries.

Since it is crucial to perform the same preprocessing methods that are used for indexing documents to preprocess the input query, just like in the previous phase the user can/should specify the preprocessing methods to use by flags. The complete list of flags is as follows:


       main.py [-h] [-v] [-k K]
               [-i INVERTED_INDEXING_DATAFRAME_PATH]
               [-p PREPROCESSED_DATAFRAME_PATH] [--normalize]
               [--remove-stop-words] [--remove-punctuations]
               [--lemmatize] [--stemmer]

The output of this phase is `k` documents with the least cosine distance from the input query as well as their distance. Furthermore, the output will be saved in the format `JSON` file.


## Data crawling:
In this project, we were supposed to crawl data from the website *https://fidibo.com/* - a Persian website containing the information of a ton of text/audio books. There were various categories that our program had to crawl each one separately. The categories are as follows:

<p align="center">
<img 
       src="./figures/books_categories.png"
       width="85%">
</p>

Although numerous information fields were shared between audiobooks and textbooks, each of them had its specific fields. The extracted fields for each type of book (audio/text) are as follows:

<details>
<summary>Text books</summary>

* Title
* Authors
* Translator
* Price
* Publisher
* Printed price
* Publication date
* Language
* Volume <sub>(in Megabyte)</sub>
* Number of pages
* ISBN
* Description
* Category
* Book's cover address
</details>

<details>
<summary>Audio books</summary>

* Title
* Authors
* Translator
* Broadcaster
* Price
* Publisher
* Printed price
* Publication date
* Language
* Volume <sub>(in Megabyte)</sub>
* Description
* Category
* Book's cover address
</details>

It is worth mentioning that, while it is highly plausible that all of the aforementioned fields are not defined for a book, our crawler has been robustly designed to handle those exceptional cases. Furthermore, the crawler identifies and ignores the duplicate links.

## Elastic Search:
First, we combine all data from the categories we previously crawled in the last phase into two dataframes - text_df and audio_df. After that, we need to preprocess data to use them for elasticsearch.
The preprocessing steps that we have done includes:
1. Converting all `None` to np.NaN
2. If ***translator***, ***description***, and ***ioc_cover*** are null in ***textbooks***, we replace them with **have not** and the for other features, we replace them with **unknown**.
3. If ***translator*** and ***description*** are null in ***audiobooks***, we replace them with **have not**. On the other side for other features, we replace it with **unknowns**.
4. Converting all numbers to English digits.

Finally, we transfer our data to Elasticsearch and view our data with the help of ***Kibana***.
<p align="center">
<img 
       src="./figures/elasticsearch.png"
       width="85%">
</p>

## Collaborative Filtering:
User Based:
1. Calculate similarity between selected user and all users.
   - Smoothing ratings: 
     - **$\overline{r_{i}}=\Sigma_{p}r_{ip}$**
     - **$r^\prime_{ip}=r_{ip} - \overline{r}_{i}$**  
   - Similarity:
     - **$Sim(a,b)=\frac{\Sigma_{p} r^\prime_{ap} * r^\prime_{bp}} {\sqrt{r_{ap}^{2}} * \sqrt{r_{bp}^{2}}}$**
2. Calculate ratings to movies that user have not seen them.
   - $$r_{up}=\frac{\Sigma_{i \in users}sim(u,i)* r_{ip} }{\Sigma_{i \in users}|sim(u,i)|} + \overline{r}_{u}$$
3. Normalization and get Top 10 ratings.
   - $$newValue =(\frac{value - minData}{maxData - minData}) * (newMaxData - newMinData) + newMinData$$
 

Item Based:
1. Calculate similarity between all movies.
   - **$Sim(\overrightarrow{A}, \overrightarrow{B}) = \frac{\overrightarrow{A} . \overrightarrow{B}}{\parallel\overrightarrow{A}\parallel * \parallel\overrightarrow{B}\parallel} $**
2. Calculate ratings to movies that user have not seen them.
   - **$rating(U, I_{j}) = \frac{\Sigma_{k} rating(U, I_{k}) * Sim_{jk}}{\Sigma_{k}Sim_{jk}}$**
