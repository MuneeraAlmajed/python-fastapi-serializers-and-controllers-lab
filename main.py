from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.teas import router as TeasRouter
from controllers.comments import router as CommentRouter
from controllers.users import router as UsersRouter

app = FastAPI()

origins = [
  'http://localhost:5173',
  'http://127.0.0.1:5173'
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_methods=['*'],
  allow_headers=['*'],
)
@app.get("/health")
def health_check():
    return {"ok": True}
  
app.include_router(TeasRouter, prefix='/api')
app.include_router(CommentRouter, prefix='/api')
app.include_router(UsersRouter, prefix='/api')

@app.get('/')
def home():
  return {'message': 'Home Page'}


