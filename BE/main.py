import uvicorn
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI , WebSocket , WebSocketDisconnect
from src.routes.answer_route import AnswerRoute
from src.routes.auth_route import AuthRoute
from src.routes.appointments_route import Appointment_route
from src.routes.question_route import QuestionRoute
from src.routes.user_route import UserRoute
from src.schemas.answer_schema import AnswerBase
from src.schemas.question_schema import QuestionBase
from src.utils.database import engine
from src.schemas.database_schema import Base
from src.schemas.appointments_schema import AppointmentBase


Base.metadata.create_all(bind=engine)
AppointmentBase.metadata.create_all(bind=engine)
QuestionBase.metadata.create_all(bind=engine)
AnswerBase.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(AuthRoute)
app.include_router(Appointment_route)
app.include_router(UserRoute)
app.include_router(QuestionRoute)
app.include_router(AnswerRoute)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8100)

#uvicorn main:app --reload --port 8100