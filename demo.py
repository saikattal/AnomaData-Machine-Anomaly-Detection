
from anoma_data.pipeline.prediction_pipeline import AnomaData, AnomaDataClassifier
path='/Users/skt/Documents/MLOPS Projects/AnomaData-Machine-Anomaly-Detection/notebooks/test_anoma_data.csv'
anoma_data=AnomaData(path)
df=anoma_data.get_anomadata_input_data_frame()

model_predictor = AnomaDataClassifier()
value = model_predictor.predict(dataframe=df)[0]

status = None
if value == 1:
    status = "Anomaly detected"
else:
    status = "No anomaly detected"
print (status)