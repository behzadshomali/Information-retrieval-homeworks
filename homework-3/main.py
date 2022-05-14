import requests
import bs4
from utils import *

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
            if l.has_attr('data-ut-object-id'):
                id = l['data-ut-object-id']            
                link_books = f"https://fidibo.com/book/{id}"
                headers={"X-Forwarded-For":random_IP_generator()}
                request_result=requests.get(link_books, headers=headers)
                soup = bs4.BeautifulSoup(request_result.text, "html.parser")
                
                try:
                    # print(link_books)
                    flag = extract_main_title(illegal_character, l, soup, dict_data)
                    if not flag:
                        print("name error1")
                        time.sleep(3)
                        flag = extract_main_title(illegal_character, l, soup, dict_data)
                    if not flag:
                        print("name error2")
                        time.sleep(3)
                        flag = extract_main_title(illegal_character, l, soup, dict_data)
                    if not flag:
                        continue
                    extract_author_translator_broadcaster(mode, soup, dict_data)
                    extract_price(soup, dict_data)
                    extract_publisher(soup, dict_data)
                    extract_publish_date(soup, dict_data)
                    extract_language(soup, dict_data)
                    extract_volume(soup, dict_data)
                    extract_description(soup, dict_data)
                    extract_cover_img_link(soup, dict_data)
                    extract_category(soup, dict_data)

                    # these information are only
                    # available in text mode
                    if mode == 'text':
                        extract_printed_price(soup, dict_data)
                        extract_pages_count(soup, dict_data)
                        extract_isbn(soup, dict_data)
                except:
                    pass

                if len(dict_data["name"]) % 10 == 0:
                    print(f"{len(dict_data['name'])} books are already crawled!")
    
    save_crawled_data(mode, name_title, count_page_start, count_page_end, dict_data)