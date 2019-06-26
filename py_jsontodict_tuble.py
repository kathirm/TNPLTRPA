import json, os, sys


def convert_jsoninto_tuble(data):
    try:
        params = {}
        #paramlist = list()
        #for key, value in data.items():
            #params= key
            #paramlist.append((params, value))
        #    for k , v in value.items():
        #        tup = tuple(v.items())
        #        paramlist.append((key, k))
        #        paramlist.append(v)
                #paramlist.append((params, v))
        #print paramlist

        for key, value in data.items():
            for eventkey,  eventVal in value.items():
                #paramlist.append((key, eventkey))
                tub = tuple((key, eventkey))
                params[tub] = eventVal

        print params
    except Exception as er:
        print "Convert_jsoninto_tuble Exception error :: %s"%er





if __name__ == "__main__":
    
    inputFile = sys.argv[1]; 
    with open(inputFile) as f:
        data = json.load(f)
    inputValue = convert_jsoninto_tuble(data)
