import json, time, os


try:
    
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)   
        print type(data)
        for i in data:
            Id = i.get("Id") 
            place = i.get("location")
            if Id == 1:
                print "data match"
                intf = {}
                intf["Method"] = i.get("method")                                          
                intf["Id"] = i.get("Id") 
                intf["location"] = "Coimbatore"
                intfdata = json.dumps(intf)

                data.append(intfdata)
                print data 

           #     with open("data.json", "w") as jsonfile:
           #         json.dump(tmp, jsonfile)
           #     print place
                break
        else:
            print "No data found"

except Exception as e:
    print e
    

#tmp = data["location"]
#data["location"] = "Chennai"

#with open("data.json", "w") as jsonFile:
#    json.dump(data, jsonFile)
