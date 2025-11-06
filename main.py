import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
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

@app.get("/submitData/{id}", response_model=schemas.PerevalOutputSchema)
def get_pereval_by_id(id: int, db: Session = Depends(database.get_db)):
    pereval = services.get_pass_by_id(db, id)
    if not pereval:
        raise HTTPException(status_code=404, detail=f"Перевал с id={id} не найден")
    return pereval

@app.get("/submitData/", response_model=List[schemas.PerevalOutputSchema])
def get_perevals_by_user_email(user__email: str, db: Session = Depends(database.get_db)):
    passes = services.get_passes_by_email(db, user__email)
    return passes

@app.patch("/submitData/{id}", response_model=schemas.UpdateResponseSchema)
def update_pereval_by_id(id: int, pereval_update: schemas.PerevalUpdateSchema, db: Session = Depends(database.get_db)):
    state, message = services.update_pass_by_id(db, id, pereval_update)

    if state == 0 and "не найден" in message:
         return JSONResponse(
            status_code=404,
            content={"state": 0, "message": message}
        )
    if state == 0 and "Нельзя редактировать" in message:
         return JSONResponse(
            status_code=403,
            content={"state": 0, "message": message}
        )
    if state == 0:
         return JSONResponse(
            status_code=500,
            content={"state": 0, "message": message}
        )

    return {"state": state, "message": message}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)