import xml.etree.cElementTree as ET
from convert import convertparam
import pandas as pd
import random
import copy

def model(df, n_notes=200, param=6):
    gen_notes = []

    prev3 = df.iloc[0].values[0]
    prev2 = df.iloc[1].values[0]
    prev = df.iloc[2].values[0]
    gen_notes.append(prev3)
    gen_notes.append(prev2)
    gen_notes.append(prev)
    for i in range(n_notes):
        selection = df[df['prev']==-1]
        num = random.randint(1, 6)
        if num in convertparam(param)[0]:
            if selection.empty:
                selection = df[(df['prev']==prev)&(df['prev2']==prev2)&(df['prev3']==prev3)]
            if selection.empty:
                selection = df[(df['prev']==prev)&(df['prev2']==prev2)]
            if selection.empty:
                selection = df[df['prev']==prev]
        elif num in convertparam(param)[1]:
            if selection.empty:
                selection = df[(df['prev']==prev)&(df['prev2']==prev2)]
            if selection.empty:
                selection = df[df['prev']==prev]
        else:
            if selection.empty:
                selection = df[df['prev']==prev]

        if selection.empty:
            prev3 = df.iloc[0].values[0]
            prev2 = df.iloc[1].values[0]
            prev = df.iloc[2].values[0]
        else:
            prev3 = prev2
            prev2 = prev
            prev = selection.sample(1)['label'].values[0]
        gen_notes.append(prev)

    return gen_notes

def debug_gen(data):
    return data['note'].tolist()