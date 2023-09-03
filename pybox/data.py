import pandas as pd
import matplotlib.pyplot as plt


class DataAnalyzer:
    def __init__(self, dataframe: pd.DataFrame):
        """
        Creates a DataAnalyzer object.

        Args:
            dataframe (pd.DataFrame): Pandas DataFrame to analyze.
        """

        self.df = dataframe

    def start(self):
        for column in self.df.columns:
            plt.figure(figsize=(8, 6))
            plt.title(f'Plot for {column}')

            if self.df[column].dtype in ['int64', 'float64']:
                plt.hist(self.df[column], bins=20)
                plt.xlabel(column)
                plt.ylabel('Frequency')
            else:
                value_counts = self.df[column].value_counts()
                value_counts.plot(kind='bar')
                plt.xlabel(column)
                plt.ylabel('Count')

            plt.show()
