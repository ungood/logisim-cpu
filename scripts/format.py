#!/usr/bin/env python3

import xml.etree.ElementTree as Tree

root = Tree.parse('cpu.circ')


cpu = root.find("circuit[@name='CPU']")


      # <a name="facing" val="east"/>
#       <a name="color" val="#e6e600"/>
#       <a name="label" val="T1"/>
#       <a name="labelloc" val="west"/>
#       <a name="labelfont" val="Courier bold 10"/>

def set_a(component, name, value):
    a = component.find(f"a[@name='{name}']")
    if a is None:
        a = Tree.SubElement(component, 'a')
    a.set('name', name)
    a.set('val', value)        

for led in cpu.findall("comp[@name='LED']"):
    label = led.find("a[@name='label']")
    set_a(led, 'labelfont', 'Courier bold 10')
    
root.write('cpu_formatted.circ')
