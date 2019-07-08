Data = {
	"definitions": {
		"process": {
			"startEvent": {
				"extensionElements": {
					"properties": {
						"property": [
							{
								"_name": "nextstate",
								"_value": "Approved",
								"__prefix": "camunda"
							},
							{
								"_name": "action",
								"_value": "Rejected",
								"__prefix": "camunda"
							}
						],
						"__prefix": "camunda"
					},
					"__prefix": "bpmn"
				},
				"_id": "Init_State",
				"__prefix": "bpmn"
			},
			"_id": "Process_03lluia",
			"_isExecutable": "true",
			"__prefix": "bpmn"
		},
		"BPMNDiagram": {
			"BPMNPlane": {
				"BPMNShape": {
					"Bounds": {
						"_x": "179",
						"_y": "81",
						"_width": "36",
						"_height": "36",
						"__prefix": "dc"
					},
					"_id": "_BPMNShape_StartEvent_2",
					"_bpmnElement": "Init_State",
					"__prefix": "bpmndi"
				},
				"_id": "BPMNPlane_1",
				"_bpmnElement": "Process_03lluia",
				"__prefix": "bpmndi"
			},
			"_id": "BPMNDiagram_1",
			"__prefix": "bpmndi"
		},
		"_xmlns:bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
		"_xmlns:bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
		"_xmlns:dc": "http://www.omg.org/spec/DD/20100524/DC",
		"_xmlns:camunda": "http://camunda.org/schema/1.0/bpmn",
		"_id": "Definitions_0t5g447",
		"_targetNamespace": "http://bpmn.io/schema/bpmn",
		"_exporter": "Camunda Modeler",
		"_exporterVersion": "3.1.2",
		"__prefix": "bpmn"
	}
}
      
_id = Data["definitions"]["process"]["startEvent"]["_id"]
print _id
Keyval = Data["definitions"]["process"]["startEvent"]["extensionElements"]["properties"]["property"]
print Keyval
keyDict = {}
for i in Keyval:
    key = i["_name"]
    val = i["_value"]
    keyDict[key] = val
print keyDict

    