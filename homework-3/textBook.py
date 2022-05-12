
from gettext import find
import requests
import bs4
from lxml import etree
import pandas as pd
import time
import convert_numbers

count_page_start = int(input("count page start: "))

count_page_end = int(input("count page end: "))
count_page_end = count_page_end + 1

name_title = input("name of cetegory: ")

illegal_character = ["صوتی" , "PDF کتاب", "دانلود", "رمان", "|", "_", "-", "ترجمه", "اثر","نوشته", "نسخه"]

count_book = 1
dict_data = {
    # "id": [],
    "name": [],
    "authors": [],
    "translator": [],
    "price": [],
    "publisher": [],
    "price_printed": [],
    "date": [],
    "language": [],
    "vol": [],
    "pages": [],
    "isbn": [],
    "description": [],
    "category": [],
    "cover_loc": [],
}

request_result=requests.get("https://fidibo.com/")
soup = bs4.BeautifulSoup(request_result.text, "html.parser")



a_name = soup.find("a", {"title": f"{name_title}"})

link_name_title = f"https://fidibo.com{a_name['href']}?page=1&book_formats%5B%5D=text_book"
print(link_name_title)
request_result=requests.get(link_name_title)
soup = bs4.BeautifulSoup(request_result.text, "html.parser")

id_books = soup.find_all("a")

for cp in range(count_page_start, count_page_end):
    print(f"page: {cp}")

    link_nt = f"https://fidibo.com{a_name['href']}?page={cp}&book_formats%5B%5D=text_book"
    print(link_nt)
    request_result=requests.get(link_nt)
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    title_check = soup.find("title")
    id_books = soup.find_all("a")

    for l in id_books:
        if l.has_key('data-ut-object-id'):
            id = l['data-ut-object-id']
            href_name_book = l['href']
            # print(href_name_book)
            href_name_book = href_name_book.split("-")
            original = []
            for i in range(1, len(href_name_book)):
                if "کتاب" != href_name_book[i]:
                    original.append(href_name_book[i])    
            

            link_books = f"https://fidibo.com/book/{id}"
            request_result=requests.get(link_books)
            soup = bs4.BeautifulSoup(request_result.text, "html.parser")
            name_book_h1 = soup.find("title")
            if name_book_h1.text == "502 Bad Gateway" or name_book_h1.text == "":
                print("Error... 5 Sec ...")
                time.sleep(5)
                id = l['data-ut-object-id']
                link_books = f"https://fidibo.com/book/{id}"
                request_result=requests.get(link_books)
                soup = bs4.BeautifulSoup(request_result.text, "html.parser")
                name_book_h1 = soup.find("title")
            
            # dict_data["name"].append((name_book_h1.text).strip())
            name_book_h1 = (name_book_h1.text).strip()
            if original[0].isnumeric():
                original[0] = convert_numbers.english_to_persian(original[0])
            

            loc_1 = name_book_h1.find(original[0])
            if loc_1 == -1:
                if original[1].isnumeric():
                    original[1] = convert_numbers.english_to_persian(original[1])
                loc_1 = name_book_h1.find(original[1])

            if original[len(original) - 1].isnumeric():
                original[len(original) - 1] = convert_numbers.english_to_persian(original[len(original) - 1])
            loc_2 = name_book_h1.find(original[len(original) - 1])
            
            # print(name_book_h1, loc_1, loc_2, original[0], original[len(original) - 1])
            # print(name_book_h1[loc_1:loc_2 + len(href_name_book[len(href_name_book) - 1])])
            # name_book = name_book_h1[loc_1:loc_2 + len(href_name_book[len(href_name_book) - 1])]
            if loc_2 == -1:
                loc_2 = name_book_h1.find(original[len(original) - 2]) + len(original[len(original) - 1]) + len(original[len(original) - 2]) + 2
                name_book = name_book_h1[loc_1:loc_2]
            else:
                name_book = name_book_h1[loc_1:loc_2 + len(href_name_book[len(href_name_book) - 1])]
            if "کتاب" in name_book:
                name_book = name_book.replace("کتاب", "")

            if name_book == "":
                name_book = soup.find("title").text.strip()
                for ic in illegal_character:
                    if ic in name_book:
                        name_book = name_book.replace(ic, "")
            dict_data["name"].append(name_book)
            print(link_books, name_book)
            authors_ = soup.find_all("li", {"class": "author_title white"})
            if len(authors_) == 2:
                for a in authors_:
                    if "نویسنده" in a.text:
                        temp = (a.text).replace("نویسنده","")
                        temp = (temp).replace(":","")
                        temp = temp.strip()
                        dict_data["authors"].append(temp)
                    if "مترجم" in a.text:
                        temp = (a.text).replace("مترجم","")
                        temp = (temp).replace(":","")
                        temp = temp.strip()
                        dict_data["translator"].append(temp)
            elif len(authors_) == 1:
                    temp = (authors_[0].text).replace("نویسنده","")
                    temp = (temp).replace(":","")
                    dict_data["authors"].append(temp)
                    dict_data["translator"].append("None")
            try:
                book_price = soup.find("span", {"class": "book-price"})
                dict_data["price"].append((book_price.text.replace("تومان", "")))
            except:
                dict_data["price"].append("None")

            try:
                pub_book = soup.find("img", {"alt": "ناشر"})
                publisher = pub_book.find_next_sibling("a")['data-ut-object-title']
                if publisher.find("نشر") != -1:
                    publisher = publisher.replace("نشر", "")
                if publisher.find("انتشارات") != -1:
                    publisher = publisher.replace("انتشارات", "")
                if publisher.find("گروه") != -1:
                    publisher = publisher.replace("گروه", "")
                print(publisher)
                dict_data["publisher"].append(publisher)
            except:
                dict_data["publisher"].append("None")

            try:
                price_book_printed = soup.find("img", {"alt": "قیمت نسخه چاپی"})
                dict_data["price_printed"].append(((price_book_printed.find_next_sibling("span").text).replace("قیمت نسخه چاپی", "")).replace("تومان", ""))
            except:
                dict_data["price_printed"].append("None")

            try:
                date_book = soup.find("img", {"alt": "تاریخ نشر"})
                dict_data["date"].append(date_book.find_next_sibling("span").text)
            except:
                dict_data["date"].append("None")

            try:
                language_book = soup.find("img", {"alt": "زبان"})
                dict_data["language"].append(language_book.parent.text)
            except:
                dict_data["language"].append("None")

            try:
                vol_book = soup.find("img", {"alt": "حجم فایل"})
                dict_data["vol"].append((vol_book.parent.text).replace("مگابایت", ""))
            except:
                dict_data["vol"].append("None")

            try:
                pages_book = soup.find("img", {"alt": "تعداد صفحات"})
                dict_data["pages"].append((pages_book.parent.text).replace("صفحه", ""))
            except:
                dict_data["pages"].append("None")

            try:
                isbn_book = soup.find("img", {"alt": "شابک"})
                dict_data["isbn"].append(isbn_book.find_next_sibling("label").text)
            except:
                dict_data["isbn"].append("None")

            try:
                description_book = soup.find("p", {"dir": "rtl"})
                if description_book is None:
                    description_book = soup.find("p", {"dir": "RTL"})
                    if description_book is None:
                        description_book = soup.find("p", {"class": "more-info book-description"})
                        if description_book is None:
                            description_book = soup.find("p", {"style": "direction: rtl;"})
                dict_data["description"].append(description_book.text)
            except:
                dict_data["description"].append("None")
                    
            
            try:
                image_source = soup.find("img", {"id": "book_img"})
                dict_data["cover_loc"].append(image_source['src'])
            except:
                dict_data["cover_loc"].append("None")
            
            dom = etree.HTML(str(soup))
            category_book = dom.xpath('/html/body/div[1]/nav/ul/li[4]/a/span')
            if len(category_book) != 0:
                dict_data["category"].append(category_book[0].text)
            else:
                category_book = dom.xpath('/html/body/div[1]/nav/ul/li[3]/a/span')
                if len(category_book) != 0:
                    dict_data["category"].append(category_book[0].text)
                else:
                    category_book = dom.xpath('/html/body/div[1]/nav/ul/li[2]/a/span')
                    if len(category_book) != 0:
                        dict_data["category"].append(category_book[0].text)
                    else:
                        dict_data["category"].append("None")
        

for zz in dict_data:
    print(len(dict_data[zz]), zz)
frame = pd.DataFrame(dict_data)


frame.to_csv(f"result/text/{name_title}_textbook_{count_page_start}_{count_page_end-1}.csv")
