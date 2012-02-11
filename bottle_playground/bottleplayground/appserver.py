import bottle
from mako import lookup
from mako import template
import os

@bottle.route('/')
def index():
    template_dir = os.path.abspath(os.path.dirname(__file__)  + '/templates')
    template_lookup = lookup.TemplateLookup(directories=[template_dir])
    t = template.Template(filename=template_dir + '/transfer.html', lookup=template_lookup)

    account_balances = [('0123456', 388), ('98764', 42), ('55454', 500), ('88888', 8008)]
    data = {
        'bank_name': 'Global Bank',
        'account_balances': account_balances,
        'from_accounts': [x[0] for x in account_balances[0:2]],
        'to_accounts': [x[0] for x in account_balances[2:]],
    }
    return t.render(**data)

bottle.debug(True)
bottle.run(host='localhost', port=8080)
