#!/usr/bin/env python3

import xml.etree.ElementTree as Tree

root = Tree.parse('cpu.circ')
cpu = root.find("circuit[@name='CPU']")

def set_a(component, name, value):
    a = component.find(f"a[@name='{name}']")
    if a is None:
        a = Tree.SubElement(component, 'a')
    a.set('name', name)
    a.set('val', value)        


# Set fonts and colors on LED components.
# <a name="facing" val="east"/>
# <a name="color" val="#e6e600"/>
# <a name="label" val="T1"/>
# <a name="labelloc" val="west"/>
# <a name="labelfont" val="Courier bold 10"/>
for led in cpu.findall("comp[@name='LED']"):
    label = led.find("a[@name='label']").attrib['val']
    set_a(led, 'labelfont', 'Courier bold 10')
    
    # Flag LEDs will be red.
    if label[-1] == 'F' or label == 'HALT':
        set_a(led, 'color', '#e60000')
    # Time step LEDs to be yellow.
    elif label[0] == 'T':
        set_a(led, 'color', '#e6e600')
    else:
        set_a(led, 'color', '#0000e6')

# <comp lib="6" loc="(273,201)" name="Text">
#   <a name="text" val="RAM" />
#   <a name="font" val="Courier New bold 24" />
#   <a name="valign" val="center" />
# </comp>
# Set fonts on text components
for text in cpu.findall("comp[@name='Text']"):
    set_a(text, 'font', 'Courier New bold 24')
    
root.write('cpu.circ')
