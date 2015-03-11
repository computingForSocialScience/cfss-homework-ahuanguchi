Alex's Twitter Content Explorer
===============================

Preparation
-----------

Web App Usage
-------------

Once the local MySQL server is running, flask_app.py allows visitors to go to
[link](http://localhost:5000) to access the Twitter content explorer's home
page. From here, visitors can select two shows from a list of 11 currently
airing shows and a way to compare tweets about the two shows (sentiment, time,
or place). Pressing "Submit" sends a get request with the URL parameters show1,
show2, and comparison and takes the visitor to the resulting comparison page
(e.g., [link](http://localhost:5000/compare?show1=yona&show2=aldnoah&comparison=sentiment)).
