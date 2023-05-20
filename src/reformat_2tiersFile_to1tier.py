import regex as re
from pathlib import Path
import parselmouth
import bs4 as bs
import os
import tgt

def main():
    filename = "reformat_one_tier/deux_tiers/ESLO1_INTPERS_420/ESLO1_INTPERS_420.TextGrid"
    grid = parselmouth.read(filename).to_tgt()
    # ajout d'une nouvelle tire ortho
    tiers_len = len(grid.get_tier_names())
    tiers_names = grid.get_tier_names()
    del(tiers_names[-1])
    tier2insert = tgt.IntervalTier(grid.start_time, grid.end_time, name='ortho')
    grid.insert_tier(tier2insert, tiers_len-1)
    print(tiers_names)

    ortho_tier = grid.get_tier_by_name("ortho")
    label_tier = grid.get_tier_by_name("label")

    # names = ['407PERS', '407PERSFIE', '407PERSFEM', 'JSM', 'HM']
    tier1 = grid.get_tier_by_name(tiers_names[0])
    tier2 = grid.get_tier_by_name(tiers_names[1])

    question_list = []


    # parcours de la tier label pour trouver les questions
    for elt in label_tier :
        if elt.text != "question":
            for elt1 in tier1:
                if elt.start_time == elt1.start_time and elt.end_time == elt1.end_time and "?" in elt1.text :
                                    start_time = elt.start_time
                                    end_time = elt.end_time
                                    label = elt.text
                                    label1 = elt1.text
                                    res = [start_time, end_time, label1]
                                    question_list.append(res)
            for elt2 in tier2 :
                if elt.start_time == elt2.start_time and elt.end_time == elt2.end_time and "?" in elt2.text :
                                start_time = elt.start_time
                                end_time = elt.end_time
                                label = elt.text
                                label2 = elt2.text
                                res = [start_time, end_time, label2]
                                question_list.append(res)
            
    for i in range(len(question_list)):
        text = question_list[i][2]
        start_time = question_list[i][0]
        end_time = question_list[i][1]
        interval_labels = tgt.core.Interval(
			float(start_time), float(end_time), text
		)
        ortho_tier.add_interval(interval_labels)
    
    label_tier.delete_annotations_with_text(pattern='question', n=0, regex=False)
    grid.delete_tiers(tier_names= tiers_names, complement = False)
    export = tgt.io.export_to_long_textgrid(grid)
    
    with open("reformat_one_tier/deux_tiers/ESLO1_INTPERS_420/one_tier_ESLO1_INTPERS_420.TextGrid", "w", encoding="utf-8") as out:
        out.write(export)                
                            

if __name__ == '__main__':
    main()