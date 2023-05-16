# fastapi-limit-example
FastAPI Limit Example




## Requirements:
- python 3.11
- install dependencies using `pip install -r requirements.txt`
- Copy `.env.sample` and rename it to `.env`. Then fill the variables
- Create MongoDb database with name `DorsaDb`
- run command `python -m main` in the root folder.
- redis server. for development you can run docker command:
    `docker run -p 6379:6379 --name redis_service -d redis`


## Run
You can run this project in two ways:
    1. Run in development:
        Just run file `main_dev.py` in your IDE to have debugging options.

    2. Run in production:
        Execute this command in this directory: `python uvicorn main:app`

