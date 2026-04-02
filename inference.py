from fastapi import FastAPI
from env.environment import EmailEnv

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Email AI is running 🚀"}

@app.get("/run")
def run_ai():
    env = EmailEnv()
    result = env.run_task("easy")
    return {"result": result}