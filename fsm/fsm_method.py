import os, sys, json
from py_fsmcls import *


class fsm_workflow_engine():

    def __init__(self, evntfle=None, tenantName=None):
        self.fsm = {}
        #self.tuple_convrt = evntfle
        self.fsm = self.fsm_covrt_tuple(evntfle)
        self.work_flow_engine = Work_Flow_Engine(); 


    def tuple_convrt(self, evntjson):
        try:
            self.fsmRespcls = Work_Flow_Engine(evntjson) 
        except Exception as eR:
            print "fsm_convert_tuple function_Exception :: %s"%eR

    def fsm_covrt_tuple(self, data):
        try:
            fsm = {}
            for key, value in data.items():
                for eventkey,  eventVal in value.items():
                    tup = tuple((key, eventkey)) 
                    fsm[tup] = eventVal
                    #self.run_engine(tup, eventVal)
        except Exception as er:
            print "tuple_convrt exception error :: %s"%er
        return fsm 

    def run_engine(self, curr_state, event):

        new_state = None;
        fnArgs = []
        try:
            key_tuple  = tuple((curr_state, event))
            curr_val= self.fsm[key_tuple]
            if curr_state is not None:
                fnName = curr_val['action']
                new_state = curr_val['nextstate'] 
                funKey = self.work_flow_engine.get_keywords(fnName) 
                if funKey is not None:
                    funKey()
        except Exception as er:
            print "could not find Keyword Function :: %s"%er
        return new_state

if __name__ == "__main__":

    with open('stateJson.json') as fsm:
        data = json.load(fsm)
    engine = fsm_workflow_engine(data);
    for key, value in data.items():
        for eventkey, eventval in value.items():
            result = engine.run_engine(key, eventkey)
