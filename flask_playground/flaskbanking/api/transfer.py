import sys
import traceback
from flask import helpers
import flask
from db import dbinit
from model.globalbank import member
from model.piggybank import tummy

def transfer_api_view():
    try:
        if flask.request.method == 'POST':
            # TODO assertions / error handling
            req_data = flask.request.json
            # TODO Remove
            print 'Received: {}'.format(req_data)
            # {"from_account":"123456789","to_account":"Pink Piggy","amount":"3"}
            session_globalbank = dbinit.get_session(dbinit.DB_GLOBALBANK)
            from_member = session_globalbank.query(member.MemberBalance).filter_by(
                account=req_data['from_account']).first()
            session_piggybank = dbinit.get_session(dbinit.DB_PIGGYBANK)
            to_member = session_piggybank.query(tummy.TummyBalance).filter_by(
                which_piggy=req_data['to_account']).first()
            amount = int(req_data['amount'])
            if from_member.balance - amount < 0:
                raise Exception('Insufficient funds.')
            from_member.balance -= amount
            to_member.balance += amount

            session_globalbank.commit()
            # TODO put funds back in from acct if next commit fails
            session_piggybank.commit()
            return helpers.jsonify( {
                'status': 'success',
                'amount': amount,
                'from_account': from_member.account,
                'new_balances': {
                    from_member.account: from_member.balance,
                    to_member.which_piggy: to_member.balance
                }
            })
        else:
            raise Exception('GET not implemented. Use POST!')
    except Exception as ex:
        print 'ERROR: {} {} {}'.format(ex, sys.exc_info(), traceback.print_exc())
        raise





  