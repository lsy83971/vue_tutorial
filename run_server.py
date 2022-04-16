## 任务是建立单机版的调试器
## simple way
## 一切从简单 但是预留扩展空间

from flask import Flask
from flask import render_template_string, render_template
from flask import request
import json
from pyxmind.pyxmind import pyxmind



app = Flask(__name__, template_folder='./',static_folder="",static_url_path="/")

def init():
    return render_template("init.html")

def run():
    mind = pyxmind()
    data = json.loads(request.data)
    mind.from_elixir(data=data["data"])    
    mind.feed(data["xml"])
    return mind.result

def save():
    mind = pyxmind()
    data = json.loads(request.data)
    mind.from_elixir(data=data["data"])
    mind.save(filename=data["filename"])
    return "just soso"

def load():
    mind = pyxmind()
    data = json.loads(request.data)
    filename = data["filename"]
    mind.load(filename)
    return mind.to_elixir()

def test():
    return "test"


app.add_url_rule("/", "init", init, methods=["GET", "POST"])
app.add_url_rule("/run", "run", run, methods=["GET", "POST"])
app.add_url_rule("/save", "save", save, methods=["GET", "POST"])
app.add_url_rule("/load", "load", load, methods=["GET", "POST"])
app.add_url_rule("/test", "test", test, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5005, debug=True)
    #app.run(host="127.0.0.1", port=5005, debug=False)






## main post/get



## ajax post/get






