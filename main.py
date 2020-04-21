import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from datetime import datetime

from models import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)


# main handler
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        user = users.get_current_user()


        # initializing the strings and values
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        currentUser = None
        followers = 0
        following = 0





        # determine if we have a user logged in or not.
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'Logout'

            username = user.email().split("@")[0]


            userKey = ndb.Key('User',user.user_id())
            currentUser = userKey.get()


            if currentUser == None:
                welcome = 'Welcome to the application'
                myuser = User(
                    id = user.user_id(),
                    email = user.email(),
                    name = username
                     )
                myuser.put()
                userKey = ndb.Key('User',user.user_id())
                currentUser = userKey.get()
            else:
                followers = len(currentUser.followers)
                following = len(currentUser.following)




        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'


        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome': welcome,
            'currentUser':currentUser,
            'followers': followers,
            'following': following,
            'upload_url' : blobstore.create_upload_url('/upload'),


        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# class to handle the uploads
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = users.get_current_user()
        currentUser = ndb.Key('User',user.user_id()).get()

        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        caption = self.request.get('caption')

        if self.request.get('button') == 'Post':
            post = Post(
                caption = caption,
                image = upload.key(),
                date = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                user = currentUser.key
            )
            post.put()
            currentUser.posts.append(post.key)
            currentUser.put()
            self.redirect('/')







app = webapp2.WSGIApplication(
            [
            ('/', MainPage),
            ('/upload', UploadHandler),


            ],

        )
