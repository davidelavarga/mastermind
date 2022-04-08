import os
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from mastermind.bootstrap import configure_inject

tags_metadata = [
    {
        "name": "",
        "description": "",
    }
]
app = FastAPI(root_path=os.getenv("ROOT_PATH", ""), openapi_tags=tags_metadata)


@app.on_event("startup")
async def startup_event():
    configure_inject()


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content={
            "status": f"{HTTPStatus.INTERNAL_SERVER_ERROR.name}",
            "ErrorMessage": f"{exc}",
        },
    )
