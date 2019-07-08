import json
import xmltodict
import pprint


#with open("workflow_diagram.bpmn") as f:
#    jsondict = xmltodict.parse(f.read())

#pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(json.dumps(jsondict))

#print type(jsondict)


import xml.etree.ElementTree as ET
import xmltodict
import json

tree = ET.parse("Sample_Test.bpmn")
xml_data = tree.getroot()

xmlstr = ET.tostring(xml_data, encoding='utf8', method='xml')
data_dict = dict(xmltodict.parse(xmlstr))


print data_dict



