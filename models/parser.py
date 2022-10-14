
try:
    import requests
    import random
    from bs4 import BeautifulSoup
    from nltk import RegexpTokenizer
    from nltk.tokenize import word_tokenize

except: raise ImportError('Packages missing, see requirement.txt')


# user-agenst
ua = {
    #1: '/libser_engine/utils/ua/android_webkit',
    2: 'models/ua/Chrome',
    3: 'models/ua/Edge',
    #'firefox': '/libser_engine/utils/ua/Firefox',
    #'intenet_explorer': 'LIBSER/libser_engine/utils/ua/Internet+Explorer',
    4: 'models/ua/Opera',
    #'safari': '/libser_engine/utils/ua/Safari'
    }

sec_ch_ua = {
    2: '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"', # chrome
    3: '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"', #edge
    4: '"Opera";v="81", " Not;A Brand";v="99", "Chromium";v="95"' # opera
}

ua_edge_3 = None
ua_chrome_2 = None
ua_opera_4 = None

for user_agent in ua:
    agents_data = open(ua[user_agent]).read()
    tok = RegexpTokenizer(r'\n', gaps=True)
    agents_ = tok.tokenize(agents_data)
    if user_agent == 2:
        ua_chrome_2 = agents_
    elif user_agent == 3:
        ua_edge_3 = agents_
    elif user_agent == 4:
        ua_opera_4 = agents_


class Headers:
    
    def __init__(self):
        self.choose_browser = random.randint(2, 4)
        self.secchua = sec_ch_ua[self.choose_browser]

        if self.choose_browser == 2: self.header = ua_chrome_2[random.randint(0, 848)]
        elif self.choose_browser == 3: self.header = ua_edge_3[random.randint(0, 7)]
        elif self.choose_browser == 4:self.header = ua_opera_4[random.randint(0, 991)]

    def user_agent(self):
        return self.header

    def parm_(self):

        self.payload = {
            'Upgrade-Insecure-Requests': '1',
            'Sec-Ch-Ua': self.secchua,
            'Sec-Ch-Ua-Mobile': '?0',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'User-Agent': self.header,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Connection': 'keep-alive',
        }
        
        return self.payload


class Parse:

    def get_text(self, link):
        self.link = link
        self.parameter = Headers().parm_()
        
        self.status = 400
        try: 
            self.rec = requests.get(self.link, headers=self.parameter)
            self.html_data = self.rec.text
            self.status = self.rec.status_code
        except: self.html_data = None
        
        return self.html_data, self.status
    

    def parse_text(self, link):

        self.link = link
        self.html_data, self.status = self.get_text(self.link)

        if self.html_data is not None and self.status == 200:
        
            try:
                soup = BeautifulSoup(self.html_data, 'html.parser')
    
                self.whole_text = ''
                for text_1 in soup.find_all('p'):

                    if len(word_tokenize(text_1.text)) != 1:
                        self.whole_text += text_1.text + ' '

            except: self.whole_text = None
        else: self.whole_text = None

        return self.whole_text


#we = Parse()
#text = we.parse_text('https://towardsdatascience.com/embeddings-embeddings-everywhere-5c1d292d73e3')
#print(text)
