import json, os, sys 

class Work_Flow_Engine():

    def __init__(self, state_defn_json=None):

        self.keyFuncMap = {'send_email':self.email_notification, 'success_alert': self.success_alert, 'init_state': self.init_state,
                            'processing': self.processing_state, 'approved_state': self.approved_state, 'pending' : self.pending_state, 
                            'complete_state' : self.complete_state
                        }


    def get_keywords(self, name): 
        return self.keyFuncMap[name];

    def email_notification(self):
        print "Hi im send_email email_notification"

    def success_alert(self):
        print "Hi im success alert function"

    def init_state(self):
        print "Hi im init_state alert function"

    def processing_state(self):
        print  "hi im processing_state aler function"

    def approved_state(self):
        print "Hi im approved_state machine"

    def pending_state(self):
        print "Hi im pending_state machine fsm"

    def complete_state(self):
        print "HI im complete state alert"
