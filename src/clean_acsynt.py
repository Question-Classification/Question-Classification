import regex as re
from pathlib import Path
import parselmouth
import bs4 as bs
import os
import tgt

def get_label(text: str):
	if "?" in text:
		return "question"
	else:
		return ""
	
def add_label_tier(trs_path, filename):
	grid = parselmouth.read(filename).to_tgt()
	source = open(trs_path, encoding="utf-8").read()
	soup = bs.BeautifulSoup(source, "xml")
	tiers = len(grid.get_tier_names())
	tier2insert = tgt.IntervalTier(grid.start_time, grid.end_time, name='label')
	grid.insert_tier(tier2insert, tiers+1)
	interval_tier = grid.get_tier_by_name("label")
	all_turns = soup.findAll("Turn")
	for i in range(len(all_turns)):
		text = all_turns[i].getText()
		start_time = all_turns[i].attrs["startTime"]
		end_time = all_turns[i].attrs["endTime"]
		interval_labels = tgt.core.Interval(
			float(start_time), float(end_time), get_label(text)
		)
		interval_tier.add_interval(interval_labels)
	export = tgt.io.export_to_long_textgrid(grid)
	with open(filename, "w", encoding="utf-8") as out:
		out.write(export)
                
def main():
    directory = "test_acsynt_clean/"
    pathlist = Path(directory).rglob("*.trs")
    for trs_path in pathlist:
	    print(trs_path)
	    stem = Path(trs_path).stem
	    print("stem : ", stem)
	    base_path = re.sub(stem+".trs", "", str(trs_path))
	    print("base path : ", base_path)
	    filename = re.sub("_C", "", Path(trs_path).stem)
	    add_label_tier(trs_path, base_path+filename+".TextGrid")

        

if __name__ == '__main__':
    main()