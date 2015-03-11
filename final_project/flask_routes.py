from flask import Flask, render_template, request, redirect, g
import pymysql, numpy as np
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.resources import CDN
from bokeh.embed import components
from collections import OrderedDict

app = Flask(__name__)

app.arg_to_title = {
    'durarara': 'Durarara',
    'aldnoah': 'Aldnoah Zero',
    'yona': 'Yona of the Dawn',
    'death': 'Death Parade',
    'rolling': 'Rolling Girls',
    'sailor': 'Sailor Moon Crystal',
    'yuri': 'Yuri Kuma Arashi',
    'assassination': 'Assassination Classroom',
    'gourmet': 'Gourmet Girl Graffiti',
    'cute': 'Cute High Earth Defense Club Love',
    'shirobako': 'Shirobako'
}
app.arg_to_query = {
    'durarara': 'durarara',
    'aldnoah': 'aldnoah zero',
    'yona': '"yona of the dawn" OR "akatsuki no yona"',
    'death': '"death parade"',
    'rolling': '"rolling girls"',
    'sailor': '"sailor moon crystal"',
    'yuri': 'yuri kuma arashi',
    'assassination': '"assassination classroom" OR "ansatsu kyoushitsu"',
    'gourmet': '"gourmet girl graffiti" OR "koufuku graffiti"',
    'cute': 'cute high earth defense club love',
    'shirobako': 'shirobako'
}
app.comp_verbose = {
    'sentiment': ('Average Sentiment (-1 to 1)',),
    'time': (
        '2015-02-23 (Mon)',
        '02-24 (Tue)',
        '02-25 (Wed)',
        '02-26 (Thu)',
        '02-27 (Fri)',
        '02-28 (Sat)',
        '03-01 (Sun)',
        '03-02 (Mon)',
        '03-03 (Tue)'
    ),
}

@app.before_request
def before_request():
    g.db = pymysql.connect(user='root', database='cfss', charset='utf8mb4')
    g.c = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    c = getattr(g, 'c', None)
    db = getattr(g, 'db', None)
    if c:
        c.close()
    if db:
        db.close()

def query_database(comparison, search_term1, search_term2):
    query = None
    if comparison == 'basic':
        g.c.execute("SELECT COUNT(*) FROM tweets;")
        total = g.c.fetchone()[0]
        query = """
            SELECT COUNT(*), (COUNT(*) / %s)
            FROM tweets
            WHERE search_term = %s;
        """
        g.c.execute(query, (total, search_term1))
        data1 = g.c.fetchone()
        g.c.execute(query, (total, search_term2))
        data2 = g.c.fetchone()
    elif comparison == 'place':
        query = """
            SELECT t1.place, COALESCE(t2.num, 0), COALESCE(t3.num, 0)
            FROM (
                (
                    SELECT place FROM tweets
                    WHERE search_term IN (%s, %s)
                    GROUP BY place
                ) AS t1
                LEFT OUTER JOIN (
                    SELECT place, COUNT(*) AS num FROM tweets
                    WHERE search_term = %s
                    GROUP BY place
                ) AS t2
                ON t1.place = t2.place
                LEFT OUTER JOIN (
                    SELECT place, COUNT(*) AS num FROM tweets
                    WHERE search_term = %s
                    GROUP BY place
                ) AS t3
                ON t1.place = t3.place
            );
        """
        g.c.execute(
            query,
            (search_term1, search_term2, search_term1, search_term2)
        )
        all_rows = g.c.fetchall()[1:]           # skip first row, where place is "NULL"
        locations, data1, data2 = tuple(zip(*all_rows))
    else:
        if comparison == 'sentiment':
            query = """
                SELECT AVG(sentiment)
                FROM tweets
                WHERE search_term = %s;
            """
        elif comparison == 'time':
            query = """
                SELECT COUNT(*)
                FROM tweets
                WHERE search_term = %s
                GROUP BY DATE(created_at);
            """
        else:
            pass
        if query:
            g.c.execute(query, (search_term1,))
            data1 = tuple(x[0] for x in g.c.fetchall())
            g.c.execute(query, (search_term2,))
            data2 = tuple(x[0] for x in g.c.fetchall())
    if not query:
        data1 = ('',)
        data2 = ('',)
    if comparison != 'place':
        return data1, data2
    else:
        return data1, data2, locations

def plot_data(comparison, title1, title2, data1, data2, comp_full):
    if comparison == 'sentiment':
        bar_chart = Bar(
            [float(data1[0]), float(data2[0])], [title1, title2],
            xlabel='Show', ylabel='Average Sentiment (-1 to 1)',
            tools='resize,reset,save,crosshair'
        )
        fig_js, fig_div = components(bar_chart, CDN)
    elif comparison == 'time':
        x_vals = list(comp_full[:-1])
        p = figure(
            title='', x_range=x_vals, x_axis_label='Day',
            y_axis_label='Number of Tweets',
            tools='resize,reset,save,crosshair'
        )
        p.line(x_vals, data1[:-1], legend=title1, line_color='red')
        p.line(x_vals, data2[:-1], legend=title2)
        p.legend.orientation = "top_left"
        p.xaxis.major_label_orientation = np.pi / 3
        fig_js, fig_div = components(p, CDN)
    elif comparison == 'place':
        locations = list(reversed(comp_full))               # put places in alphabetical order from top to bottom
        locations_data1 = [l + ':0.4' for l in locations]
        locations_data2 = [l + ':0.6' for l in locations]
        counts1 = np.array(tuple(reversed(data1)), dtype=np.float)      # put data in the same order
        counts2 = np.array(tuple(reversed(data2)), dtype=np.float)
        p = figure(
            title='', y_range=locations, y_axis_label='Place',
            x_axis_label='Number of Tweets',
            x_range=[0, max((counts1.max(), counts2.max())) + 1],
            plot_width=1000, plot_height=600,
            tools='resize,reset,save,crosshair'
        )
        p.rect(
            y=locations_data1, x=counts1 / 2, height=0.2,
            width=counts1, color='red', alpha=0.5, legend=title1
        )
        p.rect(
            y=locations_data2, x=counts2 / 2, height=0.2,
            width=counts2, color='blue', alpha=0.5, legend=title2
        )
        p.xgrid.grid_line_color = None
        fig_js, fig_div = components(p, CDN)
    else:
        fig_js, fig_div = '', ''
    return fig_js, fig_div

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index/')
def index():
    return redirect('/')

# urls appear as "/compare?show1=yona&show2=aldnoah&comparison=sentiment", etc.
@app.route('/compare')
def compare():
    show1 = request.args['show1']
    show2 = request.args['show2']
    comparison = request.args['comparison']
    
    search_term1 = app.arg_to_query[show1]      # This also completely prevents unwanted SQL queries
    search_term2 = app.arg_to_query[show2]      # in addition to pymysql's execute function sanitizing arguments.
    title1 = app.arg_to_title[show1]
    title2 = app.arg_to_title[show2]
    
    if comparison != 'place':
        comp_full = app.comp_verbose[comparison]
        data1, data2 = query_database(comparison, search_term1, search_term2)
    else:
        data1, data2, comp_full = query_database(comparison, search_term1, search_term2)
    basic1, basic2 = query_database('basic', search_term1, search_term2)
    
    fig_js, fig_div = plot_data(comparison, title1, title2, data1, data2, comp_full)
    
    return render_template(
        'compare.html',
        title1=title1,
        title2=title2,
        comparison='by ' + comparison.title(),
        comp_full=comp_full,
        data1=data1,
        data2=data2,
        basic1=basic1,
        basic2=basic2,
        fig_js=fig_js,
        fig_div=fig_div
    )

if __name__ == '__main__':
    app.run(debug=True)
