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

### API Refactor
- I decided to move the api portion into its own `api/` folder where I have also split the routes from the main file. Sort of like having their own individual controllers or "routers" as you would in SpringBoot or dotnet. I am trying to fit my usual means with dotnet or spring to fastAPI, its similar but the specifics are quite a learning curve so Im using quite a bit of docs and AI for clarifying some things and translating common patterns
- I have also implemented the filtering and sorting on the endpoint for fetching all books. 
- Getting the sort to work was a bit of a hassle, I definitely had to look up what exactly I was trying to do. I ended up with trying to get the sort_field by extracting directly if its present or converting the book object to a dictionary with `model_dump()` and extracting from there. 
```python
if sort_by:
        reverse = True if order == "desc" else False
        sort_field = SORT_FIELD_MAP[sort_by]
        try:
            books = sorted(books, key=lambda b: getattr(b, sort_field) if hasattr(b, sort_field) else (b.model_dump().get(sort_field) if hasattr(b, "model_dump") else None), reverse=reverse)
        except Exception:
            # fallback: return unsorted if something unexpected happens
            pass
``` 
### Rate Limitting
- Using slowAPI i managed to add a rate limiter which is so far pretty straight forward given the docs. Currently I am rate limiting on the IP of the incoming request which is the default. Once I have implemented the API KEYS i will then swap out the `rate_limit_key` to use the API Keys for that instead. I have also isolated the rate limiter setup in the `api/rate_limiter.py` file for better organization.
- While doing this I've thought of putting some of the "server settings" such as the default rate limiter and the database connection details in a `.env` file. That should make the important stuff easy to change when changing environments or changing some global setting like default_rate_limits. I have found that I can make pydantic model that will load all these settings and I can just access it everywhere like I would any other class instance. Very handy. Now the application only reads the environment variables in one place. 

## Struggles I have faced.
- getting to know the python ecosystem has proven to be a challenge, I just didn't have the time to delve deep into a lot of things and so I am constantly researching what tools do I need to achieve a particular outcome like rate limiting or scheduling and the like. I am trying not to lean on A.I tools outside of researching and comparing libraries and getting a quick start guide and cheatsheet for something I feel i can use. I guess with a little more time I could get much more done but I did have my current full-time job sucking up much of my time. Its been really fun working on this though. Learned a whole lot about building with python. I actually found a lot of similarities with how express apps would be built in Javascript. 