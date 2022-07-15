# Information Retrieval (IR) Homework

In this repository, the result of our teamwork (Hojjat Rezaei, 
Navid All Gharaee, Amirlai Vojdanifard, and I) are gathered in the form of different folders which are as follows:

* preprocess_index_text
* data_crawling 
* <NAME OF 3rd ONE>



## Data crawling:
In this project, we were supposed to crawl data from the website *https://fidibo.com/* - a Persian website containing the information of a ton of text/audiobooks. There were various categories that our program had to crawl each one separately. The categories are as follows:

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

</br>
It is worth mentioning that, while it is highly plausible that all of the aforementioned fields are not defined for a book, our crawler has been robustly designed to handle those exceptional cases. Furthermore, the crawler identifies and ignores the duplicate links.