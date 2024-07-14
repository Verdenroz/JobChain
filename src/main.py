from dotenv import load_dotenv
from fastapi import FastAPI
from mangum import Mangum

from src.routes import jobs_router

# Load environment variables
load_dotenv()
app = FastAPI()

app.include_router(jobs_router)

handler = Mangum(app)
