import pandas as pd 
import tgt
import parselmouth
import numpy as np
from pathlib import Path
import re

def extract_3_last_syllable_duration_slope(question, syll_tier):
	total_duree = 0
	syll_object = syll_tier.get_annotations_between_timepoints(question.start_time, question.end_time, left_overlap=False, right_overlap=False)
	
	for syll in syll_object[-3:] :
		if syll.text != "_" and question.text != "_":
			syll_duration = syll.end_time - syll.start_time
			total_duree += syll_duration
			#print(syll.text, syll_duration, total_duree)

	#print("******** fin question")
	duree_moyenne = total_duree / 3

	return duree_moyenne*1000

def extract_mean_syll_duration_debit(question, syll_tier):

	total_duree = 0
	nb_syll = 0
	syll_object = syll_tier.get_annotations_between_timepoints(question.start_time, question.end_time, left_overlap=False, right_overlap=False)

	for syll in syll_object:
		if syll.text != "_" and question.text != "_":
			nb_syll+=1
			syll_duration = syll.end_time - syll.start_time
			total_duree += syll_duration

	duree_moyenne = total_duree / len(syll_object)

	if total_duree != 0 :
		debit = nb_syll / (total_duree)
	else : 
		debit = 0

	return duree_moyenne*1000, debit


def main():
	directory = "after_easy_align_files/"
	pathlist = Path(directory).rglob("*.wav")
	df = pd.DataFrame(columns=['file_name', 'question_label', 'start_time', 'end_time', 'question', 'absolute_slope_question', 'mean_syll_duration (ms)', 'debit (sps)', 'mean_syll_duration_last_3_syll (ms)'])

	for wav_path in pathlist:
		filename = wav_path.stem
		base_path = re.sub(filename+".wav", "", str(wav_path))
		tgt_filename = base_path+filename+".TextGrid"

		# print(wav_path, type(tgt_filename))
		# print(tgt_filename, type(tgt_filename))
		print(filename)
		df = pd.concat([df, extract_from_one_file(tgt_filename, str(wav_path), filename, df)])

	#df = df.drop(['start_time', 'end_time'], axis=1)
	df['mean_syll_duration (ms)'] = df['mean_syll_duration (ms)'].replace(0, np.nan)
	df['debit (sps)'] = df['debit (sps)'].replace(0, np.nan)
	df['debit (sps)'] = round(df['debit (sps)'], 3)
	df['mean_syll_duration (ms)'] = round(df['mean_syll_duration (ms)'], 3)
	df['absolute_slope_question'] = round(df['absolute_slope_question'])
	df['mean_syll_duration_last_3_syll (ms)'] = round(df['mean_syll_duration_last_3_syll (ms)'], 3)
	#df['question'] = df['question'].apply(lambda x: x)
	df = df[df['question_label'] != "poubelle"]

	df.to_csv("extraction_result.csv", sep=";", header=True, encoding="utf-8")
	df.to_excel("extraction_result.xlsx", header=True)

def extract_from_one_file(tgt_filename, wav_path, filename, df): 
	df = pd.DataFrame()
	grid = parselmouth.read(tgt_filename).to_tgt()
	sound = parselmouth.Sound(wav_path)
	
	ortho_tier = grid.get_tier_by_name("orthographe")
	label_tier = grid.get_tier_by_name("label")
	syll_tier = grid.get_tier_by_name("syll")

	for question in ortho_tier :
		if question.text != "_":
			start_time = question.start_time
			end_time = question.end_time
			question_text = question.text
			label = label_tier.get_annotations_between_timepoints(start_time, end_time, left_overlap=True, right_overlap=True)

			if len(label) > 0:
				label_text = label[0].text
			else:
				label_text = "poubelle"

			sound_sample = sound.extract_part(start_time, end_time)
			pitch = sound_sample.to_pitch(time_step= .01)
			mean_absolute_slope = pitch.get_mean_absolute_slope()
			mean_syll_duration = extract_mean_syll_duration_debit(question, syll_tier)[0]
			debit = extract_mean_syll_duration_debit(question, syll_tier)[1]
			duree_trois_dernieres_syllabes = extract_3_last_syllable_duration_slope(question, syll_tier)
			# print(question_text, mean_syll_duration)
			new_row = {'file_name': filename, 'question_label': label_text, 'start_time': start_time, 'end_time' : end_time, 'question' : question_text, 'absolute_slope_question' : mean_absolute_slope, 'mean_syll_duration (ms)' : mean_syll_duration, 'debit (sps)' : debit, 'mean_syll_duration_last_3_syll (ms)' : duree_trois_dernieres_syllabes}
			df = df.append(new_row, ignore_index=True)
	
	return df
	
if __name__ == '__main__':
	main()