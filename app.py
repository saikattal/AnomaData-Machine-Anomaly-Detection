from fastapi import FastAPI, Request,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse
from uvicorn import run as app_run
import pandas as pd
import io
from typing import Optional

from anoma_data.constants import APP_HOST, APP_PORT
from anoma_data.pipeline.prediction_pipeline import AnomaData, AnomaDataClassifier
from anoma_data.pipeline.training_pipeline import TrainPipeline
from anoma_data.logger import logging

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

        return JSONResponse(content={"message": "Training successful !!"})

    except Exception as e:
        return JSONResponse(content={"error": f"Error Occurred! {e}"}, status_code=500)


@app.post("/predict", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    try:
        contents = await file.read()
        
        # Process the uploaded CSV file
        anoma_data = AnomaData()
        df = anoma_data.get_anomadata_input_data_frame(contents=io.StringIO(contents.decode('utf-8')))
        
        # Perform prediction
        model_predictor = AnomaDataClassifier()
        value = model_predictor.predict(dataframe=df)[0]
        
        # Determine prediction status
        status = "Anomaly detected" if value == 1 else "No anomaly detected"
        
        # Log prediction result
        logging.info(f"Prediction status: {status}")
        
        # Render template with prediction result
        #return templates.TemplateResponse("anomadata.html", {"request": request, "context": status})
        return JSONResponse(content={"status": status})

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return JSONResponse(content={"error": f"Error Occurred! {e}"}, status_code=500)




if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)

