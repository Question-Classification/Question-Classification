import pandas as pd 
import tgt
import parselmouth
import numpy as np
from pathlib import Path, PurePath
import re
from tqdm import tqdm
import os

WM_DIR = "../acsynt_webmaus_files/"
EA_DIR = "../after_easy_align_files/"
NEW_DIR = "../ea_wm_acsynt_merged_files/"

def write_to_tg(tier, interval_tier):

	for x in tier:
		interval = tgt.core.Interval(
			float(x.start_time), float(x.end_time), x.text
		)

		interval_tier.add_interval(interval)

def get_both_tg(wm_filename, ea_filename, wav_path):

	wm_tg = parselmouth.read(wm_filename).to_tgt()
	ea_tg = parselmouth.read(ea_filename).to_tgt()
	sound = parselmouth.Sound(wav_path)

	wm_to_keep = wm_tg.get_tier_by_name("MAU")
	ea_ortho = ea_tg.get_tier_by_name("orthographe")
	ea_label = ea_tg.get_tier_by_name("label")

	textgrid = tgt.core.TextGrid()

	interval_tier_syll = tgt.core.IntervalTier(name="syll", start_time=sound.xmin, end_time=sound.xmax)
	interval_tier_ortho = tgt.core.IntervalTier(name="ortho", start_time=sound.xmin, end_time=sound.xmax)
	interval_tier_labels = tgt.core.IntervalTier(name="label", start_time=sound.xmin, end_time=sound.xmax)

	write_to_tg(ea_label, interval_tier_labels)
	write_to_tg(ea_ortho, interval_tier_ortho)
	write_to_tg(wm_to_keep, interval_tier_syll)

	textgrid.add_tier(interval_tier_syll)
	textgrid.add_tier(interval_tier_ortho)
	textgrid.add_tier(interval_tier_labels)

	export = tgt.io.export_to_long_textgrid(textgrid)

	outfile = re.sub("../acsynt_webmaus_files/", NEW_DIR, wm_filename)

	print(outfile)
	with open(outfile, "w", encoding="utf-8") as out:
		out.write(export)

def modify_file_name(file):
	return os.system(f"mv -f {file}.TEXTGRID {file}.TextGrid")

def main():

	files_to_rename = [re.sub(r"\.TEXTGRID", "", str(path)) for path in Path(EA_DIR).rglob("*.TEXTGRID")]
	for file in files_to_rename:
		print(f"modified name of {file}")
		modify_file_name(file)
	
	wm_files = [re.sub(r"\.TextGrid", "", str(path)) for path in Path(WM_DIR).rglob("*.TextGrid")]
	ea_files = [re.sub(r"\.TextGrid", "", str(path)) for path in Path(EA_DIR).rglob("*.TextGrid")]
	cleaned_ea_files = [PurePath(path).name for path in Path(EA_DIR).rglob("*.TextGrid")]
	cleaned_wm_files = [re.sub(r"\.TextGrid", "", str(path)) for path in Path(WM_DIR).rglob("*.TextGrid") if PurePath(path).name in cleaned_ea_files]

	for wm_file,ea_file in zip(cleaned_wm_files, ea_files):
		get_both_tg(f"{wm_file}.TextGrid", f"{ea_file}.TextGrid", f"{ea_file}.wav")

if __name__ == '__main__':
	main()