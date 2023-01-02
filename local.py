import robot_basics as rb
from flask import Flask, render_template, redirect, url_for, make_response
import socket


# get server ip
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
server_ip = s.getsockname()[0]
s.close()


# create a Flask web server from the Flask module (__name__ = this file)
app = Flask(__name__)


@app.route('/')
def webui():
    return render_template('local.php', server_ip=server_ip)


@app.route('/<instruction>', methods=['POST'])
def reroute(instruction):

    command = int(instruction)

    if command == 1:
        rb.Left()
    elif command == 2:
        rb.Forwards()
    elif command == 3:
        rb.Right()
    elif command == 4:
        rb.Backwards()
    elif command == 5:
        rb.StopMotors()
    elif command == 6:
        rb.Low()
    elif command == 7:
        rb.Medium()
    elif command == 8:
        rb.High()
    else:
        print("Wrong command")
    response = make_response(redirect(url_for('webui')))
    return(response)


app.run(debug=True, host='0.0.0.0', port=8000)
