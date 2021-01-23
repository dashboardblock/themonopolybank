"""
The Monopoly Bank
"""
from flask import Flask, request, render_template
from algo_handler import create_account, fund_transaction

application = Flask(__name__)


@application.route("/")
def start():
    """ Start page """
    return render_template('index.html')


@application.route('/new/')
def new():
    """ New account """
    return render_template('new.html')


@application.route('/create/', methods=['POST', 'GET'])
def create():
    """ Create new account """
    if request.method == 'POST':
        role = request.form.get('role')
        qr_file, message = create_account(role)
        return render_template('create.html', qr_file=qr_file, message=message)
    return render_template('create.html')


@application.route('/deposit/', methods=['POST', 'GET'])
def deposit():
    """deposit"""
    message = ''
    error = ''
    if request.method == 'POST':
        send_to_address = request.form.get('wallet')
        role = request.form.get('role')
        message, error = fund_transaction(send_to_address, role)
    return render_template('deposit.html', message=message, error=error)


@application.route('/refund/')
def refund():
    """refund"""
    return render_template('refund.html')


@application.route('/about/')
def about():
    """about"""
    return render_template('about.html')


if __name__ == "__main__":
    application.run(host='127.0.0.1', debug=True)
