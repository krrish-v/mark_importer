
import json
import numpy as np

database_path = 'database/datbase.json'


class Database():

    def w_open(self):

        self.fl_open = open(database_path, 'w')
        return self.fl_open

    def r_open(self):

        try:
            self.fl_read = open(database_path, 'r')
            read_data = json.load(self.fl_read)
            self.fl_read.close()
        except: read_data = None

        return read_data

    def __init__(self):
        self.read_data = self.r_open()
    
    def insert_user_account(self, username):

        self.username = username

        if self.read_data is None:

            self.f_1 = self.w_open()
            self.username = username

            self.read_data ={self.username: 
            {'www.libyser.herokuapp.com ': ['Books Store', 'E-book Scrapper']}
            }

            json.dump(self.read_data, self.f_1)
            self.f_1.close()
        
        else:

            if self.username not in self.read_data:
                self.f_1 = self.w_open()
                self.read_data.update({self.username: {}})
                json.dump(self.read_data, self.f_1)
                self.f_1.close()

        return self.username

    def load_data_in(self, input_data : dict, username):

        self.username = username
        self.input_data = input_data
        
        if self.username in self.read_data:

            try:
                self.f_1 = self.w_open()
                self.new_data = self.read_data[self.username]
                self.new_data.update(self.input_data)

                json.dump(self.read_data, self.f_1)
                self.f_1.close()

                return True
                
            except: return False # if it is False the database will be lost
        else: return False

    def retu_data(self, username):
        self.username = username
        
        return self.r_open()[self.username]


# Demonstration


#a = Loading().put_pridiction('You can play with a live demo of the web app here. You just input in the text box a song name (e.g. juice), or an artist name followed by a song name (e.g. harry styles watermelon sugar), and press enter.')
#print(a)

#init_data = {'https://google-book.com': ['e-book', 'book search']}

#db = Database()

#username = db.insert_user_account('hello')
#username = "chalo"
#db.insert_user_account(username)
#print(db.load_data_in(init_data, 'hell'))
