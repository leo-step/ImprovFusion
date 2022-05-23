import xml.etree.cElementTree as ET
import pandas as pd
import random
import copy

def create_dataframe(column_chord, column_step, column_alter, column_octave, column_type, column_dot):
    data = pd.DataFrame(columns=['chord', 'step', 'alter', 'octave', 'type', 'dot'])
    data['chord'] = column_chord
    data['step'] = column_step
    data['alter'] = column_alter
    data['octave'] = column_octave
    data['type'] = column_type
    data['dot'] = column_dot
    data['note'] = data['chord'] + data['step'] + data['alter'] + data['octave'] + data['type'] + data['dot']
    return data

def create_previous(data):
    df = pd.DataFrame(columns=['prev3', 'prev2', 'prev', 'label'])
    df['prev'] = data['note']
    df['prev2'] = data['note']
    df['prev3'] = data['note']
    df['label'] = data['note']
    df['prev'] = df['prev'].shift(1)
    df['prev2'] = df['prev2'].shift(2)
    df['prev3'] = df['prev3'].shift(3)
    df.drop(df.index[[0,1,2]], inplace=True)
    df = df.reset_index(drop=True)
    df = df.astype(int)
    return df