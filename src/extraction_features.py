import pandas as pd 
import tgt
import parselmouth
import numpy as np
from pathlib import Path
import re
import math
import logging
import sys
from logging import INFO


logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s|%(levelname)s|%(name)s|%(module)s|%(funcName)s|%(lineno)s|%(message)s",
    datefmt="%d/%m/%Y %I:%M:%S %p",
    level=INFO,
)
localLogger = logging.getLogger("Feature extraction")
localLogger.info("Start of feature extraction")



def extract_slope_two_last_syll_mean(pitch, question, syll_tier):
	"""To extract the slope between the last two syllables with average F0 values extracted from each syllable.
	
	Parameters
    ---------
    pitch
		A pitch parselmouth object that allows to extract pitch features.
    question
        A tgt object that represents a question and contains information like time stamps and text.
    syll_tier
        A tgt object that represent a praat tier containing syllables.

    Returns
    -------
    float
        The value of the slope between the last two syllables. 			
	"""
	syll_object = syll_tier.get_annotations_between_timepoints(question.start_time, question.end_time, left_overlap=False, right_overlap=False)
	last_two_syll = []

	for i in range(len(syll_object)-1, -1, -1):
		if len(last_two_syll) == 2:
			break
		if syll_object[i].text != "_":
			last_two_syll.append(syll_object[i])
	last_two_syll.reverse()

	if len(last_two_syll) > 1 :
		last_syll_mean_value = parselmouth.praat.call(pitch, "Get mean", last_two_syll[1].start_time, last_two_syll[1].end_time , "Hertz")
		pre_last_syll_mean_value = parselmouth.praat.call(pitch, "Get mean", last_two_syll[0].start_time, last_two_syll[0].end_time, "Hertz")

		mean_slope = last_syll_mean_value - pre_last_syll_mean_value

		if math.isnan(mean_slope): 
			return np.nan
		else : 
			return round(mean_slope)



def extract_slope_two_last_syll_mid(pitch, question, syll_tier):
	"""To extract the slope between the last two syllables with F0 values taken at the middle of each syllable.
	
	Parameters
    ---------
    pitch
		A pitch parselmouth object that allows to extract pitch features.
    question
        A tgt object that represents a question and contains information like time stamps and text.
    syll_tier
        A tgt object that represent a praat tier containing syllables.

    Returns
    -------
    float
        The value of the slope between the last two syllables. 			
	"""
	syll_object = syll_tier.get_annotations_between_timepoints(question.start_time, question.end_time, left_overlap=False, right_overlap=False)
	last_two_syll = []

	for i in range(len(syll_object)-1, -1, -1):
		if len(last_two_syll) == 2:
			break
		if syll_object[i].text != "_":
			last_two_syll.append(syll_object[i])
	last_two_syll.reverse()
	
	if len(last_two_syll) > 1 :
		mid_time_last_syll = last_two_syll[1].start_time + (last_two_syll[1].end_time - last_two_syll[1].start_time) / 2
		last_syll_value = pitch.get_value_at_time(mid_time_last_syll)

		mid_time_pre_last_syll = last_two_syll[0].start_time + (last_two_syll[0].end_time - last_two_syll[0].start_time) / 2
		pre_last_syll_value = pitch.get_value_at_time(mid_time_pre_last_syll)

		slope_mid = last_syll_value - pre_last_syll_value
		
		if math.isnan(slope_mid):
			return np.nan
		else : 
			return round(slope_mid)



def extract_three_last_syllable_duration(question, syll_tier):
	"""To extract the mean duration of the three last syllables in a question.
	
	Parameters
    ---------
    question
        A tgt object that represents a question and contains information like time stamps and text.
    syll_tier
        A tgt object that represent a praat tier containing syllables.

    Returns
    -------
    float
        Mean duration (in ms) of the three last syllables in a question.			
	"""
	total_duration = 0
	syll_object = syll_tier.get_annotations_between_timepoints(question.start_time, question.end_time, left_overlap=False, right_overlap=False)
	
	for syll in syll_object[-3:] :
		if syll.text != "_" and question.text != "_":
			syll_duration = syll.end_time - syll.start_time
			total_duration += syll_duration

	mean_duration = total_duration / 3

	return mean_duration*1000



def extract_mean_syll_duration_speech_rate(question, syll_tier):
	"""To extract the mean duration of all syllables in a question and the speech rate.
	
	Parameters
    ---------
    question
        A tgt object that represents a question and contains information like time stamps and text.
    syll_tier
        A tgt object that represent a praat tier containing syllables.

    Returns
    -------
    float
        Mean duration (in ms) of all syllables in a question.
	int
		Mean speech rate on questions.
			
	"""
	total_duration = 0
	num_syll = 0
	syll_object = syll_tier.get_annotations_between_timepoints(question.start_time, question.end_time, left_overlap=False, right_overlap=False)
	
	for syll in syll_object:
		if syll.text != "_" and question.text != "_":
			num_syll+=1
			syll_duration = syll.end_time - syll.start_time
			total_duration += syll_duration
	
	mean_duration = total_duration / len(syll_object)
	
	if total_duration != 0 :
		speech_rate = num_syll / (total_duration)
	else : 
		speech_rate = 0

	return mean_duration*1000, round(speech_rate)



def extract_features_from_one_file(tgt_filename, wav_path, filename, df): 
	"""To extract features from one file.

    Parameters
    ---------
    tgt_filename
        The name of the TextGrid file (containing the path).
    wav_path
        The name of the wav file (containing the path).
    filename
        The stem of the filenames (without any path).
	df
		A pandas dataframe to store the extraction results.

    Returns
    -------
    df
        The dataframe updated with the features extracted from the processed file.
    """
	grid = parselmouth.read(tgt_filename).to_tgt()
	sound = parselmouth.Sound(wav_path)
	
	ortho_tier = grid.get_tier_by_name("ortho")
	label_tier = grid.get_tier_by_name("label")
	syll_tier = grid.get_tier_by_name("syll")

	for question in ortho_tier :
		if question.text != "_":
			start_time = question.start_time
			end_time = question.end_time
			question_text = question.text
			label = label_tier.get_annotations_between_timepoints(start_time, end_time, left_overlap=True, right_overlap=True)
			label_text = label[0].text
			sound_sample = sound.extract_part(start_time, end_time, preserve_times = True)
			pitch = sound_sample.to_pitch(time_step=0.001, pitch_ceiling=600, pitch_floor=75)
			mean_absolute_question_slope = pitch.get_mean_absolute_slope()
			mean_all_syll_duration = extract_mean_syll_duration_speech_rate(question, syll_tier)[0]
			speech_rate = extract_mean_syll_duration_speech_rate(question, syll_tier)[1]
			three_last_syll_duration = extract_three_last_syllable_duration(question, syll_tier)
			two_last_syll_mid_slope = extract_slope_two_last_syll_mid(pitch, question, syll_tier)
			two_last_syll_mean_slope = extract_slope_two_last_syll_mean(pitch, question, syll_tier)

			new_row = {'file_name': filename, 'question_label': label_text, 'start_time': start_time, 'end_time' : end_time, 'question_text' : question_text, 'mean_absolute_question_slope (Hz)' : mean_absolute_question_slope, 'mean_all_syll_duration (ms)' : mean_all_syll_duration, 'speech_rate (sps)' : speech_rate, 'three_last_syll_duration (ms)' : three_last_syll_duration, 'two_last_syll_mid_slope (Hz)' : two_last_syll_mid_slope, 'two_last_syll_mean_slope (Hz)' : two_last_syll_mean_slope}
			df = df.append(new_row, ignore_index=True)
	
	return df
	


def main():
	"""The main function is used to process all the files and make the last modifications before saving the resulting frame."""
	directory = r"clean_data_for_extraction/ESLO"
	pathlist = Path(directory).rglob("*.wav")
	df = pd.DataFrame(columns=['file_name', 'question_label', 'start_time', 'end_time', 'question_text', 'mean_absolute_question_slope (Hz)', 'mean_all_syll_duration (ms)', 'speech_rate (sps)', 'three_last_syll_duration (ms)', 'two_last_syll_mid_slope (Hz)', 'two_last_syll_mean_slope (Hz)'])

	for wav_path in pathlist:
		filename = wav_path.stem
		base_path = re.sub(filename+".wav", "", str(wav_path))
		tgt_filename = base_path+"one_tier_easy_align_"+filename+".TextGrid"

		localLogger.info("Processing %s file", filename)
		df = extract_features_from_one_file(tgt_filename, str(wav_path), filename, df)

	df['mean_all_syll_duration (ms)'] = df['mean_all_syll_duration (ms)'].replace(0, np.nan)
	df['speech_rate (sps)'] = df['speech_rate (sps)'].replace(0, np.nan)
	df['mean_all_syll_duration (ms)'] = round(df['mean_all_syll_duration (ms)'])
	df['mean_absolute_question_slope (Hz)'] = round(df['mean_absolute_question_slope (Hz)'])
	df['three_last_syll_duration (ms)'] = round(df['three_last_syll_duration (ms)'])
	df['question_text'] = df['question_text'].apply(lambda x: x + ' ?')
	# df = df.drop(['mean_absolute_question_slope (Hz)'], axis=1)

	df.to_csv("features_extraction_results.csv", sep=";", header=True, encoding="utf-8")
	df.to_excel("features_extraction_results.xlsx", header=True)

	print(df)



if __name__ == '__main__':
	main()