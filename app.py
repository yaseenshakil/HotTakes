from flask import Flask, render_template;
# import cohere

app = Flask(__name__)

takes = [
    {
        "title": "Taylor Swift is lame", 
        "author": "ellie"
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

@app.route('/makeatake')
def makeatakeroute():
    # Need to add code to verify logged in users only
    return render_template("makeatake.html")

app.static_folder = "static"

# def call_cohere(take: str): 
#     cohere_prompt = f"""Respond with either Offensive or Non-Offensive on whether the following take is offensive. The take must not personally attack or offend any particular race, religion, sex, or demographic. 
#     The take is as follows: {take}"""
#     co = cohere.ClientV2("bJzEp6501sXBRHjZvJcb4yVRiaHUmANj7awo30ss")
#     response = co.chat(
#         model="command-a-03-2025",
#         messages=[{"role": "user", "content": cohere_prompt}]
#     )
#     print(response)
if __name__ == "__main__":
    app.run(port=8000,debug=True)
    # connect_to_openai()
    # call_cohere("Black history month is a scam")