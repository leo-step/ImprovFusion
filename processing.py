import xml.etree.cElementTree as ET
import pandas as pd
import random
import copy

def readxml(root, column_chord, column_step, column_alter, column_octave, column_type, column_dot):
    for child1 in root:
        if child1.tag == 'part':
            for child2 in child1:
                for child3 in child2:
                    if child3.tag == 'note':
                        if str(ET.tostring(child3)).find("<voice>1</voice>") != -1:
                            if child3[0].tag == 'chord':
                                column_chord.append('chord')
                            else:
                                column_chord.append('nonchord')
                            dot = ''
                            alter = '0'
                            for child4 in child3:
                                if child4.tag == 'pitch':
                                    for child5 in child4:
                                        if child5.tag == 'step':
                                            column_step.append(child5.text)
                                        elif child5.tag == 'alter':
                                            alter = child5.text
                                        elif child5.tag == 'octave':
                                            column_octave.append(child5.text)
                                elif child4.tag == 'rest':
                                    column_step.append('rest')
                                    column_octave.append('rest')
                                elif child4.tag == 'type':
                                    column_type.append(child4.text)
                                if child4.tag == 'dot':
                                    dot = dot + 'dot'
                            if dot == '':
                                dot = 'nodot'
                            column_dot.append(dot)
                            column_alter.append(alter)

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

def convertparam(param):
    switcher2 = {
        0:[-1],
        1:[1],
        2:[1,2],
        3:[1,2,3],
        4:[1,2,3,4],
        5:[1,2,3,4,5],
        6:[1,2,3,4,5,6],
        7:[1,2,3,4,5],
        8:[1,2,3,4],
        9:[1,2,3],
        10:[1,2],
        11:[1],
        12:[-1]

    }
    twonote = switcher2.get(param, [-1])
    switcher3 = {
        0:[-1],
        1:[-1],
        2:[-1],
        3:[-1],
        4:[-1],
        5:[-1],
        6:[-1],
        7:[6],
        8:[5,6],
        9:[4,5,6],
        10:[3,4,5,6],
        11:[2,3,4,5,6],
        12:[1,2,3,4,5,6]

    }
    if param > 12:
        threenote = switcher3.get(param, [1,2,3,4,5,6])
    else:
        threenote = switcher3.get(param, [-1])

    return twonote, threenote

def model(df, n_notes=100, param=2):
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

def typetotime_num(note_type, note_dot):
    combined = note_type + note_dot
    switcher = {
        'eighthnodot': '1',
        'quarternodot': '1',
        'halfnodot': '1',
        'wholenodot': '1',
        '16thnodot': '1',
        '32ndnodot': '1',
        'eighthdot': '3',
        'quarterdot': '3',
        'halfdot': '3',
        'wholedot': '3',
        '16thdot': '3',
        'eighthdotdot': '7',
        'quarterdotdot': '7',
        'halfdotdot': '7',
        'wholedotdot': '7'
    }
    return switcher.get(combined, '1')

def typetotime_den(note_type, note_dot):
    combined = note_type + note_dot
    switcher = {
        'eighthnodot': '8',
        'quarternodot': '4',
        'halfnodot': '2',
        'wholenodot': '1',
        '16thnodot': '16',
        '32ndnodot': '32',
        'eighthdot': '16',
        'quarterdot': '8',
        'halfdot': '4',
        'wholedot': '2',
        '16thdot': '32',
        'eighthdotdot': '32',
        'quarterdotdot': '16',
        'halfdotdot': '8',
        'wholedotdot': '4'
    }
    return switcher.get(combined, '4')

def writexml(root, tree, data, gen_notes):
    for child in root:
        if child.tag == 'part':
            attributes_template = child[0][0]
            while len(child) > 0:
                child.remove(child[0])
            measure_number = 0
            for i in range(len(gen_notes)):
                row = data[data['note'] == gen_notes[i]].drop_duplicates()
                chord = row['chord'].values[0]
                step = row['step'].values[0]
                octave = row['octave'].values[0]
                note_type = row['type'].values[0]
                dot = row['dot'].values[0]
                alter = row['alter'].values[0]
                if chord == 'nonchord':
                    attributes = copy.deepcopy(attributes_template)
                    measure_number += 1
                    measure = ET.SubElement(child, 'measure')
                    measure.set("number", str(measure_number))
                    measure.append(attributes)
                    attributes[2][0].text = typetotime_num(note_type, dot)
                    attributes[2][1].text = typetotime_den(note_type, dot)
                note = ET.SubElement(measure, 'note')
                if chord == 'chord':
                    note_chord = ET.SubElement(note, 'chord')
                if step == 'rest':
                    rest = ET.SubElement(note, 'rest')
                else:
                    pitch = ET.SubElement(note, 'pitch')
                    note_step = ET.SubElement(pitch, 'step')
                    note_step.text = step
                    note_alter = ET.SubElement(pitch, 'alter')
                    note_alter.text = alter
                    note_octave = ET.SubElement(pitch, 'octave')
                    note_octave.text = octave
                note_duration = ET.SubElement(note, 'type')
                note_duration.text = note_type
                if dot == 'dot':
                    note_dot = ET.SubElement(note, 'dot')
                elif dot == 'dotdot':
                    note_dot = ET.SubElement(note, 'dot')
                    note_dot = ET.SubElement(note, 'dot')
    tree.write('output.xml')