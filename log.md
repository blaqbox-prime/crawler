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
  - once Ive ensured the crawler is able to fetch pages and parse them successfully, I convert the synchronous `httpx.get` to instead use `httpx.AsyncClient` 

### Mongo DB Setup
- I had to look up what options i have for ORM / ODM, preferrably use one of those instead of a driver and writing raw queries. Unless the application grows to require complex queries that need me to write a direct query, an ODM will be more than enough for what where we are right now. So i picked Beanie among other options like MongoEngine, because its asynchronous and looks familiar to Mongoose which I have used for jS projects. 
- Beanie using Pydantic is also a plus so I just replaced the `BaseModel` parent class of `Book` with `Document` which is a subclass of `BaseModel` so it does all the same stuff but also add some features of the ODM so now book looks like `class Book(Document)`
- Added the setup in the main.py as `def lifespan():` with the `@asynccontextmanager` decorator to allow for a single instance of the async mongodb client to be created when the server starts and closes when the server stops. This way we have a single client throughout 

### logging 
I added a logger utility file to be able to log any exceptions raised while scraping and parsing the pages.  The error will be logged to a log file in the `./logs` folder

## Struggles I have faced.
- getting to know the python ecosystem has proven to be a challenge, I just didn't have the time to delve deep into a lot of things and so I am constantly researching what tools do I need to achieve a particular outcome like rate limiting or scheduling and the like. I am trying not to lean on A.I tools outside of researching and comparing libraries and getting a quick start guide and cheatsheet for something I feel i can use. I guess with a little more time I could get much more done but I did have my current full-time job sucking up much of my time. Its been really fun working on this though. Learned a whole lot about building with python. I actually found a lot of similarities with how express apps would be built in Javascript. 