from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from controllers.teas import router as TeasRouter
from controllers.comments import router as CommentRouter
from controllers.users import router as UsersRouter

app = FastAPI()

app.include_router(TeasRouter, prefix='/api')
app.include_router(CommentRouter, prefix='/api')
app.include_router(UsersRouter, prefix='/api')

@app.get('/')
def home():
  return {'message': 'Home Page'}


