
from flask import Flask, request, render_template, url_for, redirect, jsonify
import time

class clor:

    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


print(clor.BOLD + clor.BLUE + '\n' + 'Mark IMPORTER' + clor.ENDC)

print(clor.YELLOW + '\n' +'\nLoading a Application may takes some time [maximum 10-20 or more seconds] depend on you system speed\n'+ clor.ENDC)
time.sleep(0.8)


from utils import Database
from create_taggs import Load_tags
import threading

db = Database()


def tranverse_data(username):
    
    raw_tag_list = []
    all_tags_list = {}
    show_tags = {}

    data = db.retu_data(username)
    for item in data:

        tags = str(data[item])

        if tags not in raw_tag_list:

            raw_tag_list.append(tags)

            s_no = raw_tag_list.index(tags)
            all_tags_list[s_no] = [item]
            show_tags[str(s_no)] = data[item]

        else:
            ind_no = raw_tag_list.index(tags)
            all_tags_list[ind_no].append(item)
            
    return all_tags_list, show_tags


def load_mark(bookmark_link, username):
    all_tags = Load_tags(bookmark_link) # get all tags

    input_data = {bookmark_link: all_tags} # preparing data to get in the database
        
    db.load_data_in(input_data, username) # import data to database


def thread_mark(link,username):
    threading.Thread(target=load_mark, args=(link, username)).start()


app = Flask(__name__)

@app.route('/bookmarks/username=<username>', methods=['GET', 'POST'])

def index_page(username):

    links = db.retu_data(username)

    if request.method == 'POST':
        query = request.form['bookmark']
        bookmark_link =  query
        
        thread_mark(bookmark_link, username)
        
    list_links, show_tags = tranverse_data(username)
    total_len = len(list_links)

    return render_template('index.html', username=username, tags=show_tags)


@app.route('/login', methods=['GET', 'POST'])

def login():

    message = 0

    if request.method == "POST":
        username = request.form['email']
        
        try:
            db.insert_user_account(username)
            return redirect(url_for('index_page', username=username))
        
        except:
            message = 1

    else: return render_template("login.html", message=message)


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/bookmark/target/link_num=<link_num>,username=<username>')
def link_list(link_num, username):

    links, useless_list = tranverse_data(username)
    links = links[int(link_num)]

    return render_template('bookmark_targe.html', links=links)


if __name__=='__main__':
    app.run(host='127.0.0.1', port=7923)
