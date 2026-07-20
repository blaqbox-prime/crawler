import httpx 
from bs4 import BeautifulSoup
from models.Book import Book, Metadata
from datetime import datetime
from utils.logger import log_scrape_error
import asyncio
from utils.settings import get_settings

class BooksCrawler:

    def __init__(self):
        self.client = httpx.AsyncClient()
        self.base_url = get_settings().crawl_base_url

    async def crawl_books(self, page_number: int = -1):
        all_books: list[Book] = []
        max_pages = await self.get_page_count()
        # max_pages = 10
        
        # if page_number == -1 scrape all books  
        if page_number == -1:
            #get all pages
            for page_number in range(1, max_pages + 1):
                new_books = await self.crawl_books_by_page(page_number)
                all_books.extend(new_books)        

        else:
            # Fetch the specified page only
            all_books = await self.crawl_books_by_page(page_number)
        
        return { "current_page": page_number, "pages": max_pages, "count": len(all_books), "books": all_books }

    async def get_page_count(self):
        # Get Page Count
        response = await self.client.get(f"{self.base_url}")
        page = BeautifulSoup(response.content, "lxml")
        page_count_container = page.find("ul", class_="pager")
        max_pages = int(page_count_container.find("li", class_="current").text.strip().split()[-1]) if page_count_container else 1
        return max_pages
            
    async def crawl_books_by_page(self, page_number: int):
        # fetch page content
        page_slug = f"{self.base_url}/catalogue/page-{page_number}.html" if page_number > 1 else self.base_url
        response = await self.client.get(page_slug)
        page = BeautifulSoup(response.content, "lxml")

        anchors = [book_container.find("h3").find("a")["href"].strip() for book_container in page.find_all("article", class_="product_pod")]
        link_prefix = "/catalogue/" if page_number > 1 else "/"
        links_to_books = [self.base_url + link_prefix + link for link in anchors] 
        books = []
        
        try:
                # fetch individual book page
            tasks = [self.client.get(link) for link in links_to_books]
            responses = await asyncio.gather(*tasks)
        except Exception as e:
            print("Something went wrong fetching links", e)
            return
        
        for response in responses:
            try:
                b = await self.scrape_book(response.content, response.status_code, str(response.url))
                books.append(b)
            except Exception as e:
                # write error to a log
                log_scrape_error(response.url, e)
                continue
        
        return books

    async def scrape_book(self, html_bytes: bytes, status_code: int, url: str) -> Book:
        try:
            book_page = BeautifulSoup(html_bytes, "lxml")
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
            upc = rows[0].find("td").text.strip()[1:]

            price_excluding_tax = float(rows[2].find("td").text.strip()[1:])
            price_including_tax = float(rows[3].find("td").text.strip()[1:])
            availability = rows[5].find("td").text.strip()
            number_of_reviews = int(rows[6].find("td").text.strip())
       
            
            return Book(
                    id=upc,
                    title=title,
                    description=description,
                    category=category,
                    price_excluding_tax=price_excluding_tax,
                    price_including_tax=price_including_tax,
                    availability=availability,
                    number_of_reviews=number_of_reviews,
                    cover_image_url=cover_image_url,
                    rating=rating,
                    metadata=Metadata(
                        crawl_timestamp=datetime.now(),
                        status=str(status_code),
                        source_url=url
                    )
                )
        except Exception as exc:
            print(url, exc)
            raise