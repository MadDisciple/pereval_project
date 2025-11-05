import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import models, schemas, services, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_400_BAD_REQUEST,
        content={"status": 400, "message": f"Ошибка валидации: {exc.errors()}", "id": None}
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": 500, "message": f"Ошибка БД: {str(exc)}", "id": None}
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": 500, "message": f"Внутренняя ошибка сервера: {str(exc)}", "id": None}
    )



@app.post("/submitData", response_model=schemas.PerevalResponseSchema)
def create_pereval(pereval_input: schemas.PerevalInputSchema, db: Session = Depends(database.get_db)):
    try:
        new_id = services.submit_data(db=db, data=pereval_input)

        return {"status": 200, "message": "Отправлено успешно", "id": new_id}

    except Exception as e:
        raise e


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)