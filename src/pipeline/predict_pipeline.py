import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
from sklearn.impute import SimpleImputer
from src.exception import CustomException
from src.utils import load_object


def _restore_imputer_state(transformer):
    if isinstance(transformer, SimpleImputer):
        if not hasattr(transformer, "_fill_dtype") and hasattr(transformer, "_fit_dtype"):
            transformer._fill_dtype = transformer._fit_dtype
        return

    if hasattr(transformer, "transformers_"):
        for _, fitted_transformer, _ in transformer.transformers_:
            _restore_imputer_state(fitted_transformer)

    if hasattr(transformer, "steps"):
        for _, step in transformer.steps:
            _restore_imputer_state(step)


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = os.path.join(project_root, "artifacts", "model.pkl")
            preprocessor_path = os.path.join(project_root, "artifacts", "preprocessor.pkl")
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            _restore_imputer_state(preprocessor)
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e,sys)



class CustomData:
    def __init__(  self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int):

        self.gender = gender

        self.race_ethnicity = race_ethnicity

        self.parental_level_of_education = parental_level_of_education

        self.lunch = lunch

        self.test_preparation_course = test_preparation_course

        self.reading_score = reading_score

        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)

