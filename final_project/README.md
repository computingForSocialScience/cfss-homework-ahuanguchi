Alex's Twitter Content Explorer
===============================

Preparation
-----------

To set up

Web App Usage
-------------

Once the local MySQL server is running, flask_app.py allows you to go to
[http://localhost:5000](http://localhost:5000) to access the Twitter content explorer's home
page. From here, you can select two shows from a list of 11 currently
airing shows and a way to compare tweets about the two shows (sentiment, time,
or place). Pressing "Submit" sends a GET request with the URL parameters show1,
show2, and comparison and takes you to the resulting comparison page
(e.g., [http://localhost:5000/compare?show1=yona&show2=aldnoah&comparison=sentiment](http://localhost:5000/compare?show1=yona&show2=aldnoah&comparison=sentiment)).

On the backend, the application calls a function to query the database with the
search terms for the selected titles and returns data relevant to the selected
type of comparison. It then uses this data to make an appropriate Bokeh plot
and embeds it in the webpage that you see. The page's template also
receives variables that allow it to show a table with a basic comparison of the
total number of tweets for each title and, for sentiment and time comparisons,
a table of the data that also appears in the Bokeh plot.

At the bottom of the page, you can click on "Go back" to retain the
same titles and select a different type of comparison or choose different
titles to compare.
