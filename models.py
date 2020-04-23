from google.appengine.ext import ndb

class User(ndb.Model):
    email = ndb.StringProperty()
    name = ndb.StringProperty()
    followers = ndb.KeyProperty(repeated=True)
    following = ndb.KeyProperty(repeated=True)
    posts = ndb.KeyProperty(repeated=True)


class Comment(ndb.Model):
    text = ndb.StringProperty()
    author = ndb.KeyProperty()


class Post(ndb.Model):
    caption = ndb.StringProperty()
    image = ndb.BlobKeyProperty()
    comments = ndb.StructuredProperty(Comment, repeated=True)
    date = ndb.StringProperty()
    user = ndb.KeyProperty()
