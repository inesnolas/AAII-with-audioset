
from __future__ import print_function, division
import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import json
import librosa
from torchvggish.torchvggish import vggish
from torchvggish.torchvggish import vggish_params
from torchvggish.torchvggish.vggish_input import AudioFileLargerThanDefinedMax


def get_embeddings(dataset_csv, dataset_with_embeddings_csv ):
    

    url_state_dict = {'vggish':'https://github.com/harritaylor/torchvggish/releases/download/v0.1/vggish-10086976.pth',
            'pca':'https://github.com/harritaylor/torchvggish/releases/download/v0.1/vggish_pca_params-970ea276.pth'}
    # model = torch.hub.load('harritaylor/torchvggish', 'vggish')
    model = vggish.VGGish(url_state_dict)
    
    model.eval()

    # Get set of wavs to go through vggish
    # 1 -one at a time?
        # read csv file
    dataset = pd.read_csv(dataset_csv)
    dataset_with_embeddings = dataset.copy()
    dataset_with_embeddings['Embeddings'] = 'somethingTOfill'
        # get wavfilename and path   
    for i in range(len(dataset.index)):
        example = os.path.join(dataset.iloc[i].wavpath, dataset.iloc[i].wavfilename)
        print(example)
        try: 
            embeddings = model.forward(example)
        except AudioFileLargerThanDefinedMax :
            print("the file: " + example + " is larger than "+ str(vggish_params.MAX_AUDIO_LENGTH_SEC) + " sec")
            continue
        dataset_with_embeddings.loc[i, 'Embeddings'] = embeddings.detach().numpy()
        # print(embeddings)
        print(dataset_with_embeddings.iloc[i])
    # clean from dataset_with_embeddings dataframe the entries without embedding computed, before saving
    dataset_with_embeddings = dataset_with_embeddings[dataset_with_embeddings.Embeddings != 'somethingTOfill']
    dataset_with_embeddings.to_csv(dataset_with_embeddings_csv,index=False)


if __name__ == "__main__" :
    
    dataset_csv = "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/Id_classification_from_audioset_embedings/test.csv"
    dataset_with_embeddings_csv = "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/Id_classification_from_audioset_embedings/testresult.csv"
    # dataset_csv = "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/Id_classification_from_audioset_embedings/three_bird_species_dataset_with_embeddings/Three_Species_and_Id_Dataset.csv"
    # dataset_with_embeddings_csv = "/mnt/c/Users/madzi/Dropbox/QMUL/PHD/Id_classification_from_audioset_embedings/three_bird_species_dataset_with_embeddings/Three_Species_and_Id_withEmbeddings.csv"

    get_embeddings(dataset_csv, dataset_with_embeddings_csv )
