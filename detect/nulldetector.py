import pandas as pd
from .detector import Detector

class NullDetector(Detector):
    def __init__(self, name='NullDetector'):
        super(NullDetector, self).__init__(name)

    def setup(self, dataset, env):
        self.ds = dataset
        self.env = env
        self.df = self.ds.get_raw_data()

    def detect_noisy_cells(self):
        """
        detech_noisy_cells returns a pandas.DataFrame containing all cells with
        NULL values.

        :return: pandas.DataFrame with columns:
            _tid_: entity ID
            attribute: attribute with NULL value for this entity
        """
        attributes = self.ds.get_attributes()
        errors = []
        for attr in attributes:
            # self.df i.e. raw_data has all NULL values converted to '_nan_'
            tmp_df = self.df[self.df[attr] == '_nan_']['_tid_'].to_frame()
            tmp_df.insert(1, "attribute", attr)
            errors.append(tmp_df)
        errors_df = pd.concat(errors, ignore_index=True)
        return errors_df

