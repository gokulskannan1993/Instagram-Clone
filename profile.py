import os
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

from models import *


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
            allPosts.append(post.get())

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


        # fetching current user
        currentUser =  ndb.Key(urlsafe=(self.request.get('currentUser'))).get()

        # fetching the selectedUser
        selectedUser = ndb.Key(urlsafe=(self.request.get('selectedUser'))).get()


        # if the user wants to follow
        if self.request.get('button') == 'Follow':
            # adding the currentUser to selectedUser followers
            selectedUser.followers.append(currentUser.key)
            selectedUser.put()

            # adding selectedUser to currentUser Following
            currentUser.following.append(selectedUser.key)
            currentUser.put()

            self.redirect('/profile?key='+str(selectedUser.key.urlsafe()))


        # if the user wants to unfollow
        elif self.request.get('button') == 'Unfollow':

            # removing the currentUser from selectedUser
            selectedUser.followers.remove(currentUser.key)
            selectedUser.put()

            # removing selectedUser to currentUser Following
            currentUser.following.remove(selectedUser.key)
            currentUser.put()

            self.redirect('/profile?key='+str(selectedUser.key.urlsafe()))


        # if the user wants to add comment
        elif self.request.get('button') == 'Add Comment':
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

            self.redirect('/profile?key='+str(selectedUser.key.urlsafe()))
