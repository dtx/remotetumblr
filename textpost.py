import argparse
import glob
import json
import os
import time
import urllib2
import urlparse
import oauth2
import reqBody
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

class APIError(StandardError):
    def __init__(self, msg, response=None):
        StandardError.__init__(self, msg)

class TumblrAPIv2:
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_token_secret):
        self.consumer = oauth2.Consumer(consumer_key, consumer_secret)
        self.token = oauth2.Token(oauth_token, oauth_token_secret)
        self.url = "http://api.tumblr.com"

    def parse_response(self, result):
        content = json.loads(result)
        if 400 <= int(content["meta"]["status"]) <= 600:
            raise APIError(content["meta"]["msg"], result)
        return content["response"]

    def createPhotoPost(self, id, post):
        url = self.url + "/v2/blog/%s/post" %id

        #img_file = post['body']
        #del(post['body'])
        str = open(post['body'], 'rb').read()
        post['body'] = str
        req = oauth2.Request.from_consumer_and_token(self.consumer,
                                                 token=self.token,
                                                 http_method="POST",
                                                 http_url=url,
                                                 parameters=post)
        req.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.consumer, self.token)
        compiled_postdata = req.to_postdata()
        all_upload_params = urlparse.parse_qs(compiled_postdata, keep_blank_values=True)

        for key, val in all_upload_params.iteritems():
            all_upload_params[key] = val[0]

        #all_upload_params['body'] = open(img_file, 'rb')
        datagen, headers = multipart_encode(all_upload_params)
        request = urllib2.Request(url, datagen, headers)

        try:
            respdata = urllib2.urlopen(request).read()
        except urllib2.HTTPError, ex:
            return 'Received error code: ', ex.code

        return self.parse_response(respdata)

#Set up the CLI environment.
parser = argparse.ArgumentParser(description='Tumblr API for Pythonrunners! ^^')
parser.add_argument('filename', metavar='FILEMASK', type=str,
        help='a filepath to read the data from')
parser.add_argument('-t', dest='type', help='The type of the post, text/photo, defaults to text',
       default='text')
parser.add_argument('-s', dest='state', help='The state of the post, can be published, draft or queue. Defaults to publish.',
        default='published')
parser.add_argument('-g', dest='tags', help="A string of comma seperated tags wrapped in quotes, eg: 'tags, helpers, taggers'")
parser.add_argument('-w', dest='tweet', help='Text to tweet, or off to disable default set on Tumblr.')
parser.add_argument('-m', dest='markdown', default= 'false', help='Set if provided text post is markdown, set to false by default')
args = parser.parse_args()
#TODO: Add a checker to check the validity of args

#make the basic request body
bodymaker = reqBody.reqBodyMaker()
post1= bodymaker.makeBody(args)

register_openers()

CONSUMER_KEY = 'KOh8sy3TRszyliDMOMxbTga6Il9tDcrQ3l7FYUt5TgjG7dMDzF'
CONSUMER_SECRET = 'c7XCB7TcQ9duEkHPxotb24d7GYUXRxZ5qaQXwBvs0sJhKoKSTP'
OAUTH_TOKEN = 'qcHD4Y5BtB8AvaAYl0XQIcrJJ0gxIGnynkAMoPh6uFyvmQPL1S'
OAUTH_TOKEN_SECRET = 'zjqix3Ce2aTdOoIvnacPCfRLyh0rgKxJ1GMPM1G9GR6oHqY0rZ'

#TODO: DIR should be set to the current directory
DIR = '/Users/dsanghani/git/remotetumblr/'
FILE_MASK = args.filename
BLOG = 'dtx4.tumblr.com'


api = TumblrAPIv2(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
for img in glob.glob(os.path.join(DIR, FILE_MASK)):

    date  = time.gmtime(os.path.getmtime(img))
    post = {
        'type': args.type,
        'state': 'draft',
        'date': time.strftime("%Y-%m-%d %H:%M:%S", date),
        'body': img,
        'tags': time.strftime("%Y", date) + ", photo",
        'title': 'yaya1'
    }


    try:
        print 'Sending data'
        #response = api.createPhotoPost(BLOG,post)
        #if 'id' in response:
        #   print response['id']
        #else:
        #   print response
        #   break

    except APIError:
        print "Error"
        break

print "Done!"

