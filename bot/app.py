from flask import Flask, url_for, redirect, render_template, request, abort,flash,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
from config import Config



app = Flask(__name__)
app.config.from_pyfile('config.py')    
db = SQLAlchemy(app)
Base=automap_base()
Base.prepare(db.engine,reflect=True)

Users=Base.classes.user
IP=Base.classes.ip


@app.route('/<chat_id>')
def get_ip(chat_id):
    ipaddr=request.headers['X-Real-IP'].split(',')[0]
    exists = db.session.query(db.exists().where(IP.ip == ipaddr)).scalar()
    if not exists:
        ip=IP(chat_id=int(chat_id),ip=ipaddr)
        db.session.add(ip)
        db.session.commit()
    else:
        getchat=db.session.query(IP).filter_by(ip==ipaddr).first()
        getuser=db.session.query(Users).filter_by(chat_id==chat_id).first()
        db.session.query(Users).filter_by(chat_id==chat_id).update(dict(is_multiple_account=True))
        db.session.commit()
        if getuser.refferd_by is None:
            pass
        else:
            refuser=db.session.query(Users).filter_by(chat_id==getuser.refferd_by).first()
            db.session.query(Users).filter_by(chat_id==getuser.refferd_by).update(dict(balance=refuser.balance-100))
            db.session.commit()
    return redirect(f"https://t.me/{Config.BOT_USERNAME}")