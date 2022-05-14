from gettext import find
import requests
import bs4
from lxml import etree
import pandas as pd
import time
import convert_numbers
from random import randint


def extract_main_title(illegal_character, l, soup, dict_data):
    name_book = ""
    id = l['data-ut-object-id']
    href_name_book = l['href']
    href_name_book = href_name_book.split("-")
    
    # extract the original name of the book
    # with all those illegal characters
    original = []
    for i in range(1, len(href_name_book)):
        if "کتاب" != href_name_book[i]:
            original.append(href_name_book[i]) 
    name_book_h1 = soup.find("title")

    # sometimes while searching for book's name, 
    # we face "502 Bad Gateway" error so this if-statement
    # is used to wait for the server to respond again
    if name_book_h1.text == "502 Bad Gateway" or name_book_h1.text == "":
        # print("Error... waiting for 5 sec ...")
        time.sleep(5)
        id = l['data-ut-object-id']
        link_books = f"https://fidibo.com/book/{id}"
        request_result=requests.get(link_books)
        soup = bs4.BeautifulSoup(request_result.text, "html.parser")
        name_book_h1 = soup.find("title")

    try:
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

        if loc_2 == -1:
            loc_2 = name_book_h1.find(original[len(original) - 2]) + len(original[len(original) - 1]) + len(original[len(original) - 2]) + 2
            name_book = name_book_h1[loc_1:loc_2]
        else:
            name_book = name_book_h1[loc_1:loc_2 + len(href_name_book[len(href_name_book) - 1])]
        
        if "کتاب" in name_book:
            name_book = name_book.replace("کتاب", "")
        if "صوتی" in name_book:
            name_book = name_book.replace("صوتی", "")

    except Exception as e:
        # if the book's name was not available
        # we will search for it in the title tag
        if name_book == "" or len(name_book) < 2 or name_book is None:
            name_book = soup.find("title").text.strip()
            for ic in illegal_character:
                if ic in name_book:
                    name_book = name_book.replace(ic, "")

    print(f"name of book: {name_book}")
    if name_book == "" or name_book is None or len(name_book) < 2:
        return False
        # name_book = soup.find("title").text
    else:
        dict_data["name"].append(name_book)
        return True

    #     return False, name_book_h1
    # else:
    #     dict_data["name"].append(name_book)
    #     return True, name_book_h1

def extract_author_translator_broadcaster(mode, soup, dict_data):
    '''
        "mode" determines whether we're working 
        with a text-book or audio-book
        mode: ['text', 'audio']
    '''
    authors_ = soup.find_all("li", {"class": "author_title white"})

    if mode == "audio":
        # if the book has author, 
        # translator, and broadcaster
        if len(authors_) == 3: 
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
                if "گوینده" in a.text:
                    temp = (a.text).replace("گوینده","")
                    temp = (temp).replace(":","")
                    temp = temp.strip()
                    dict_data["broadcaster"].append(temp)
        
        # the book has author
        # and broadcaster
        elif len(authors_) == 2:
            for a in authors_:
                if "نویسنده" in a.text:
                        temp = (a.text).replace("نویسنده","")
                        temp = (temp).replace(":","")
                        temp = temp.strip()
                        dict_data["authors"].append(temp)
                if "گوینده" in a.text:
                        temp = (a.text).replace("گوینده","")
                        temp = (temp).replace(":","")
                        temp = temp.strip()
                        dict_data["broadcaster"].append(temp)
            dict_data["translator"].append("None")

    elif mode == "text":
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

def extract_publisher(soup, dict_data):
    # extract the main name of the publisher
    # by finding and eliminating the additional
    # phrases such as "گروه", "انتشارات", "نشر"
    try:
        pub_book = soup.find("img", {"alt": "ناشر"})
        publisher = pub_book.find_next_sibling("a")['data-ut-object-title']
        if publisher.find("نشر") != -1:
            publisher = publisher.replace("نشر", "")
        if publisher.find("انتشارات") != -1:
            publisher = publisher.replace("انتشارات", "")
        if publisher.find("گروه") != -1:
            publisher = publisher.replace("گروه", "")

        dict_data["publisher"].append(publisher)
    
    # this is the case when the publisher 
    # is not available
    except:
        dict_data["publisher"].append("None")

def extract_printed_price(soup, dict_data):
    try:
        price_book_printed = soup.find("img", {"alt": "قیمت نسخه چاپی"})
        dict_data["price_printed"].append(((price_book_printed.find_next_sibling("span").text).replace("قیمت نسخه چاپی", "")).replace("تومان", ""))
    
    # this is a case that the
    # book's printed price is not available
    except:
        dict_data["price_printed"].append("None")

def extract_price(soup, dict_data):
    try:
        book_price = soup.find("span", {"class": "book-price"})
        dict_data["price"].append((book_price.text.replace("تومان", "")))
    
    # this is a case that the 
    # book's price is not available
    except:
        dict_data["price"].append("None")

def extract_publish_date(soup, dict_data):
    try:
        date_book = soup.find("img", {"alt": "تاریخ نشر"})
        dict_data["date"].append(date_book.find_next_sibling("span").text)
    
    # this is a case that the
    # book's publish date is not available
    except:
        dict_data["date"].append("None")

def extract_language(soup, dict_data):
    try:
        language_book = soup.find("img", {"alt": "زبان"})
        dict_data["language"].append(language_book.parent.text)
    
    # this is a case that the
    # book's language is not available
    except:
        dict_data["language"].append("None")

def extract_volume(soup, dict_data):
    try:
        vol_book = soup.find("img", {"alt": "حجم فایل"})
        dict_data["vol"].append((vol_book.parent.text).replace("مگابایت", ""))
    
    # this is a case that the
    # book's volume is not available
    except:
        dict_data["vol"].append("None")

def extract_pages_count(soup, dict_data):
    try:
        pages_book = soup.find("img", {"alt": "تعداد صفحات"})
        dict_data["pages"].append((pages_book.parent.text).replace("صفحه", ""))
    
    # this is a case that the
    # book's pages count is not available
    except:
        dict_data["pages"].append("None")

def extract_isbn(soup, dict_data):
    try:
        isbn_book = soup.find("img", {"alt": "شابک"})
        dict_data["isbn"].append(isbn_book.find_next_sibling("label").text)
    
    # this is a case that the
    # book's isbn is not available
    except:
        dict_data["isbn"].append("None")

def extract_description(soup, dict_data):
    try:
        # since website Fidibo didn't follow a
        # unique structure, the book's description
        # may exist in one of the following ways
        description_book = soup.find("p", {"dir": "rtl"})
        if description_book is None:
            description_book = soup.find("p", {"dir": "RTL"})
            if description_book is None:
                description_book = soup.find("p", {"class": "more-info book-description"})
                if description_book is None:
                    description_book = soup.find("p", {"style": "direction: rtl;"})
        dict_data["description"].append(description_book.text)
    
    # this is a case that the
    # book's description is not available
    except:
        dict_data["description"].append("None")

def extract_cover_img_link(soup, dict_data):
    try:
        image_source = soup.find("img", {"id": "book_img"})
        dict_data["cover_loc"].append(image_source['src'])
    
    # this is the case that the
    # book's cover image link is not available
    except:
        dict_data["cover_loc"].append("None")

def extract_category(soup, dict_data):
    # the book's category may exist under
    # different pathes such as:
    # Novel
    #  |
    #  |- Fiction
    #       |
    #       |- Romance
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

def save_crawled_data(mode, name_title, count_page_start, count_page_end, dict_data):
    '''
        "mode" determines whether we're working 
        with a text-book or audio-book
        mode: ['text', 'audio']
    '''
    print('Saving data...')
    frame = pd.DataFrame(dict_data)
    frame.to_csv(f"result/{mode}/{name_title}_{mode}book_{count_page_start}_{count_page_end}.csv")

def random_IP_generator():
    return "{}.{}.{}.{}".format(randint(100,255),randint(0,255),randint(0,255),randint(0,255))