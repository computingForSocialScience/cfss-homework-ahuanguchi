from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index/')
def index():
    return redirect('/')

@app.route('/compare')
def compare():
    show1 = request.args['show1']
    show2 = request.args['show2']
    comparison = request.args['comparison']
    return '%s %s %s' % (show1, show2, comparison)

if __name__ == '__main__':
    app.run(debug=True)
