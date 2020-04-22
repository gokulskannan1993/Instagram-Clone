import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers


class DownloadHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self):
        post = ndb.Key('Post', int(self.request.get('post'))).get()
        self.send_blob(post.image)
