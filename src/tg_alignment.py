from pathlib import Path
import re
import os

DIRECTORY = "../data/ESLO/"

def align_one_ESLO_file(trs_path, filename):
	print(f"Created {filename}")
	os.system(f"perl trs_to_tg.pl {trs_path} > {filename}")

def main():
	pathlist = Path(DIRECTORY).rglob("*.trs")
	for trs_path in pathlist:
		stem = Path(trs_path).stem
		base_path = re.sub(stem+".trs", "", str(trs_path))
		filename = re.sub("_C", "", Path(trs_path).stem)
		align_one_ESLO_file(trs_path, base_path+filename+".TextGrid")

if __name__ == '__main__':
	main()
