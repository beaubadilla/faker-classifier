from typing import Dict
import pkg_resources
import joblib
import json
from sklearn.model_selection import GridSearchCV


def save_model(
    model,
    file_name: str,
    dataset,
    hyperparam_tuning: Dict,
    test_score: float,
    description: str = None,
):
    # def save_model():
    # get best score
    train_score = model.best_score_

    # get best params found
    params = model.best_params_

    # get versions of packages and Python
    track_package_versions = [
        "pandas",
        "numpy",
        "scikit-learn",
        "seaborn",
        "sklearn",
        "tensorflow",
        "xgboost",
    ]
    versions = {
        package: pkg_resources.get_distribution(package).version
        for package in track_package_versions
    }

    # get dataset_shape
    dataset_shape = dataset.shape

    # get columns
    columns = list(dataset.columns)

    # get model type
    if isinstance(model, GridSearchCV):
        model_type = model.estimator["model"]
        model_type = str(type(model_type)).split(".")[-1][:-2]
    else:
        model_type = str(type(model)).split(".")[-1][:-2]

    new_model = {
        "scores": {
            "train_score": train_score,
            "test_score": test_score,
        },
        "params": params,
        "columns": columns,
        "dataset_meta_data": {"shape": dataset_shape},
        "hyperparam_tuning": hyperparam_tuning,
        "file_name": file_name,
        "type": model_type,
        "versions": versions,
    }
    if description:
        new_model["description"] = description

    with open("models.json", "r") as json_file:
        data = json.load(json_file)
    # Check if file exists
    for m in data["models"]:
        if file_name == m["file_name"]:
            raise ValueError("Duplicate files will be created")

    data["models"].append(new_model)
    print(f"data after append={data}")
    with open("models.json", "w") as json_file:
        json.dump(data, json_file, indent=2)

    # Serialize model to filename
    file_name = f".\\models\\{file_name}"
    joblib.dump(model, file_name)
