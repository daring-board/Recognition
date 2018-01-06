import urllib.request
import json

class Weather:
    def __init__(self):
        src_path = 'primary_area.txt'
        f = open(src_path, 'r')
        local_dict = {}
        line = f.readline()
        while line:
            loc = line.strip()
            local_dict[loc] = {}
            while True:
                line = f.readline()
                items = line.strip().split('：')
                if '<delim>' in line: break
                local_dict[loc][items[1]] = items[0]
            line = f.readline()
        f.close()
        self.loc_dic = local_dict
        self.loc = ''
        self.reg = ''

    def weather(self, txt):
        loc, reg = '', ''
        res = '予報する都道府県と地区を教えてください。'
        for key in self.loc_dic.keys():
            if key in txt: loc = key
        if loc == '' and self.loc == '':
            print('no loc')
            return res
        else:
            if loc != '': self.loc = loc
        for key in self.loc_dic[loc].keys():
            if key in txt: reg = self.loc_dic[loc][key]
        if reg == '' and self.reg == '':
            res = '予報する地区を教えてください。%sは、'%loc
            for key in self.loc_dic[loc].keys(): res += '%sと'%key
            res += 'です。'
            return res
        else:
            if reg != '': self.reg = reg
        location = self.reg #場所
        url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%location
        print(url)
        html = urllib.request.urlopen(url)
        jsonfile = json.loads(html.read().decode('utf-8'))
        print(jsonfile['description'])
        return jsonfile['description']['text'].replace('\n', '')
