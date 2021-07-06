from flask import Flask, render_template
app = Flask(__name__)

from subbot import routes

app.config['SECRET_KEY'] = '8cb90f8fea491d6444248698'

from subbot import functions

if __name__=='__main__':
    app.run(debug=True)