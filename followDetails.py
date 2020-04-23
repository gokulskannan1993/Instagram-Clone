import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users

from models import *


JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True
)



# FollowDetails handler
class FollowDetails(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        # fetching current user
        user = users.get_current_user()
        currentUser = ndb.Key('User',user.user_id()).get()

        # get the details from url
        followString = self.request.get('followString')
        # fetching the selectedUser
        selectedUser = ndb.Key(urlsafe=(self.request.get('key'))).get()

        template_values = {
            'followString': followString,
            'currentUser' : currentUser,
            'selectedUser': selectedUser
        }

        template = JINJA_ENVIRONMENT.get_template('followDetails.html')
        self.response.write(template.render(template_values))
