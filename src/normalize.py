import pandas as pd
from sklearn import preprocessing
import numpy as np

def compute_question_length(row):
	return row["end_time"] - row["start_time"]

def normalize_data(vals):
	return preprocessing.normalize([vals]).tolist()[0]

if __name__ == '__main__':

	#infile = pd.read_csv("extraction_result.csv", sep=";", encoding="utf-8", index_col=0)
	infile = pd.read_excel("extraction_result_acsynt.xlsx", index_col=0)
	infile = infile[infile["debit (sps)"].notna()].reset_index()

	infile["duree_phrase"] = infile.apply(lambda row: compute_question_length(row), axis=1)
	infile["mean_syll_duration_norm (ms)"] = normalize_data(np.array(infile["mean_syll_duration (ms)"]))
	infile["mean_syll_duration_last_3_syll_norm (ms)"] = normalize_data(np.array(infile["mean_syll_duration_last_3_syll (ms)"]))

	infile.to_csv("extraction_result_acsynt_norm.csv", sep=";", encoding="utf-8")

	