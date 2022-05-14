from time import sleep
import requests
import bs4
from utils import *


if __name__ == "__main__":
    mode = input("Mode [audio/text]: ").strip()
    count_page_start = int(input("Start page: "))
    count_page_end = int(input("End page: "))
    name_title = input("Name of category: ")

    request_result=requests.get("https://fidibo.com/")
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
    tt = soup.find("a", {"title": f"{name_title}"})

    if mode == 'audio':
        dict_data = {
            "name": [],
            "authors": [],
            "translator": [],
            "broadcaster": [],
            "price": [],
            "publisher": [],
            "date": [],
            "language": [],
            "vol": [],
            "description": [],
            "category": [],
            "cover_loc": [],   
        }

        illegal_character = ["کتاب", "اثر", "صوتی", "-", "|", "اثر", "اثری از", "فیدیبو"]

    elif mode == 'text':
        dict_data = {
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

        illegal_character = [
                "صوتی", 
                "PDF کتاب", 
                "دانلود", 
                "رمان", 
                "|", 
                "_", 
                "-", 
                "ترجمه", 
                "اثر",
                "نوشته", 
                "نسخه",
                "(نسخه PDF)"
        ]

    for cp in range(count_page_start, count_page_end+1):
        print(f"Page: {cp}")
        if mode == 'text':
            link_nt = f"https://fidibo.com{tt['href']}?page={cp}&book_formats%5B%5D=text_book"
        elif mode == 'audio':
            link_nt = f"https://fidibo.com{tt['href']}?page={cp}&book_formats%5B%5D=audio_book"
        request_result=requests.get(link_nt)
        soup = bs4.BeautifulSoup(request_result.text, "html.parser")
        id_books = soup.find_all("a")

        for l in id_books:
            # check whether the tag has the 
            # "data-ut-object-id" attribute
            try:
                if l.has_attr('data-ut-object-id'):
                    id = l['data-ut-object-id']            
                    link_books = f"https://fidibo.com/book/{id}"
                    headers={"X-Forwarded-For":random_IP_generator()}
                    request_result=requests.get(link_books, headers=headers)
                    soup = bs4.BeautifulSoup(request_result.text, "html.parser")
                    
                    results = []

                    name_result = extract_main_title(illegal_character, l, soup)
                    results.append(name_result)

                    authors_result =  extract_author_translator_broadcaster(mode, soup)
                    results.append(authors_result)

                    price_result = extract_price(soup)
                    results.append(price_result)

                    publisher_result = extract_publisher(soup)
                    results.append(publisher_result)

                    date_result = extract_publish_date(soup)
                    results.append(date_result)

                    language_result = extract_language(soup)
                    results.append(language_result)

                    vol_result = extract_volume(soup)
                    results.append(vol_result)

                    description_result = extract_description(soup)
                    results.append(description_result)

                    cover_loc_result = extract_cover_img_link(soup)
                    results.append(cover_loc_result)

                    category_result = extract_category(soup)
                    results.append(category_result)

                    # these information are only
                    # available in text mode
                    if mode == 'text':
                        price_printed_result = extract_printed_price(soup)
                        results.append(price_printed_result)

                        pages_result = extract_pages_count(soup)
                        results.append(pages_result)

                        isbn_result = extract_isbn(soup)
                        results.append(isbn_result)

                    is_everyhing_ok = True
                    for result in results: 
                        if result['status'] == False:
                            is_everyhing_ok = False
                            break
                    
                    if is_everyhing_ok:
                        for key in dict_data.keys():
                            for result in results:
                                if key in result.keys():
                                    dict_data[key].append(result[key])
                                    break

                    if len(dict_data["name"]) % 10 == 0:
                        print(f"{len(dict_data['name'])} books are already crawled!")
            except Exception as e:
                print(e)
                sleep(5)
    
    for k, v in dict_data.items():
        print(f"{k}: {len(v)}")
    save_crawled_data(mode, name_title, count_page_start, count_page_end, dict_data)