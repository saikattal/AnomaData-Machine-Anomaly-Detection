from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run
import pandas as pd

from typing import Optional

from anoma_data.constants import APP_HOST, APP_PORT
from anoma_data.pipeline.prediction_pipeline import AnomaData, AnomaDataClassifier
from anoma_data.pipeline.training_pipeline import TrainPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index(request: Request):

    return templates.TemplateResponse(
            "anomadata.html",{"request": request, "context": "Rendering"})


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()

        train_pipeline.run_pipeline()

        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/")
async def predictRouteClient(request: Request):
    try:
        request_data = await request.json()
        if request_data is not None:
            path = request_data['filepath']
           
            anoma_data=AnomaData(path)
            df=anoma_data.get_anomadata_input_data_frame()

            model_predictor = AnomaDataClassifier()
            value = model_predictor.predict(dataframe=df)[0]

            status = None
            if value == 1:
                status = "Anomaly detected"
            else:
                status = "No anomaly detected"

        return templates.TemplateResponse(
            "anomadata.html",
            {"request": request, "context": status},
        )
    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
