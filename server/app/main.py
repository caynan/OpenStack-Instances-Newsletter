import instance_terminator
from flask import Flask



app = Flask(__name__)

@app.route("/instances/delete/<key>")
def instance_delete(key):
    return "Deleted: " + key


if __name__ == "__main__":
    app.run(debug=True)
