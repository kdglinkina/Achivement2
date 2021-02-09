from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

Message = namedtuple('Message', 'number')
messages = []


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html', messages=messages)


@app.route('/add_number', methods=['POST'])
def add_message():
    x = request.form['calc']
    y = int(x) + 1
    messages.append(Message(y))
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run()
