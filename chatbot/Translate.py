# To translate text between chinese and English
# If query_text is in English, result_text will be in chinese
# If query_text is in chinese, result_text will be in English

# Import module
import requests
import json
import random

# Use the youdao's api to translate
def translate(query_text):
    # To randomly get keyfrom and key
    keyfrom_key = random.choice(keyfrom_keys)
    # Construct the url
    url= "http://fanyi.youdao.com/openapi.do?keyfrom={}&key={}&type=data&doctype=json&version=1.1&q={}"\
        .format(keyfrom_key["keyfrom"], keyfrom_key["key"], query_text)
    try:
        # Get request
        r = requests.get(url).text
        # Transform into dictionary
        resp_dict = json.loads(r)
        # Get result
        result_text = resp_dict["translation"][0]
    except Exception as e:
        # Deal with the exception.
        #print("I can't deal with it." + "The problem is" + str(e))
        result_text = ""
    return result_text

# The list of keyfrom and key for authentication
keyfrom_keys = [
    {
        "keyfrom": 'xujiangtao',
        "key":'1490852988'
    },
    {
        "keyfrom": 'ltxywp',
        "key": '1092195550'
    },
    {
        "keyfrom": 'txw1958',
        "key": '876842050'
    },
    {
        "keyfrom": 'youdanfanyi123',
        "key": '1357452033'
    },
    {
        "keyfrom": 'fadabvaa',
        "key": '522071532'
    },
    {
        "keyfrom": 'yyxiaozhan',
        "key": '1696230822'
    },
    {
        "keyfrom": 'siwuxie095-test',
        "key": '2140200403'
    },
    {
        "keyfrom": '11pegasus11',
        "key": '273646050'
    },
    {
        "keyfrom": 'webblog',
        "key": '1223831798'
    },
    {
        "keyfrom": 'wojiaozhh',
        "key": '1770085291'
    },
    {
        "keyfrom": 'atmoon',
        "key": '1407453772'
    },
    {
        "keyfrom": 'morninglight',
        "key": '1612199890'
    },
    {
        "keyfrom": 'Yanzhikai',
        "key": '2032414398'
    },
    {
        "keyfrom": 'JustForTestYouDao',
        "key": '498375134'
    },
    {
        "keyfrom": 'aaa123ddd',
        "key": '336378893'
    },
    {
        "keyfrom": 'aaa123ddd',
        "key": '336378893'
    },
    {
        "keyfrom": "wjy-test",
        "key": "36384249"
    },
    {
        "keyfrom": "youdao111",
        "key": "60638690"
    },
    {
        "keyfrom": "pythonfankjjkj1",
        "key": "1288254626"
    },
    {
        "keyfrom": "Dic-EVE",
        "key": "975360059"
    },
    {
        "keyfrom": "youdianbao",
        "key": "1661829537"
    },
    {
        "keyfrom": "AndroidHttpTest",
        "key": "507293865"
    },
    {
        "keyfrom": "123licheng",
        "key": "1933182090"
    },
    {
        "keyfrom": "pdblog",
        "key": "993123434"
    },
    {
        "keyfrom": "testorot",
        "key": "1145972070"
    },
    {
        "keyfrom": "node-translator",
        "key": "2058911035"
    },
    {
        "keyfrom": "mytranslator1234",
        "key": "1501976072"
    },
    {
        "keyfrom": "SkyHttpGetTest",
        "key": "545323935"
    },
    {
        "keyfrom": "htttpGetTest",
        "key": "1230480132"
    },
    {
        "keyfrom": "neverland",
        "key": "969918857"
    },
    {
        "keyfrom": "HTTP-TESTdddaa",
        "key": "702271149"
    },
    {
        "keyfrom": "fadabvaa",
        "key": "522071532"
    },
    {
        "keyfrom": "atmoon",
        "key": "1407453772"
    },
    {
        "keyfrom": "orchid",
        "key": "1008797533"
    },
    {
        "keyfrom": "chdego",
        "key": "1347056326"
    },
    {
        "keyfrom": "cxvsdffd33",
        "key": "1310976914"
    },
    {
        "keyfrom": "123licheng",
        "key": "1933182090"
    },
    {
        "keyfrom": "huichuang",
        "key": "386196262"
    },
    {
        "keyfrom": "eweewqeqweqwe",
        "key": "957582233"
    },
    {
        "keyfrom": "abc1243",
        "key": "1207861310"
    },
    {
        "keyfrom": "xxxxxxx",
        "key": "1618693256"
    },
    {
        "keyfrom": "mypydict",
        "key": "27855339"
    },
    {
        "keyfrom": "zqhong",
        "key": "694644553"
    },
    {
        "keyfrom": "wangtuizhijia",
        "key": "1048394636"
    },
    {
        "keyfrom": "xinlei",
        "key": "759115437"
    },
    {
        "keyfrom": "youdaoci",
        "key": "694691143"
    },
]

