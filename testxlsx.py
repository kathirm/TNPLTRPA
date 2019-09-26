import csv, json
import requests
import pandas as pd
json_text = """[{'Shop': u'Testing', 'EmpId': u'PRO-03000', 'EmpName': u'Raja', 'Branch': u'Testing'}, {'Shop': u'Testing', 'EmpId': u'PRO-04000', 'EmpName': u'S Bala', 'Branch': u'Testing'}, {'Shop': u'Testing', 'EmpId': u'PRO-04001', 'EmpName': u'M Ravi', 'Branch': u'Testing'}]"""


F = [{'Shop': u'Testing', 'EmpId': u'PRO-03000', 'EmpName': u'Raja', 'Branch': u'Testing'}, {'Shop': u'Testing', 'EmpId': u'PRO-04000', 'EmpName': u'S Bala', 'Branch': u'Testing'}, {'Shop': u'Testing', 'EmpId': u'PRO-04001', 'EmpName': u'M Ravi', 'Branch': u'Testing'}]
G = json.dumps(F)
print G

df = pd.read_json(G)
df.to_excel('text.xlsx', index=False)



