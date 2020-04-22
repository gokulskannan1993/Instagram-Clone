import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers

from models import *
from datetime import datetime


# class to handle the uploads
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        # fetching current user
        user = users.get_current_user()
        currentUser = ndb.Key('User',user.user_id()).get()

        # fetching the file from the input
        upload = self.get_uploads()[0]
        blobinfo = blobstore.BlobInfo(upload.key())
        caption = self.request.get('caption')

        if self.request.get('button') == 'Post':
            # create a new Post object
            post = Post(
                caption = caption,
                image = upload.key(),
                date = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                user = currentUser.key
            )
            post.put()

            # adding the key of the post to user
            currentUser.posts.append(post.key)
            currentUser.put()
            self.redirect('/')
