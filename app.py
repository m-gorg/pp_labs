from flask import Flask
from methods import api_blueprint

app = Flask(__name__)
app.register_blueprint(api_blueprint)


@app.route('/api/v1/hello-world-5')
def index():
    return "Hello World 5"


if __name__ == "__main__":
    app.run(debug=True)
