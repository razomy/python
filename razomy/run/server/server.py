from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, List
import uvicorn
import importlib
import threading

from razomy.run.run_function_instant import run_function_instant

# Create a global lock for dynamic imports
import_lock = threading.Lock()
app = FastAPI(
    title="Dynamic Function Runner API",
    version="1.0"
)
ALLOWED_PACKAGES = [
    "razomy.string_case",
    "razomy.ai_hugging_face",
    "razomy.ai_hugging_face.chat.tool.predict",
    "razomy.ai_hugging_face.chat.logic.predict",
    "razomy.translate_ai"
]
for pkg in ALLOWED_PACKAGES:
    try:
        importlib.import_module(pkg)
    except Exception as e:
        print(f"Warning: Could not pre-import {pkg}: {e}")

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
async def run_code(request: FunctionRequest):
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
