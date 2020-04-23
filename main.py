import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from datetime import datetime
from profile import Profile
from downloadHandler import DownloadHandler
from uploadHandler import UploadHandler
from models import *
from followDetails import FollowDetails

from search import Search

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
        currentUser = None
        allPosts = []

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
                    name = username.lower()
                     )
                myuser.put()
                userKey = ndb.Key('User',user.user_id())
                currentUser = userKey.get()
            else:
                # select all posts in reverse chronological order
                query = Post.query().order(-Post.date).fetch()
                for post in query:
                    if post.user == currentUser.key or post.user in currentUser.following:
                        if len(allPosts) <= 50:
                            allPosts.append(post)

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'


        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'currentUser':currentUser,
            'upload_url' : blobstore.create_upload_url('/upload'),
            'allPosts'  : allPosts


        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'


        # fetching current user
        user = users.get_current_user()
        currentUser = ndb.Key('User',user.user_id()).get()


        # if the user wants to add comment
        if self.request.get('button') == 'Add Comment':
            # retrieve the post
            postKey = self.request.get('postKey')
            post = ndb.Key('Post',int(postKey)).get()

            # retieve the text
            commentText = self.request.get('addComment')

            if commentText:
                comment = Comment(
                    text = commentText,
                    author = currentUser.key
                )
                post.comments.insert(0, comment)
                post.put()

            self.redirect('/')





app = webapp2.WSGIApplication(
            [
            ('/', MainPage),
            ('/upload', UploadHandler),
            ('/profile', Profile),
            ('/download', DownloadHandler),
            ('/search', Search),
            ('/followDetails', FollowDetails)
            ],
        )
