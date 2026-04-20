from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, List
import uvicorn

from razomy.run.run_function_instant import run_function_instant

app = FastAPI(
    title="Dynamic Function Runner API",
    version="1.0"
)


# Request model
class FunctionRequest(BaseModel):
    package_name: str = Field()
    function_name: str = Field()
    args: List[Any] = Field()


# Response model
class FunctionResponse(BaseModel):
    result: Any
    status: str


def call_dynamic_function(package_name: str, function_name: str, args: list):
    try:
        result = run_function_instant(package_name, function_name, args)
        return result
    except ImportError as e:
        print(e)
        raise HTTPException(status_code=404, detail=f"Package '{package_name}' not found")
    except AttributeError as e:
        print(e)
        raise HTTPException(status_code=404, detail=f"Function '{function_name}' not found in '{package_name}'")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")


@app.post("/api/run", response_model=FunctionResponse)
def run_code(request: FunctionRequest):
    ALLOWED_PACKAGES = [
        "razomy.string_case",
        "razomy.ai_hugging_face",
        "razomy.ai_hugging_face.chat.tool.predict",
        "razomy.ai_hugging_face.chat.logic.predict",
        "razomy.translate_ai"
    ]

    if request.package_name not in ALLOWED_PACKAGES:
        raise HTTPException(status_code=403, detail="Package not allowed")

    try:
        result = call_dynamic_function(
            request.package_name,
            request.function_name,
            request.args,
        )
        return FunctionResponse(result=result, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
