from fastapi import FastAPI, Request
from app.utils.predict import predict_email

app = FastAPI()

@app.post("/predict-email")
async def predict(request: Request):
    data = await request.json()
    result = predict_email(data)
    return result
