import pandas as pd
import json
import re

def generate_json(dataframe):
    data = dataframe
    data['prev'] = data['note'].shift(1)
    data = data.drop([0], axis=0)
    df = data[["prev","note"]]
    grouped_df = df.groupby(["note","prev"]).size().reset_index()
    unique_notes = pd.Index(grouped_df['note'].append(grouped_df['prev']).reset_index(drop=True).unique())
    grouped_df.rename(columns={0:'count'}, inplace=True)
    temp_links_list = list(grouped_df.apply(lambda row: {"source": row['prev'], "target": row['note'], "value": row['count']}, axis=1))
    links_list = []
    for link in temp_links_list:
        record = {"value":link['value'], "source":unique_notes.get_loc(link['source']), "target": unique_notes.get_loc(link['target'])}
        links_list.append(record)
    data = data.astype(str)
    data['octave'] = data['octave'].replace('rest', '')
    nodes_list = []
    for note in unique_notes:
        note_data = data[data['note'] == note]
        try:
            size = str(df.groupby('prev').count().loc[note].values[0])
        except:
            size='1'
        nodes_list.append({"name":note, "group":note_data['octave'].values[0], "size":size, "label":note_data['step'].values[0] + note_data['alter'].map({'0':'', '1':'#', '2':'##', '-1':'b', '-2':'bb'}).values[0] + note_data['octave'].values[0] + ' ' + note_data['dot'].map({'nodot':'', 'dot':'dot ', 'dotdot': 'double dot '}).values[0] + note_data['type'].values[0] + str(note_data['chord'].map({'nonchord':'', 'chord':' in chord'}).values[0])})
    json_prep = {"nodes":nodes_list, "links":links_list}
    json_dump = json.dumps(json_prep, indent=1, sort_keys=True)
    return json_dump
