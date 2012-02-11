from flask.templating import render_template

# Avoid Flask app circular includes. See add_url_rule
#@app.route('/')
from db import dbinit
from model.globalbank import member
from model.piggybank import tummy

def get_from_account_balances():
    member_balances = dbinit.get_session(dbinit.DB_GLOBALBANK).query(member.MemberBalance).all()
    return [(m.account, m.balance) for m in member_balances]

def get_to_accounts():
    return [x.which_piggy for x in dbinit.get_session(dbinit.DB_PIGGYBANK).query(tummy.TummyBalance).all()]

def transfer_view():
    account_balances = get_from_account_balances()
    context = {
        'bank_name': 'Global Bank',
        'account_balances': account_balances,
        'from_accounts': [a[0] for a in account_balances],
        'to_accounts': get_to_accounts()
    }
    return render_template('transfer.html', **context)

  