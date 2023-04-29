'''inspo : https://colab.research.google.com/github/neerajww/myblog/blob/master/_notebooks/2020-06-16-PRAAT_feature_extractiion.ipynb#scrollTo=m0msaLq6B86x'''

from pathlib import Path
import parselmouth
import bs4 as bs
import re
import os
import tgt
import matplotlib.pyplot as plt

DIRECTORY = "../data3/ESLO/"

# for PRAAT
sr = 16000
hop_dur = .01
num_form = 3
max_form_freq = 4500

def read_tg(tg_path):
	return parselmouth.read(tg_path).to_tgt()

def read_wav(wav_path):
	return parselmouth.Sound(wav_path)

def get_annot(label_tier, question_type: str):
	'''keep only annotated sentences'''
	return [(q.start_time, q.end_time) for q in label_tier if q.text == question_type]

def get_questions(grid, questions, all_tiers):
	''' get time stamps + question as a list of tuples '''
	
	text = []
	for question in questions:
		for tier in all_tiers:
			tier = grid.get_tier_by_name(tier)
			for annot in tier:
				if annot.start_time == question[0] and annot.end_time == question[1] and "?" in annot.text:
					text.append((annot.start_time, annot.end_time, annot.text))

	return text

def get_pitch(sound):
	return sound.to_pitch(time_step=hop_dur) # pitch track

def get_harmonicity(sound):
	return sound.to_harmonicity(time_step=hop_dur) # harmonic-to-noise ratio

def get_formants(sound):
	return sound.to_formant_burg(time_step=hop_dur, max_number_of_formants=num_form, maximum_formant=max_form_freq, pre_emphasis_from=50.0) # formants

def get_intensity(sound):
	return sound.to_intensity(minimum_pitch=75.0, time_step=hop_dur, subtract_mean=False) # intensity

def get_spectrogram(sound):
	return sound.to_spectrogram(window_length=0.04)

def get_sound_snippet(sound, start_time, end_time):
	return sound.extract_part(start_time, end_time)

def extract_features(sound, questions):

	pitch = harm = form = intensity = []
	for question in questions:
		snippet = get_sound_snippet(sound, question[0], question[1])

		pitch.append(get_pitch(snippet))
		harm.append(get_harmonicity(snippet))
		form.append(get_formants(snippet))
		intensity.append(get_intensity(snippet))

		# times = pitch.ts() # analysis window time instants

	return pitch, harm, form, intensity

def extract_questions(tg_path,wav_path):

	print(Path(tg_path).stem)

	grid = read_tg(tg_path)
	sound = read_wav(wav_path)
	label_tier = grid.get_tier_by_name("label")
	all_tiers = grid.get_tier_names()

	prepared = get_questions(grid, get_annot(label_tier, "préparé"), all_tiers)
	spontaneous = get_questions(grid, get_annot(label_tier, "spontané"), all_tiers)
	non_question = get_questions(grid, get_annot(label_tier, "non-question"), all_tiers)
	
	all_questions = prepared + spontaneous + non_question

	if len(all_questions) < 1:
		return None # skip files with no annotations

	pitch, harm, form, intensity = extract_features(sound, prepared) # extraction du pitch, harmonicité, formants, intensité pour les questions préparéesà)

def main():
	tg = Path(DIRECTORY).rglob("*.TextGrid")
	wav = Path(DIRECTORY).rglob("*.wav")
	for tg_path,wav_path in zip(tg,wav):
		extract_questions(str(tg_path),str(wav_path))

if __name__ == '__main__':
	main()
