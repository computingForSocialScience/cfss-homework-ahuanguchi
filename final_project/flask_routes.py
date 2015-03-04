from flask import Flask, render_template, request, redirect, g

app = Flask(__name__)

app.arg_to_title = {
    'durarara': "Durarara",
    'aldnoah': "Aldnoah Zero",
    'yona': "Yona of the Dawn",
    'death': "Death Parade",
    'rolling': "Rolling Girls",
    'sailor': "Sailor Moon Crystal",
    'yuri': "Yuri Kuma Arashi",
    'assassination': "Assassination Classroom",
    'gourmet': "Gourmet Girl Graffiti",
    'cute': "Cute High Earth Defense Club Love",
    'shirobako': "Shirobako"
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
    'sentiment': 'Average Sentiment (-1 to 1)',
    'time': 'Tweets Over Time',
    'place': 'Places'
}

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
    title1 = app.arg_to_title[show1]
    title2 = app.arg_to_title[show2]
    search_term1 = app.arg_to_query[show1]
    search_term2 = app.arg_to_query[show2]
    comp_full = app.comp_verbose[comparison]
    return render_template(
        'compare.html',
        title1=title1,
        title2=title2,
        comparison=comparison.title(),
        comp_full=comp_full
    )

if __name__ == '__main__':
    app.run(debug=True)
