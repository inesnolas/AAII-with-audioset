import numpy as np
import pandas as pd 
import csv
import os
import json



def create_dataset_csv(list_csv_specie, master_csv, wavs_folders_species, identities_per_species_dict):

    classes_dict = {}

    with open(master_csv, 'w') as master_csv:
        writer = csv.writer(master_csv)
        writer.writerow(["wavfilename", "wavpath", "species", "individual_id"])

        for sp, list_csvs in list_csv_specie.items():
            ids = []
            species = sp
            wavs_folder = wavs_folders_species[sp]         
            for ff in list_csvs:
                    
                with open(ff, 'r') as csv1:
                    reader1 =csv.reader(csv1)
                    print(ff)
                    for row in reader1:
                        #get id from wav filename
                        if row[0] == 'wavfilename':
                            continue
                        else:
                            ident = row[0].split('_')[2]
                    #         print(ident)
                            ids.append(ident)
                            writer.writerow([row[0], wavs_folder, species, ident])
                    del(reader1)
                    csv1.close()
                
                identities = set(ids)
                if species not in classes_dict.keys():
                    classes_dict[species] = []
                for i in identities:
                    if i not in classes_dict[species]:
                        classes_dict[species].append(i)
              

    print(classes_dict)
    with open(identities_per_species_dict, 'w') as fp:
        json.dump(classes_dict, fp)

    return



if __name__ == "__main__":
    list_csv_specie = {"chiffchaffs" :["/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/csv/csv/chiffchaff-withinyear-fg-trn.csv",
                                   "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/csv/csv/chiffchaff-withinyear-fg-tst.csv",
                                   "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/csv/csv/chiffchaff-acrossyear-fg-tst.csv",
                                   "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/csv/csv/chiffchaff-acrossyear-fg-trn.csv"],
                   "littleowls" : ["/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/csv/csv/littleowl-acrossyear-fg-trn.csv", 
                                  "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/csv/csv/littleowl-acrossyear-fg-tst.csv"], 
                   "pipits" : ["/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/csv/csv/pipit-withinyear-fg-tst.csv", 
                             "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/csv/csv/pipit-withinyear-fg-trn.csv", ]
                  }

    master_csv = "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/Id_classification_from_audioset_embedings/Three_Species_and_Id_Dataset.csv"


    wavs_folders_species = {"chiffchaffs":"/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/wavs/chiffchaff-fg",
                       "littleowls": "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/wavs/littleowls-fg", 
                       "pipits": "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/local datasets/data_dans_paper/wavs/pipits-fg"}

    identities_per_species_dict = '/mnt/c/Users/madzi/Dropbox/QMUL/PHD/Id_classification_from_audioset_embedings/classes_dict.json'

    create_dataset_csv(list_csv_specie, master_csv, wavs_folders_species, identities_per_species_dict)
