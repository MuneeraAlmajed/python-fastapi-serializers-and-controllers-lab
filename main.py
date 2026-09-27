from fastapi import FastAPI
from controllers.teas import router as TeasRouter
from controllers.comments import router as CommentRouter

app = FastAPI()

app.include_router(TeasRouter, prefix='/api')
app.include_router(CommentRouter, prefix='/api')

@app.get('/')
def home():
  return {'message': 'Home Page'}


