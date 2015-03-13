Alex's Twitter Content Explorer
===============================

Preparation
-----------

To make the database for my web app, I used Tweepy, JSON, and MySQL. I used 
the script in table_creation.sql to create/recreate tables as needed 
(usually to modify a VARCHAR field that wasn't long enough). Through 
Tweepy, I accessed the Twitter Search API, which returns tweets that match 
certain queries and data about them. To make my results as inclusive as 
possible, I included common alternate titles in my queries 
(e.g., '"yona of the dawn" OR "akatsuki no yona"'). I avoided exceeding the 
API's rate limit all at once by uncommenting different queries in 
twitter_api.py and running the script for each one. Each time, a new JSON file 
containing all of the information I wanted was made.

Once I was done collecting 
data, I used tweets_to_mysql.py to dump everything contained in all of the JSON 
files into my MySQL database. I made the script truncate the database's tables 
each time I did this because I kept changing the formats and/or kinds of data I 
was collecting for each tweet, which made old data unusable. 

The file useful_queries.sql just contains various SELECT statements I wrote to 
help me get a general grasp of the data I was collecting.


Web App Usage
-------------

Once the local MySQL server is running, flask_app.py allows you to go to
[http://localhost:5000](http://localhost:5000) to access the Twitter content explorer's home
page. From here, you can select two shows from a list of 11 currently
airing shows and a way to compare tweets about the two shows.
Pressing "Submit"sends a GET request with the URL parameters show1,
show2, and comparison and takes you to the resulting comparison page
(e.g., [http://localhost:5000/compare?show1=yona&show2=aldnoah&comparison=sentiment](http://localhost:5000/compare?show1=yona&show2=aldnoah&comparison=sentiment)).

On the backend, the application calls a function to query the database with the
search terms for the selected titles and returns data relevant to the selected
type of comparison. It then uses this data to make an appropriate Bokeh plot
and embeds it in the web page that you see. The page's template also
receives variables that allow it to show a table with a basic comparison of the
total number of tweets for each title and, for sentiment and time comparisons,
a table of the data that also appears in the Bokeh plot.

At the bottom of the page, you can click on "Go back" to retain the
same titles and select a different type of comparison or choose different
titles to compare.
