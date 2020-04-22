import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)


class Profile(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # fetching current user
        user = users.get_current_user()
        currentUser = ndb.Key('User',user.user_id()).get()

        # fetching the selectedUser
        selectedUser = ndb.Key(urlsafe=(self.request.get('key'))).get()

        followString = 'Follow'

        # fetching all the posts of selectedUser
        allPosts = []
        for post in selectedUser.posts:
            allPosts.insert(0, post.get())

        # check if the currentUser follows selectedUser
        if selectedUser.key in currentUser.following:
            followString = 'Unfollow'





        template_values = {
            'selectedUser': selectedUser,
            'currentUser': currentUser,
            'followers': len(selectedUser.followers),
            'following': len(selectedUser.following),
            'allPosts': allPosts,
            'followString': followString
        }

        template = JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
