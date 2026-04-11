from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import predict

app = FastAPI(
    title="Спеллчекер API",
    description="Сервер для исправления опечаток на базе MLX",
    version="1.0"
)


class Message(BaseModel):
    role: str
    content: str


class TextRequest(BaseModel):
    messages: list[Message]


class TextResponse(BaseModel):
    text: str


@app.post("/api/ai-server/predict", response_model=TextResponse)
def predict_post(request: TextRequest):
    try:
        corrected = predict.predict(request.messages)
        return TextResponse(text=corrected)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
