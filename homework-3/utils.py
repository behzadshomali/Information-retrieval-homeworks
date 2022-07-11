from gettext import find
import requests
import bs4
from lxml import etree
import pandas as pd
import time
import convert_numbers
from random import randint


def extract_main_title(illegal_character, l, soup):
    name_book = ""
    id = l["data-ut-object-id"]
    href_name_book = l["href"]
    href_name_book = href_name_book.split("-")

    # extract the original name of the book
    # with all those illegal characters
    # e.g. "کتاب اثر مرکب" while we only
    # need "اثر مرکب"
    original = []
    for i in range(1, len(href_name_book)):
        if "کتاب" != href_name_book[i]:
            original.append(href_name_book[i])

    name_book_h1 = soup.find("title")

    # sometimes while searching for book's name,
    # we face "502 Bad Gateway" error so this if-statement
    # is used to wait for the server to respond again
    if name_book_h1.text == "502 Bad Gateway" or name_book_h1.text == "":
        print("Error... waiting for 5 sec ...")
        time.sleep(5)
        id = l["data-ut-object-id"]
        link_books = f"https://fidibo.com/book/{id}"
        request_result = requests.get(link_books)
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
            original[len(original) - 1] = convert_numbers.english_to_persian(
                original[len(original) - 1]
            )
        loc_2 = name_book_h1.find(original[len(original) - 1])

        if loc_2 == -1:
            loc_2 = (
                name_book_h1.find(original[len(original) - 2])
                + len(original[len(original) - 1])
                + len(original[len(original) - 2])
                + 2
            )
            name_book = name_book_h1[loc_1:loc_2]
        else:
            name_book = name_book_h1[
                loc_1 : loc_2 + len(href_name_book[len(href_name_book) - 1])
            ]

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
        return {"status": False}
    else:
        return {"status": True, "name": name_book}


def extract_author_translator_broadcaster(mode, soup):
    """
        "mode" determines whether we're working 
        with a text-book or audio-book
        mode: ['text', 'audio']
    """
    try:
        authors_ = soup.find_all("li", {"class": "author_title white"})
        if mode == "audio":
            # if the book has author,
            # translator, and broadcaster
            if len(authors_) == 3:
                for a in authors_:
                    if "نویسنده" in a.text:
                        author = (a.text).replace("نویسنده", "")
                        author = (author).replace(":", "")
                        author = author.strip()
                    if "مترجم" in a.text:
                        translator = (a.text).replace("مترجم", "")
                        translator = (translator).replace(":", "")
                        translator = translator.strip()
                    if "گوینده" in a.text:
                        broadcaster = (a.text).replace("گوینده", "")
                        broadcaster = (broadcaster).replace(":", "")
                        broadcaster = broadcaster.strip()

            # if the book has author
            # and broadcaster (it is
            # probably a Persian book,
            # so it has no translator)
            elif len(authors_) == 2:
                translator = "None"
                for a in authors_:
                    if "نویسنده" in a.text:
                        author = (a.text).replace("نویسنده", "")
                        author = (author).replace(":", "")
                        author = author.strip()
                    if "گوینده" in a.text:
                        broadcaster = (a.text).replace("گوینده", "")
                        broadcaster = (broadcaster).replace(":", "")
                        broadcaster = broadcaster.strip()

            return {
                "status": True,
                "authors": author,
                "translator": translator,
                "broadcaster": broadcaster,
            }

        elif mode == "text":
            # if the book has author
            # and translator
            if len(authors_) == 2:
                for a in authors_:
                    if "نویسنده" in a.text:
                        author = (a.text).replace("نویسنده", "")
                        author = (author).replace(":", "")
                        author = author.strip()
                    if "مترجم" in a.text:
                        translator = (a.text).replace("مترجم", "")
                        translator = (translator).replace(":", "")
                        translator = translator.strip()

            # if the book has only
            # author (it is probably a
            # Persian book, so it has
            # no translator)
            elif len(authors_) == 1:
                translator = "None"
                author = (authors_[0].text).replace("نویسنده", "")
                author = (author).replace(":", "")
                author = author.strip()

            return {"status": True, "authors": author, "translator": translator}
    except Exception as e:
        return {"status": False}


def extract_publisher(soup):
    """
    extract the main name of the publisher
    by finding and eliminating the additional
    phrases such as "گروه", "انتشارات", "نشر"
    e.g. "گروه انتشارات قاصدک" -> "قاصدک"
    """
    try:
        pub_book = soup.find("img", {"alt": "ناشر"})
        publisher = pub_book.find_next_sibling("a")["data-ut-object-title"]
        if publisher.find("نشر") != -1:
            publisher = publisher.replace("نشر", "")
        if publisher.find("انتشارات") != -1:
            publisher = publisher.replace("انتشارات", "")
        if publisher.find("گروه") != -1:
            publisher = publisher.replace("گروه", "")

        return {"status": True, "publisher": publisher}

    # this is the case when the publisher
    # is not available
    except:
        return {"status": True, "publisher": "None"}


def extract_printed_price(soup):
    try:
        price_book_printed = soup.find("img", {"alt": "قیمت نسخه چاپی"})
        return {
            "status": True,
            "price_printed": (price_book_printed.find_next_sibling("span").text)
            .replace("قیمت نسخه چاپی", "")
            .replace("تومان", ""),
        }

    # this is a case that the
    # book's printed price is not available
    except:
        return {"status": True, "price_printed": "None"}


def extract_price(soup):
    try:
        book_price = soup.find("span", {"class": "book-price"})
        return {"status": True, "price": (book_price.text.replace("تومان", ""))}

    # this is a case that the
    # book's price is not available
    except:
        return {"status": True, "price": "None"}


def extract_publish_date(soup):
    try:
        date_book = soup.find("img", {"alt": "تاریخ نشر"})
        return {"status": True, "date": date_book.find_next_sibling("span").text}

    # this is a case that the
    # book's publish date is not available
    except:
        return {"status": True, "date": "None"}


def extract_language(soup):
    try:
        language_book = soup.find("img", {"alt": "زبان"})
        return {"status": True, "language": language_book.parent.text}

    # this is a case that the
    # book's language is not available
    except:
        return {"status": True, "language": "None"}


def extract_volume(soup):
    try:
        vol_book = soup.find("img", {"alt": "حجم فایل"})
        return {"status": True, "vol": (vol_book.parent.text).replace("مگابایت", "")}

    # this is a case that the
    # book's volume is not available
    except:
        return {"status": True, "vol": "None"}


def extract_pages_count(soup):
    try:
        pages_book = soup.find("img", {"alt": "تعداد صفحات"})
        return {"status": True, "pages": (pages_book.parent.text).replace("صفحه", "")}

    # this is a case that the
    # book's pages count is not available
    except:
        return {"status": True, "pages": "None"}


def extract_isbn(soup):
    try:
        isbn_book = soup.find("img", {"alt": "شابک"})
        return {"status": True, "isbn": isbn_book.find_next_sibling("label").text}

    # this is a case that the
    # book's isbn is not available
    except:
        return {"status": True, "isbn": "None"}


def extract_description(soup):
    try:
        # since website "Fidibo" didn't follow a
        # unique structure, the book's description
        # may exist in one of the following paths
        description_book = soup.find("p", {"dir": "rtl"})
        if description_book is None:
            description_book = soup.find("p", {"dir": "RTL"})
            if description_book is None:
                description_book = soup.find(
                    "p", {"class": "more-info book-description"}
                )
                if description_book is None:
                    description_book = soup.find("p", {"style": "direction: rtl;"})
        return {"status": True, "description": description_book.text}

    # this is a case that the
    # book's description is not available
    except:
        return {"status": True, "description": "None"}


def extract_cover_img_link(soup):
    try:
        image_source = soup.find("img", {"id": "book_img"})
        return {"status": True, "cover_loc": image_source["src"]}

    # this is the case that the
    # book's cover image link is not available
    except:
        return {"status": True, "cover_loc": "None"}


def extract_category(soup):
    """
    the book's category may exist under
    different paths such as:
    Novel
      |
      |- Fiction
           |
           |- Romance
    """
    dom = etree.HTML(str(soup))
    category_book = dom.xpath("/html/body/div[1]/nav/ul/li[4]/a/span")
    if len(category_book) != 0:
        return {"status": True, "category": category_book[0].text}
    else:
        category_book = dom.xpath("/html/body/div[1]/nav/ul/li[3]/a/span")
        if len(category_book) != 0:
            return {"status": True, "category": category_book[0].text}
        else:
            category_book = dom.xpath("/html/body/div[1]/nav/ul/li[2]/a/span")
            if len(category_book) != 0:
                return {"status": True, "category": category_book[0].text}
            else:
                return {"status": True, "category": "None"}


def save_crawled_data(mode, name_title, count_page_start, count_page_end, dict_data):
    """
        "mode" determines whether we're working 
        with a text-book or audio-book
        mode: ['text', 'audio']
    """
    print("Saving data...")
    frame = pd.DataFrame(dict_data)
    frame.to_csv(
        f"result/{mode}/{name_title}_{mode}book_{count_page_start}_{count_page_end}.csv"
    )


def random_IP_generator():
    """
    This function generates a random IP address,
    so that we can spoof the IP address of the
    client we're using to crawl the website. In
    this case, we prevent the website from blocking
    our IP address.
    """
    return "{}.{}.{}.{}".format(
        randint(100, 255), randint(0, 255), randint(0, 255), randint(0, 255)
    )
