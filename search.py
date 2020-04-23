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



# Search handler
class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # fetching current user
        user = users.get_current_user()
        currentUser = ndb.Key('User',user.user_id()).get()

        searchedOutput = []

        # Searching users
        if self.request.get('button') == 'Search':
            queryInput = self.request.get('queryInput')
            if queryInput:
                text = queryInput.lower()
                limit = text[:-1] + chr(ord(text[-1]) + 1)
                searchedOutput = User.query(User.name >= text, User.name < limit).fetch()


        template_values = {
          'searchedOutput': searchedOutput,
          'currentUser': currentUser,

        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))
