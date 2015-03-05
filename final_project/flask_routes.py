from flask import Flask, render_template, request, redirect, g
import pymysql

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
        'Tweets on 2015-02-23',
        '02-24',
        '02-25',
        '02-26',
        '02-27',
        '02-28',
        '03-01',
        '03-02',
        '03-03'
    ),
    'place': ('Tweet Locations',)
}

def query_database(comparison, search_term1, search_term2):
    query = None
    if comparison == 'basic':
        g.c.execute("SELECT COUNT(*) FROM tweets;")
        total = g.c.fetchone()[0]
        query = "SELECT COUNT(*), (COUNT(*) / %s) " \
                "FROM tweets " \
                "WHERE search_term = %s;"
        g.c.execute(query, (total, search_term1))
        data1 = g.c.fetchone()
        g.c.execute(query, (total, search_term2))
        data2 = g.c.fetchone()
    else:
        if comparison == 'sentiment':
            query = "SELECT AVG(sentiment) " \
                    "FROM tweets " \
                    "WHERE search_term = %s;"
        elif comparison == 'time':
            query = "SELECT COUNT(*) " \
                    "FROM tweets " \
                    "WHERE search_term = %s " \
                    "GROUP BY DATE(created_at);"
        elif comparison == 'space':
            pass
        if query:
            g.c.execute(query, (search_term1,))
            data1 = tuple(x[0] for x in g.c.fetchall())
            g.c.execute(query, (search_term2,))
            data2 = tuple(x[0] for x in g.c.fetchall())
    if not query:
        data1 = ('',)
        data2 = ('',)
    return data1, data2

def plot_data(comparison, search_term1, search_term2, labels1, labels2, data1, data2):
    pass

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
    comp_full = app.comp_verbose[comparison]
    
    data1, data2 = query_database(comparison, search_term1, search_term2)
    basic1, basic2 = query_database('basic', search_term1, search_term2)
    
    return render_template(
        'compare.html',
        title1=title1,
        title2=title2,
        comparison='by ' + comparison.title() if comparison != 'basic' else '',
        comp_full=comp_full,
        data1=data1,
        data2=data2,
        basic1=basic1,
        basic2=basic2
    )

if __name__ == '__main__':
    app.run(debug=True)
