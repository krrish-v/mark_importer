
try:
    import numpy as np
    import pickle
    import json
    import warnings

except: raise ImportError('Packages missing, see requirement.txt')

warnings.filterwarnings("ignore")

try:
    f_model = open('model_data/prid_model.sav', 'rb')
    means_model = pickle.load(f_model)
    f_model.close()
    
except: raise Exception("Can't load the Pridiction model")


try:
    f_arranged_topic_file = open('model_data/json_files/pridicted_tags.json', 'r')
    set_topic_tags = json.load(f_arranged_topic_file)
    f_arranged_topic_file.close()

except: raise EOFError("Can't load the ['/json_files/pridicted_tags.json'] file")


class Model:

    def pridict_topic(self, to_prid_data: np.array):
        '''
        Input Parameter: (prid_data) => numpy array, shape = (x, -x) dtype = float32
        
        Output: type == str => topic <no>
        '''
        
        topic_data = means_model.predict(to_prid_data)

        self.topic_out = 'topic ' + str(topic_data[0])

        return self.topic_out

    def get_topic(self, to_prid_data):
        
        self.settopic_element = self.pridict_topic(to_prid_data=to_prid_data)

        self.all_tags = set_topic_tags[self.settopic_element]

        return self.all_tags[0][-4:]
