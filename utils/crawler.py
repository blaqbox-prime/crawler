import httpx
from bs4 import BeautifulSoup
from models.Book import Book, Metadata
from datetime import datetime


class BooksCrawler:

    def __init__(self):

        self.base_url = "https://books.toscrape.com"

    def crawl_books(self):
        # fetch page content
        books, page = self.crawl_books_by_page(6)        
        # Crawl multiple pages
        page_count_container = page.find("ul", class_="pager")

        max_pages = int(page_count_container.find("li", class_="current").text.strip().split()[-1]) if page_count_container else 1
        current_page = int(page_count_container.find("li", class_="current").text.strip().split()[1]) if page_count_container else 1

        print(f"Current page: {current_page}, Max pages: {max_pages}")
        return { "current_page": current_page, "max_pages": max_pages, "books": books }


    def crawl_books_by_page(self, page_number: int):

        # fetch page content
        page_slug = f"catalogue/page-{page_number}.html" if page_number > 1 else ""
        response = httpx.get(f"{self.base_url}/{page_slug}")
        page = BeautifulSoup(response.content, "lxml")

        anchors = [book_container.find("h3").find("a")["href"].strip() for book_container in page.find_all("article", class_="product_pod")]

        links_to_books = [self.base_url + "/catalogue/" + link for link in anchors[:5]] 

        books = []
        

        # fetch individual book page

        for link in links_to_books:
            b = self.scrape_book(link)
            books.append(b)
        
        return books, page

    def scrape_book(self, book_url: str) -> Book:
        response = httpx.get(book_url)

        book_page = BeautifulSoup(response.content, "lxml")
        

        # extract book details

        title = book_page.find("div", class_="product_main").find("h1").text.strip()

        description = book_page.find("div", id="product_description").find_next_sibling("p").text.strip()

        category = book_page.find("ul", class_="breadcrumb").find_all("li")[2].find("a").text.strip()

        cover_image_url = self.base_url + book_page.find("div", class_="item active").find("img")["src"].strip()[5:]

        rating_class = book_page.find("p", class_="star-rating")["class"][1]

        rating_mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

        rating = rating_mapping.get(rating_class, 0)
        

        # Parse Table for prices, availability, and number of reviews

        rows = book_page.find("table", class_="table table-striped").find_all("tr")

        price_excluding_tax = float(rows[2].find("td").text.strip()[1:])

        price_including_tax = float(rows[3].find("td").text.strip()[1:])

        availability = rows[5].find("td").text.strip()

        number_of_reviews = int(rows[6].find("td").text.strip())
        

        return Book(
                title=title,
                description=description,

                category=category,

                prices={

                    "excluding_tax": price_excluding_tax,

                    "including_tax": price_including_tax

                },

                availability=availability,

                number_of_reviews=number_of_reviews,

                cover_image_url=cover_image_url,
                rating=rating,

                metadata=Metadata(

                    crawl_timestamp=datetime.now(),
                    status=str(response.status_code),
                    source_url=book_url
                )
            )