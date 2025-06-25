from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "YT-DLP API is working!"}
