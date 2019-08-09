import json


#Json file update specific keyword value 

with open('data.json', 'r+') as f:
    data = json.load(f)
    for i in data:
        Id = i.get("fingerID")
        Type = i.get("05-08-2019")
        if  Id  == 10 and Type == "IN":           
            i['05-08-2019'] = "OUT"  # <--- add `Type` value. 
            f.seek(0)                # <--- should reset file position to the beginning.
            json.dump(data, f)       
            f.truncate()             # remove remaining part
            break
        else:
            if Id == 10 and Type == "OUT":                
                i["05-08-2019"] = "IN";  # <--- add `Type` value.
                f.seek(0)                # <--- should reset file position to the beginning.
                json.dump(data, f)
                f.truncate()             # remove remaining part
                break
