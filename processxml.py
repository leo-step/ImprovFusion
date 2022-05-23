import xml.etree.cElementTree as ET
from convert import typetotime_num, typetotime_den
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

def writexml(root, data, gen_notes):
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
    return ET.tostring(root, encoding='utf8', method='xml')
    #tree.write('output.xml')





