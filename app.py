from flask import Flask, render_template;

app = Flask(__name__)

takes = [
    {
        "title": "Hotdogs are a taco", 
        "author": "yaseenshakil"
    }, 
    {
        "title": "Golf isn't a real sport", 
        "author": "the anti golf association"
    }, 
    {
        "title": "Friends is highly overrated",
        "author": "everyone"
    },
    {
        "title": "Crunchy peanut butter over creamy peanut butter",
        "author": "reception lady"
    }, 
    {
        "title": "Ball-point pens are much better than fountain pens", 
        "author": "all pen users"
    }
]

@app.route('/')
def home_page():
    return render_template("index.html", takes=takes)

@app.route('/signup')
def signup():
    return render_template("signup.html")

app.static_folder = "static"

if __name__ == "__main__":
    app.run(debug=True)