## The Process:
### Initial Setup
- I started by setup up the project with a virtual environment and installing some dependencies I figure will be necessary as per the brief document:
  - FastAPI
  - Pydantic
  - Uvicorn 
- I setup a main.py to hold the instance of the FastAPI app and some placeholder endpoints.

### The Model:
- After reading the brief document we start with some small things, my reach with pythons ecosystem has gaps so I start with a little research of pydantic and how it works, just the minimum to achieve the desired outcome. The code will grow as the solution is built and refined. With that we create the `Book` Model with some data types and simple validations for a solid start. 

### The Crawler
- We start with creating a `Crawler` class with the base_url as a property. We will 1st create a crawl method that will synchronously fetch the 1st page of the website, get all the links to the individual books on that page, then go to each link sequentially to extract the data from each page and creating a list of Books that fit our `Book` Model which will be validated automatically because of pydantic.
- Once this workflow is successful We then refactor by breaking down the crawl method into smaller methods. 
  - `scrape_book` to isolate the logic of scraping a single book
  - For pagination I move the logic for fetching a single page into its own method which will take a page number as an input. We will also handle error for fetching a page number higher than the actual available pages
  - 