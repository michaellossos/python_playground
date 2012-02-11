from flask import Flask
import views.transfer
import api.transfer

app = Flask(__name__)

app.add_url_rule('/', 'transfer_main_page', view_func=views.transfer.transfer_view)
app.add_url_rule('/api/v1/transfer/', 'api_transfer', view_func=api.transfer.transfer_api_view, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)