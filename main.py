#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2

from google.appengine.ext import db     #import database funtions

#Link template directory and autoescape
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
autoescape = True)

class Handler(webapp2.RequestHandler):
#base handler that others inherit from.
    def write(self, *arguments, **keywords):        #shortens the .write method for use elsewhere
        self.response.write(*arguments, **keywords)

    def render_str(self, template, **parameters):   #builds a string to render
        t = jinja_env.get_template(template)
        return t.render(parameters)

    def render(self, template, **keywords):         #shortens the render method for use elsewhere
        self.write(self.render_str(template, **keywords))

class Post(db.Model):
#build database where each instance is an entity is a blog post with 3 properties
    title = db.StringProperty(required = True)
    post_body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)  #Print this with posts?

class CreateNewPost(Handler):    #renders post creation page
    def render_front(self, title="", post_body="", error=""):
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created DESC ")
    #retrieves entity and assigns to "posts"

        self.render("post-creation.html", title=title, post_body=post_body, error=error, posts=posts)
        #renders post-creation page using .render, info from 'posts' and template

    def get(self):
        self.render_front()
        #get request calls render_front above

    def post(self):
        title = self.request.get("title")
        post_body = self.request.get("post_body")
    #retrieve title and post_body from ??????

        if title and post_body:
            a = Post(title = title, post_body = post_body)
            a.put()
        #if title and post_body are present, update db

            self.redirect("/")
        #rerender the page

        else:
            error = "We need both a title and a post!"
            self.render_front(title, post_body, error)
        #if both not present then rerender the page with input & error message

class MainBlog(Handler):
#takes /blog requests

    def get(self):
        title = self.request.get("title")
        post_body = self.request.get("post_body")
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created DESC "
                            "LIMIT 5")

        self.render("main-blog.html", title = title, post_body = post_body, posts = posts)
    #renders page with 5 newest blogs

class ViewSinglePost(Handler):
    """This page displays a single blog post when the link is clicked
    or a new post is created"""
    #def get(self, posts): #unfinished

app = webapp2.WSGIApplication([
    ('/', MainBlog),
    ('/create-new', CreateNewPost),
    ('/view-post ', ViewSinglePost)
    ], debug=True)
