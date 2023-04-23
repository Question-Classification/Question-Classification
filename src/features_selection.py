from pathlib import Path
import parselmouth
import bs4 as bs
import re
import os
import tgt

DIRECTORY = "../data3/ESLO/"

def read_tg(tg_path):
	return parselmouth.read(tg_path).to_tgt()

def read_wav(wav_path):
	return parselmouth.Sound(wav_path)

def get_annot(label_tier, question_type: str):
	return [(q.start_time, q.end_time) for q in label_tier if q.text == question_type]

def get_questions(grid, questions, all_tiers):
	
	text = []
	for question in questions:
		for tier in all_tiers:
			tier = grid.get_tier_by_name(tier)
			for annot in tier:
				if annot.start_time == question[0] and annot.end_time == question[1] and "?" in annot.text:
					text.append((annot.text, annot.start_time, annot.end_time))

	return text

def extract_questions(tg_path,wav_path):

	#print(Path(tg_path).stem)

	grid = read_tg(tg_path)
	sound = read_wav(wav_path)
	label_tier = grid.get_tier_by_name("label")
	all_tiers = grid.get_tier_names()

	prepared = get_annot(label_tier, "préparé")
	spontaneous = get_annot(label_tier, "spontané")
	non_question = get_annot(label_tier, "non-question")

	prepared = get_questions(grid, prepared, all_tiers)
	spontaneous = get_annot(grid, spontaneous, all_tiers)
	non_question = get_annot(grid, non_question, all_tiers)

def main():
	tg = Path(DIRECTORY).rglob("*.TextGrid")
	wav = Path(DIRECTORY).rglob("*.wav")
	for tg_path,wav_path in zip(tg,wav):
		extract_questions(str(tg_path),str(wav_path))

if __name__ == '__main__':
	main()
