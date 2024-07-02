import os
from pathlib import Path

project_name = "anoma_data"

list_of_files = [
    f'{project_name}/__init__.py',
    f'{project_name}/components/__init__.py',
    f'{project_name}/components/data_ingestion.py',
    f'{project_name}/components/data_validation.py',
    f'{project_name}/components/data_transformation.py',
    f'{project_name}/components/model_trainer.py',
    f'{project_name}/components/model_evaluation.py',
    f'{project_name}/components/model_pusher.py',
    f'{project_name}/configuration/__init__.py',
    f'{project_name}/constants/__init__.py',
    f'{project_name}/entity/__init__.py',
    f'{project_name}/entity/config_entity.py',
    f'{project_name}/entity/artifact_entity.py',
    f'{project_name}/exception/__init__.py',
    f'{project_name}/logger/__init__.py',
    f'{project_name}/logger/logger.py',
    f'{project_name}/pipeline/__init__.py',
    f'{project_name}/pipeline/training_pipeline.py',
    f'{project_name}/pipeline/prediction_pipeline.py',
    f'{project_name}/utils/__init__.py',
    f'{project_name}/utils/main_utils.py',
    'app.py',
    'requirements.txt',
    'Dockerfile',
    '.dockerignore',
    'demo.py',
    'setup.py',
    'config/model.yaml',
    'config/schema.yaml'

]

for  file_path in list_of_files:
    file_path = Path(file_path)
    filedir, filename = os.path.split(file_path)
    if filedir!= '':
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(file_path)) or (file_path.is_dir()):
        with open(file_path, 'w') as f:
            if file_path.name.endswith('.py'):
                pass
    else:
            print(f"File is already present or a directory at: {file_path}")




        