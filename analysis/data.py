#!/usr/bin/env python

import json
from pprint import pprint


class Data:
    
    def __init__(self, data):
        try:
            #print("trying")
            self.data = self.read_json(data)
        except:
            #print("failing")
            #if it's not a valid file, then we should assume it's json already
            self.data = data
        self.data_dict, self.names, self.problems, self.problem = self.extract_data()
        self.averages = self.get_averages()
#        print(self.problems)    
#        print(self.headers)    
#        pprint(self.data_dict)

    """
    parameter: JSON array of objects form

    [ {date: [{question/answer}, {question/answer}, ...] }, ... }

    returns header array containing the name for each question/answer and a dict
    with key = date, value = array of answers for that date corresponding to the 
    question names in header, so 

    {'2017-06-01': [4, 6.75, 22.75, 0, 6, 0, 10, 0, 20, 8], ... }

    """
    def extract_data(self):
        data_dict = dict(self.data)
        nicer_data_dict = {}
        names = []
        problems = []
        filled_names = False
        problem = ""
        for key, value in data_dict.items():
            nicer_data_dict[key] = []        
            vals = list(value)
            for val in vals:
                question = dict(val)
                #build an array of question names and T/F for if problem
                if not filled_names:
                    names.append(question['name'])
                    problems.append(question['problem'])
                    if question['problem']:
                        problem = question['name']
                nicer_data_dict[key].append(float(question['answer']))
            filled_names = True
        return nicer_data_dict, names, problems, problem

    """
    Finds the average daily value for each feature
    """
    def get_averages(self):
        ave_denom = len(self.data_dict.keys()) + 1
        averages = [0] * len(self.names)
        for val in self.data_dict.values():
            for i in range(len(val)):
                averages[i] += val[i]
        return [val / ave_denom for val in averages]

    """
    reads JSON from the given file
    """
    def read_json(self, filename):
        with open(filename) as f:
            return json.load(f)



