#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)

# Home
@app.route('/')
def home():
    return render_template("home.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)