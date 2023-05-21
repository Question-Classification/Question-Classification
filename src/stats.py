import pandas as pd
import re

ROOT_DATA_DIR = "../features/after_norm/"

def compute_stats(df_type):
	return [(col, round(df_type[col].mean(), 3)) for col in df_type.loc[:,"mean_syll_duration (ms)":]]

if __name__ == '__main__':

	df = pd.read_csv("../all_questions_norm.csv", sep=";")

	prepared = df[df['question_label'] == "préparé"]
	spontaneous = df[df['question_label'] == "spontané"]
	non_question = df[df['question_label'] == "non-question"]

	print(compute_stats(non_question)) # prints means for each feature of type of question

	annotated = pd.read_csv(ROOT_DATA_DIR+"all_questions_norm.csv", sep=";", encoding="utf-8", index_col=0)

	print("Nombre total de questions annotées :", len(df))
	print("Nombre de questions préparées :", len(prepared))
	print("Nombre de questions spontantées :", len(spontaneous))
	print("Nombre de non questions :", len(non_question))
	print(f"Pourcentage du corpus original annoté : {round((len(annotated)/len(df))*100)}%")