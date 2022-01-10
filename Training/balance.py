#from  https://github.com/Sentdex/pygta5

import numpy as np 
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

train_data = np.load('training_data.npy', allow_pickle=True) 

df = pd.DataFrame(train_data)
print(df.head())
print(Counter(df[1].apply(str)))

lefts = []
rights = []
forwards = []

shuffle(train_data)

for data in train_data:
    img = data[0]
    choice = data[1]
    #print(choice)
    if choice == [1, 1, 0]:
        lefts.append([img, choice])
    elif choice == [0, 1, 1]:
        rights.append([img, choice])
    elif choice == [0, 1, 0]:
        forwards.append([img, choice])
    else:
        pass#print('no matches')


forwards = forwards[:len(lefts)][:len(rights)]
rights = rights[:len(forwards)]
lefts = lefts[:len(forwards)]
print(len(forwards), len(rights), len(lefts))
final_data = forwards + lefts + rights

shuffle(final_data)
print(len(final_data))
np.save('balanced.npy', final_data)
