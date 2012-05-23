# -*- coding: utf-8 -*-
import sys
import os.path

if sys.version_info < (3,0):
    import urllib as request
    parse = request
    import urllib2
    for method in dir(urllib2):
        setattr(request, method, getattr(urllib2, method))
    import cookielib as cookiejar
    
else:
    from http import cookiejar
    from urllib import parse, request



class Acapela(object):

    #Properties
    TTS_ENGINE = None
    ACCOUNT_LOGIN = None
    APPLICATION_LOGIN = None
    APPLICATION_PASSWORD = None
    SERVICE_URL = None
    QUALITY = None
    DIRECTORY = ''
    
    #Available voices list
    #http://www.acapela-vaas.com/ReleasedDocumentation/voices_list.php
    langs  = {
        'ES': {
            'W': {
                'NORMAL': 'ines',
            },
            'M': {
                'NORMAL': 'antonio',
            }
        },
        'BR': {
            'W': {
                'NORMAL': 'marcia',
            },
        },
        'EN': {
            'W': {
                'NORMAL': 'lucy',
            },
            'M': {
                'NORMAL': 'graham',
            },
        },
        'US': {
            'W': {
                'NORMAL': 'laura',
            },
            'M': {
                'NORMAL': 'heather',
            },
        },
        'FR': {
            'W': {
                'NORMAL': 'alice',
            },
            'M': {
                'NORMAL': 'antoine',
            },
        },
        'PT': {
            'W': {
                'NORMAL': 'marcia',
            },
        },
    }
    data = {}
    filename = None
    
    def __init__(self, tts_engine, account_login, application_login, application_password, service_url, quality, directory=''):
        """construct Acapela TTS"""
        self.TTS_ENGINE = tts_engine
        self.ACCOUNT_LOGIN = account_login
        self.APPLICATION_LOGIN = application_login
        self.APPLICATION_PASSWORD = application_password
        self.SERVICE_URL = service_url
        self.QUALITY = quality
        self.DIRECTORY = directory
    
    def prepare(self, text, lang, gender, intonation):
        """Prepare Acapela TTS"""
        lang = lang.upper()
        concatkey = "%s-%s-%s-%s" % (text, lang, gender, intonation)
        key =  self.TTS_ENGINE + '' + str(hash(concatkey))
        try:
            req_voice = self.langs[lang][gender][intonation] + self.QUALITY
        except:
            req_voice = 'lucy22k'
        
        self.data = {
            'cl_env': 'FLASH_AS_3.0',
            'req_snd_id': key,
            'cl_login': self.ACCOUNT_LOGIN,
            'cl_vers': '1-30',
            'req_err_as_id3': 'yes',
            'req_voice': req_voice,
            'cl_app': self.APPLICATION_LOGIN,
            'prot_vers': '2',
            'cl_pwd': self.APPLICATION_PASSWORD,
            'req_asw_type': 'STREAM',
        }
        self.filename = "%s-%s.mp3" % (key, lang)
        self.data['req_text'] = '\\vct=100\\ \\spd=160\\ %s' % text.encode("utf-8")
        
    def run(self):
        """run will call acapela API and and produce audio"""
        #check if file exists
        if os.path.isfile(self.DIRECTORY + self.filename):
            return self.filename
        else:
            encdata = parse.urlencode(self.data)
            request.urlretrieve(self.SERVICE_URL, self.DIRECTORY + self.filename, data=encdata)
            return self.filename