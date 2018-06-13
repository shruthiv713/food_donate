import sqlite3
import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds
from datetime import datetime
from flask import Flask ,render_template,request
from flask import session, redirect, url_for, escape
import smtplib
from email.mime.text import MIMEText
smtp_ssl_host = 'smtp.gmail.com' # smtp.mail.yahoo.com
smtp_ssl_port = 465
username = 'donatefood4'
password = '@donatefood4'
sender = 'donatefood4@gmail.com'

app = Flask(__name__)
app.secret_key = "any random string"
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
@app.route('/')
def mainfun():
    return render_template('index.html')

@app.route('/log')
def log():
    return render_template('Login.html')


@app.route('/signup')
def signup():
    return render_template('Signup.html')

@app.route('/forgot')
def forgot():
	if session.get('mail') == True:
		return render_template('ForgotPassword.html')

@app.route('/seemail', methods=['POST', 'GET'])
def seemail():
    if request.method == 'POST':
        try:
            mail = request.form['mail']
            category = request.form['category']
            with sqlite3.connect("acms.db") as con:
                cur = con.cursor()
                if category == 'hotel':
                    cur.execute("SELECT HotelPassword from Hotel WHERE HotelMail='{}'".format(mail))
                    hp = cur.fetchone();
                    targets = [mail]
                    msg = MIMEText('Your Food Donate Password Is:'+ hp[0])
                    msg['Subject'] = 'Your Food Donate Password'
                    msg['From'] = sender
                    msg['To'] = ', '.join(targets)
					
                    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
                    server.login(username, password)
                    server.sendmail(sender, targets, msg.as_string())
                    server.quit()
                    msgDeatils = "Please Check Your Mail For The Password"
                if category == 'orphanage':
                    cur.execute("SELECT CharityPassword from Charity WHERE CharityMail='{}'".format(mail))
                    hp = cur.fetchone();
                    targets = [mail]
                    msg = MIMEText('Your Food Donate Password Is:'+ hp[0])
                    msg['Subject'] = 'Your Food Donate Password'
                    msg['From'] = sender
                    msg['To'] = ', '.join(targets)
                    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
                    server.login(username, password)
                    server.sendmail(sender, targets, msg.as_string())
                    server.quit()
                    msgDeatils = "Please Check Your Mail For The Password"
                con.commit()
        except:
            msgDeatils = "Email Does not exists in the database "
            con.rollback()
        finally:
            return render_template("ForgotPasswordSuccess.html",msgDeatils=msgDeatils)
            con.close()


@app.route('/addentry', methods=['POST', 'GET'])
def addentry():
    if request.method == 'POST':
        try:
            name = request.form['name']
            mob = request.form['mob']
            address = request.form['address']
            mail=request.form['mail']
            psw = request.form['psw']
            category = request.form['category']

            with sqlite3.connect("acms.db") as con:
                cur = con.cursor()
                if category == 'hotel':
                    cur.execute("INSERT INTO Hotel (HotelName ,HotelPhone ,HotelMail ,HotelPassword ,HotelAddress)VALUES(?, ?, ?, ? ,?)",(name,mob,mail,psw,address) )
                    #msgDeatils = "Hotel Added successfully"
                    con.commit()
                    return redirect(url_for('log'))
                if category == 'orphanage':
                    cur.execute("INSERT INTO Charity (CharityName ,CharityPhone ,CharityMail ,CharityPassword ,CharityAddress)VALUES(?, ?, ?, ? ,?)",(name,mob,mail,psw,address) )
                    #msgDeatils = "Charity Added successfully"
                    con.commit()
                    return redirect(url_for('log'))


        except:
            msgDeatils = "Insertion Failed Please check the query / db "
            con.rollback()
            return render_template("result.html", msgDeatils=msgDeatils)
            con.close()
        #finally:



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            mail = request.form['mail']
            psw = request.form['psw']
            category = request.form['category']

            with sqlite3.connect("acms.db") as con:
                cur = con.cursor()
                if category=='hotel':
                    cur.execute("SELECT HotelPassword from Hotel WHERE HotelMail='{}'".format(mail))
                    hp= cur.fetchone();

                    if hp[0]==psw:
                        session['mail']=mail
                        #msgDeatils = "Hotel logged successfully"
                        return redirect(url_for('hotel'))
                    else:
                        msgDeatils = "Hotel Password incorrect"
                        return render_template("result.html", msgDeatils=msgDeatils)
                if category == 'orphanage':
                    cur.execute("SELECT CharityPassword from Charity WHERE CharityMail='{}'".format(mail))
                    hp = cur.fetchone();

                    if hp[0] == psw:
                        session['mail'] = mail
                        #msgDeatils = "Charity logged successfully"
                        return redirect(url_for('charity'))
                    else:
                        msgDeatils = "Charity Password incorrect"
                        return render_template("result.html", msgDeatils=msgDeatils)


                con.commit()
        except:
            msgDeatils = "Incorrect email "
            con.rollback()
            return render_template("result.html", msgDeatils=msgDeatils)
            con.close()
        #finally:
            #return render_template("result.html",msgDeatils=msgDeatils)
            #con.close()


@app.route('/hotel')
def hotel():
	if  session.get('mail')==None:
		return render_template('Login.html')
	
	con = sqlite3.connect("acms.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	mail=session['mail']
    #print(mail)
	cur.execute("select HotelID from Hotel WHERE HotelMail='{}'".format(mail))
	id = cur.fetchone();
	cur.execute("select AvailID,AvailPeople,AvailDT,ExpTime,AvailLeftOut from Availability WHERE HotelID='{}'".format(id[0]))
	availrows = cur.fetchall();
	return render_template("HotelHome.html", rows=availrows)


@app.route('/hoteladd')
def hoteladd():
	if  session.get('mail')==None:
		return render_template('Login.html')
	else:
		return render_template('HotelAdd.html')

@app.route('/hoteladdentry', methods=['POST', 'GET'])
def hoteladdentry():
	if  session.get('mail')==None:
		return render_template('Login.html')
	
	if request.method == 'POST':
		
		count = request.form['count']
		hour = request.form.get('hour')
		minutes=request.form.get('minutes')
		date2 = request.form['date']
		date2=str(date2)
		mail = session['mail']
		date2+=" "+str(hour)+":"+str(minutes)+":00"
		date=datetime.strptime(date2,"%Y-%m-%d %H:%M:%S")
            #print(count)
            #print(date)
            #print(mail)
            #print(mail)
		con = sqlite3.connect("acms.db")
		con.row_factory = sqlite3.Row
		cur = con.cursor()
		cur.execute("select HotelID from Hotel WHERE HotelMail='{}'".format(mail))
		id = cur.fetchone();
            #print(id[0])
		con.close()

		try:
			with sqlite3.connect("acms.db") as con:
				cur = con.cursor()
				cur.execute("INSERT INTO Availability (HotelID ,AvailPeople ,ExpTime,AvailLeftOut)VALUES(?, ?, ?, ?)",(id[0],count,date,count))

                #msgDeatils = "Employee Added successfully"
				con.commit()
                #print("added")
				
				if 'mail' in session:
					return redirect(url_for('hotel'))
				else :
					return redirect(url_for('login'))

		except:
			msgDeatils = "Insertion Failed Please check the query / db "
			con.rollback()
			if  session.get('mail')==None:
				return render_template('Login.html')
			else:
				return render_template("result1.html", msgDeatils=msgDeatils)
			con.close()
        #finally:


@app.route('/hoteldelete')
def hoteldelete():
    if  session.get('mail')==None:
	    return render_template('Login.html')
    con = sqlite3.connect("acms.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    mail = session['mail']
    #print(mail)
    cur.execute("select HotelID from Hotel WHERE HotelMail='{}'".format(mail))
    id = cur.fetchone();
    cur.execute("select AvailID,AvailPeople,AvailDT,ExpTime from Availability WHERE HotelID='{}' and AvailID not in (select AvailID from OrderPlaced)".format(id[0]))
    availrows = cur.fetchall();

    return render_template('HotelDelete.html', rows=availrows)

@app.route('/hoteldeleteentry', methods=['POST', 'GET'])
def hoteldeleteentry():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    if request.method == 'POST':
        #print("hello")
        #print("**")
        try:
            #print("hey")
            number = request.form.getlist("Availid")
            # print(number[0])
            # return number[0]

            with sqlite3.connect("acms.db") as con:
                cur = con.cursor()
                #print("connection done")
                for i in number:
                    #print(i);
                    cur.execute("DELETE FROM Availability Where AvailID='{}'".format(i))
                    #msgDeatils = "Employee deleted successfully"
                    con.commit()
                return redirect(url_for('hotel'))
        except:
            msgDeatils = "Deletion Failed Please check the query / db "
            con.rollback()
            return render_template("result1.html", msgDeatils=msgDeatils)
            con.close()
        #finally:


@app.route('/hotelmodify')
def hotelmodify():

    if  session.get('mail')==None:
	    return render_template('Login.html')    
    con = sqlite3.connect("acms.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    mail = session['mail']
    #print(mail)
    cur.execute("select HotelID from Hotel WHERE HotelMail='{}'".format(mail))
    id = cur.fetchone();
    cur.execute("select AvailID,AvailPeople,AvailDT,ExpTime from Availability WHERE HotelID='{}' and AvailID not in (select AvailID from OrderPlaced)".format(id[0]))
    availrows = cur.fetchall();

    return render_template('HotelModify.html', rows=availrows)

#hotelmodifyrender
@app.route('/hotelmodifyrender<data>')
def hotelmodifyrender(data):
    if  session.get('mail')==None:
        return render_template('Login.html')
    try:
        #aid = request.form['Availid']
        with sqlite3.connect("acms.db") as con:
            cur = con.cursor()
            cur.execute("select AvailID,AvailPeople,AvailDT,ExpTime from Availability WHERE AvailID='{}'".format(data))
            id,people,dt,et= cur.fetchone();
            #p=str(people)
            return render_template('HotelModifyForm.html', id=id,people=people,dt=dt,et=et)
            con.commit()

    except:
        msgDeatils = "Selection Failed Please check the query / db "
        con.rollback()
        return render_template("result1.html", msgDeatils=msgDeatils)
        con.close()
    #finally:



@app.route('/hotelmodifyentry', methods=['POST', 'GET'])
def hotelmodifyentry():

    if  session.get('mail')==None:
        return render_template('Login.html')
    if request.method == 'POST':
        try:
            id = request.form['Availid']
            count = request.form['count']
            date = request.form['date']
            #print(id)
            #print(count.type)
            #print(date)

            with sqlite3.connect("acms.db") as con:
                cur = con.cursor()
                cur.execute('''UPDATE Availability SET AvailPeople = ? , ExpTime = ? , AvailLeftOut = ? WHERE AvailID = ?''', (count, date, count, id))
                #print("updated the table")
                con.commit()
                return redirect(url_for('hotel'))
        except:
            msgDeatils = "Update Failed Please check the query / db "
            con.rollback()
            return render_template("result1.html", msgDeatils=msgDeatils)
            con.close()
        #finally:


@app.route('/hoteledit')
def hoteledit():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    con = sqlite3.connect("acms.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    mail = session['mail']
    #print(mail)
    cur.execute("select * from Hotel WHERE HotelMail='{}'".format(mail))
    row = cur.fetchone();
    return render_template('HotelEdit.html', row=row)


@app.route('/hoteleditentry', methods=['POST', 'GET'])
def hoteleditentry():
    if  session.get('mail')==None:
	    return render_template('Login.html')
    if request.method == 'POST':
        try:
            id = request.form['id']
            name = request.form['name']
            mail = request.form['mail']
            mob = request.form['mob']
            passw = request.form['pass']
            addr = request.form['addr']
            #print(id)


            with sqlite3.connect("acms.db") as con:
                cur = con.cursor()
                cur.execute('''UPDATE Hotel SET HotelName = ? , HotelMail = ? , HotelPhone = ? , HotelPassword = ? , HotelAddress = ? WHERE HotelID = ?''', (name, mail, mob, passw, addr, id))
                #print("updated the table")
                con.commit()
                session['mail']=mail
                return redirect(url_for('hotel'))
        except:
            msgDeatils = "Update Failed Please check the query / db "
            con.rollback()
            return render_template("result1.html", msgDeatils=msgDeatils)
            con.close()
        #finally:



@app.route('/logout')
def logout():
    session.pop('mail', None)
    return render_template('index.html')


@app.route('/charity')
def charity():

    if  session.get('mail')==None:
	    return render_template('Login.html')    
    con = sqlite3.connect("acms.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    mail=session['mail']
    #print(mail)
    cur.execute("select CharityID from Charity WHERE CharityMail='{}'".format(mail))
    id = cur.fetchone();
    cur.execute("select OrderID,People,OrderTime,HotelName,Hotel.HotelID,CharityID,ExpTime from Hotel natural join (OrderPlaced natural join Availability) WHERE CharityID='{}'".format(id[0]))
    orderrows = cur.fetchall();
    #print(orderrows[0]["Hotel.HotelID"])
    return render_template("CharityHome.html", rows=orderrows)


@app.route('/charitymore<hid>')
def charitymore(hid):

    if  session.get('mail')==None:
	    return render_template('Login.html')
    try:
        con = sqlite3.connect("acms.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        mail = session['mail']
        #print(mail)
        cur.execute("select CharityID from Charity WHERE CharityMail='{}'".format(mail))
        cid = cur.fetchone();
        #print(hid)
        #print(cid[0])
        con.close()
        with sqlite3.connect("acms.db") as con:
            cur = con.cursor()
            cur.execute("select HotelName,HotelPhone,HotelMail,HotelAddress from Hotel WHERE HotelID='{}'".format(hid))
            HotelName, HotelPhone, HotelMail, HotelAddress= cur.fetchone();
            #print(HotelName)
            cur.execute("select CharityAddress from Charity WHERE CharityID='{}'".format(cid[0]))
            CharityAddress = cur.fetchone();
            #print(CharityAddress)
            return render_template('CharityMore.html', HotelName=HotelName, HotelPhone=HotelPhone, HotelMail=HotelMail, HotelAddress=HotelAddress, CharityAddress=CharityAddress)
            con.commit()

    except:
        msgDeatils = "Selection Failed Please check the query / db "
        con.rollback()
        return render_template("result1.html", msgDeatils=msgDeatils)
        con.close()
    #finally:


@app.route('/charityedit')
def charityedit():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    con = sqlite3.connect("acms.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    mail = session['mail']
    #print(mail)
    cur.execute("select * from Charity WHERE CharityMail='{}'".format(mail))
    row = cur.fetchone();
    con.close()
    return render_template('CharityEdit.html', row=row)



@app.route('/charityeditentry', methods=['POST', 'GET'])
def charityeditentry():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    if request.method == 'POST':
        try:
            id = request.form['id']
            name = request.form['name']
            mail = request.form['mail']
            mob = request.form['mob']
            passw = request.form['pass']
            addr = request.form['addr']
            #print(id)


            with sqlite3.connect("acms.db") as con:
                cur = con.cursor()
                cur.execute('''UPDATE Charity SET CharityName = ? , CharityMail = ? , CharityPhone = ? , CharityPassword = ? , CharityAddress = ? WHERE CharityID = ?''', (name, mail, mob, passw, addr, id))
                con.commit()
                #print("updated the table")
                session['mail']=mail
                return redirect(url_for('charity'))
        except:
            msgDeatils = "Update Failed Please check the query / db "
            #con.rollback()
            return render_template("result1.html", msgDeatils=msgDeatils)
            con.close()
        #finally:



@app.route('/charityfeedback')
def charityfeedback():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    con = sqlite3.connect("acms.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    mail=session['mail']
    #print(mail)
    cur.execute("select CharityID from Charity WHERE CharityMail='{}'".format(mail))
    id = cur.fetchone();
    cur.execute("select OrderID,People,OrderTime,HotelName,ExpTime from Hotel natural join (OrderPlaced natural join Availability) WHERE CharityID='{}' and Remaining is null".format(id[0]))
    orderrows = cur.fetchall();
    #print(orderrows[0]["Hotel.HotelID"])
    return render_template("CharityFeedback.html", rows=orderrows)



@app.route('/charityfeedbackrender<oid>')
def charityfeedbackrender(oid):

    if  session.get('mail')==None:
	    return render_template('Login.html')
    return render_template('CharityFeedbackForm.html', oid=oid)



@app.route('/charityfeedbackentry', methods=['POST', 'GET'])
def charityfeedbackentry():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    if request.method == 'POST':
        try:
            oid = request.form['oid']
            count = request.form['count']
            rate = request.form['rate']
            #print(oid)
            #print(count)
            #print(rate)

            with sqlite3.connect("acms.db") as con:
                cur = con.cursor()
                cur.execute('''UPDATE OrderPlaced SET Remaining = ? , Rating = ?   WHERE OrderID = ?''', (count, rate, oid))
                con.commit()
                #print("updated the table")

                return redirect(url_for('charity'))
        except:
            msgDeatils = "Update Failed Please check the query / db "
            #con.rollback()
            return render_template("result1.html", msgDeatils=msgDeatils)
            con.close()
        #finally:



@app.route('/charityfind')
def charityfind():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    con = sqlite3.connect("acms.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select HotelName,AvailLeftOut,ExpTime,AvailID,Hotel.HotelID from  Availability natural join Hotel where AvailLeftOut > 0 and ExpTime > datetime('now','localtime')")
    orderrows = cur.fetchall();
    #print(orderrows[0]["Hotel.HotelID"])
    return render_template("CharityFindHotel.html", rows=orderrows)


@app.route('/charityfindmore<hid>')
def charityfindmore(hid):

    if  session.get('mail')==None:
	    return render_template('Login.html')
    try:
        #print(hid)
        mail = session['mail']
        #print(mail)
        con = sqlite3.connect("acms.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select CharityAddress from Charity WHERE CharityMail='{}'".format(mail))
        CharityAddress = cur.fetchone();
        #print(cid)
        #print(CharityAddress[0])
        con.close()

        with sqlite3.connect("acms.db") as con:
            cur = con.cursor()
            cur.execute("select HotelName,HotelPhone,HotelMail,HotelAddress from Hotel WHERE HotelID='{}'".format(hid))
            HotelName, HotelPhone, HotelMail, HotelAddress= cur.fetchone();
            #print(HotelAddress)
            #cur.execute("select CharityAddress from Charity WHERE CharityID='{}'".format(cid))
            #CharityAddress = cur.fetchone();
            #print(CharityAddress)
            return render_template('CharityFindHotelMore.html', HotelName=HotelName, HotelPhone=HotelPhone, HotelMail=HotelMail, HotelAddress=HotelAddress, CharityAddress=CharityAddress[0])
            con.commit()


    except:
        msgDeatils = "Selection Failed Please check the query / db "
        con.rollback()
        return render_template("result1.html", msgDeatils=msgDeatils)
        con.close()
    #finally:


@app.route('/charityfindorder<aid>')
def charityfindorder(aid):

    if  session.get('mail')==None:
	    return render_template('Login.html')
    try:

        #print(aid)
        with sqlite3.connect("acms.db") as con:
            cur = con.cursor()
            cur.execute("select HotelName,HotelPhone,HotelMail,HotelAddress,ExpTime,Availability.AvailID from Availability natural join Hotel WHERE Availability.AvailID='{}'".format(aid))
            HotelName, HotelPhone, HotelMail, HotelAddress,ExpTime,AvailID= cur.fetchone();
            #print(HotelName)

            return render_template('CharityFindHotelOrder.html', HotelName=HotelName, HotelPhone=HotelPhone, HotelMail=HotelMail, HotelAddress=HotelAddress, ExpTime=ExpTime, AvailID=AvailID)
            con.commit()

    except:
        msgDeatils = "Selection Failed Please check the query / db "
        con.rollback()
        return render_template("result1.html", msgDeatils=msgDeatils)
        con.close()
    #finally:


@app.route('/charityfindorderentry', methods=['POST', 'GET'])
def charityfindorderentry():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    if request.method == 'POST':
        try:
            aid = request.form['aid']
            count=request.form['count']
            #print(aid)
            #print(count)
            mail = session['mail']
            #print(mail)
            con = sqlite3.connect("acms.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select CharityID from Charity WHERE CharityMail='{}'".format(mail))
            cid = cur.fetchone();
            con.commit()
            #print(cid[0])
            cur.execute("select AvailLeftOut from Availability WHERE AvailID='{}'".format(aid))
            apeople = cur.fetchone();
            con.commit()
            #print(apeople[0])

            #print("hello1")

            if int(count)>int(apeople[0]):
                msgDeatils = "Ordered more than available"
                return render_template("result1.html", msgDeatils=msgDeatils)

            con.close()

            #print("hello")
            with sqlite3.connect("acms.db") as con:
                #print("hey")
                cur = con.cursor()
                #print("hey")

                cur.execute("INSERT INTO OrderPlaced (CharityID ,AvailID ,People )VALUES(?, ?, ?)",(cid[0],aid,count) )
                con.commit()
                #print("Order Added successfully")
                leftout=int(apeople[0])-int(count)
                #print(leftout)
                cur.execute('''UPDATE Availability SET AvailLeftOut = ?  WHERE AvailID = ?''',(leftout, aid))
                con.commit()
                #print("Availability updated successfully")
                return redirect(url_for('charity'))


        except:
            msgDeatils = "Insertion Failed Please check the query / db "
            con.rollback()
            return render_template("result.html", msgDeatils=msgDeatils)
            con.close()
        #finally:



@app.route('/charityquery')
def charityquery():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    return render_template('CharityQuery.html')



@app.route('/charityqueryresult', methods=['POST', 'GET'])
def charityqueryresult():

	if  session.get('mail')==None:
		return render_template('Login.html')
	if request.method == 'POST':
		try:
			count = request.form['count']
			date2 = request.form['date']
			if(date2==""):
				date2=None;
			print("ddd :")
			print(date2)
			hour = request.form.get('hour')
			minutes=request.form.get('minutes')
			#print("str(hour)+" :"+str(minutes))
			if date2 is not None:
				date2+=" "+str(hour)+":"+str(minutes)+":00"
				date=datetime.strptime(date2,"%Y-%m-%d %H:%M:%S")
			else:
				date=date2
			
			
            #print(count)
			
            #print("hey")

			with sqlite3.connect("acms.db") as con:
				con.row_factory = sqlite3.Row
				cur = con.cursor()

				if date is None:
					print("hello")
					cur.execute("select HotelName,AvailLeftOut,ExpTime,AvailID,Hotel.HotelID from  Availability natural join Hotel where AvailLeftOut > ? and AvailLeftOut < ? and ExpTime > datetime('now','localtime')",(int(count)-10,int(count)+10))
					orderrows = cur.fetchall();
                    #print(orderrows[0][0])
                    #print(orderrows[0][1])
					con.commit()
					return render_template("CharityQueryResult.html", rows=orderrows)
				else:
                    #print("hehe")
					cur.execute("select HotelName,AvailLeftOut,ExpTime,AvailID,Hotel.HotelID from  Availability natural join Hotel where AvailLeftOut > ? and AvailLeftOut < ? and ExpTime >= ?",(int(count)-10, int(count)+10, date))
					orderrows = cur.fetchall();
					con.commit()
					return render_template("CharityQueryResult.html", rows=orderrows)


		except:
			msgDeatils = "Select Failed Please check the query / db "
            #con.rollback()
			return render_template("result1.html", msgDeatils=msgDeatils)
			con.close()
        #finally:


@app.route('/charityquerymore<hid>')
def charityquerymore(hid):

    if  session.get('mail')==None:
	    return render_template('Login.html')
    try:
        #print(hid)
        mail = session['mail']
        #print(mail)
        con = sqlite3.connect("acms.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select CharityAddress from Charity WHERE CharityMail='{}'".format(mail))
        CharityAddress = cur.fetchone();
        #print(cid)
        #print(CharityAddress[0])
        con.close()

        with sqlite3.connect("acms.db") as con:
            cur = con.cursor()
            cur.execute("select HotelName,HotelPhone,HotelMail,HotelAddress from Hotel WHERE HotelID='{}'".format(hid))
            HotelName, HotelPhone, HotelMail, HotelAddress= cur.fetchone();
            #print(HotelAddress)
            #cur.execute("select CharityAddress from Charity WHERE CharityID='{}'".format(cid))
            #CharityAddress = cur.fetchone();
            #print(CharityAddress)
            return render_template('CharityQueryMore.html', HotelName=HotelName, HotelPhone=HotelPhone, HotelMail=HotelMail, HotelAddress=HotelAddress, CharityAddress=CharityAddress[0])
            con.commit()


    except:
        msgDeatils = "Selection Failed Please check the query / db "
        con.rollback()
        return render_template("result1.html", msgDeatils=msgDeatils)
        con.close()
    #finally:


@app.route('/charityqueryorder<aid>')
def charityqueryorder(aid):

    if  session.get('mail')==None:
	    return render_template('Login.html')
    try:

        #print(aid)
        with sqlite3.connect("acms.db") as con:
            cur = con.cursor()
            cur.execute("select HotelName,HotelPhone,HotelMail,HotelAddress,ExpTime,Availability.AvailID from Availability natural join Hotel WHERE Availability.AvailID='{}'".format(aid))
            HotelName, HotelPhone, HotelMail, HotelAddress,ExpTime,AvailID= cur.fetchone();
            #print(HotelName)

            return render_template('CharityQueryOrder.html', HotelName=HotelName, HotelPhone=HotelPhone, HotelMail=HotelMail, HotelAddress=HotelAddress, ExpTime=ExpTime, AvailID=AvailID)
            con.commit()

    except:
        msgDeatils = "Selection Failed Please check the query / db "
        con.rollback()
        return render_template("result1.html", msgDeatils=msgDeatils)
        con.close()
    #finally:


@app.route('/charityqueryorderentry', methods=['POST', 'GET'])
def charityqueryorderentry():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    if request.method == 'POST':
        try:
            aid = request.form['aid']
            count=request.form['count']
            #print(aid)
            #print(count)
            mail = session['mail']
            #print(mail)
            con = sqlite3.connect("acms.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select CharityID from Charity WHERE CharityMail='{}'".format(mail))
            cid = cur.fetchone();
            con.commit()
            #print(cid[0])
            cur.execute("select AvailLeftOut from Availability WHERE AvailID='{}'".format(aid))
            apeople = cur.fetchone();
            con.commit()
            #print(apeople[0])

            #print("hello1")

            if int(count)>int(apeople[0]):
                msgDeatils = "Ordered more than available"
                return render_template("result1.html", msgDeatils=msgDeatils)

            con.close()

            #print("hello")
            with sqlite3.connect("acms.db") as con:
                #print("hey")
                cur = con.cursor()
                #print("hey")

                cur.execute("INSERT INTO OrderPlaced (CharityID ,AvailID ,People )VALUES(?, ?, ?)",(cid[0],aid,count) )
                con.commit()
                #print("Order Added successfully")
                leftout=int(apeople[0])-int(count)
                #print(leftout)
                cur.execute('''UPDATE Availability SET AvailLeftOut = ?  WHERE AvailID = ?''',(leftout, aid))
                con.commit()
                #print("Availability updated successfully")
                return redirect(url_for('charity'))


        except:
            msgDeatils = "Insertion Failed Please check the query / db "
            con.rollback()
            return render_template("result.html", msgDeatils=msgDeatils)
            con.close()
        #finally:


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
@app.route('/analytics')
def analytics():
    con = sqlite3.connect("acms.db")
    con.row_factory =  dict_factory
    cur = con.cursor()
    cur.execute("select SUM(AvailPeople) as total,SUM(AvailLeftOut) as leftout,Hotel.HotelName ,Hotel.HotelAddress from Availability natural join Hotel group by HotelName ")
    orderrows = cur.fetchall();
    #print(orderrows[0]["Hotel.HotelID"])
    return render_template("HotelAnalytics.html", rows=orderrows)


@app.route('/charityrecommend')
def charityrecommend():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    con = sqlite3.connect('acms.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    df = pd.read_sql_query("select OrderPlaced.CharityID,OrderPlaced.AvailID,OrderPlaced.Rating,Availability.HotelID from OrderPlaced natural join Availability where Rating is not null;",con)
    cha = pd.read_sql_query("select CharityID from Charity ;", con)
    hote = pd.read_sql_query("select HotelID from Hotel ;", con)

    cha = cha.values
    hote = hote.values

    cha = cha.transpose()
    hote = hote.transpose()

    cha.flatten()
    hote.flatten()

    df2 = pd.DataFrame(index=cha[0], columns=hote[0], dtype=np.float64)
    df2.fillna(0, inplace=True);
    count = pd.DataFrame(index=cha[0], columns=hote[0], dtype=np.int32)
    count.fillna(0, inplace=True)

    for row_index, row in df.iterrows():
        val = (count.get_value(int(row['CharityID']), int(row['HotelID'])) * df2.get_value(int(row['CharityID']),int(row['HotelID'])) + float(row['Rating'])) / (count.get_value(int(row['CharityID']), int(row['HotelID'])) + 1)
        df2.set_value(int(row['CharityID']), int(row['HotelID']), float(val))
        count.set_value(int(row['CharityID']), int(row['HotelID']),count.get_value(int(row['CharityID']), int(row['HotelID'])) + 1)

    R = df2.as_matrix()
    user_ratings_mean = np.mean(R, axis=1)
    R_demeaned = R - user_ratings_mean.reshape(-1, 1)

    U, sigma, Vt = svds(R_demeaned, k=5)

    sigma = np.diag(sigma)

    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)
    preds_df = pd.DataFrame(all_user_predicted_ratings, columns=df2.columns)

    mail = session['mail']

    cur.execute("select CharityID from Charity WHERE CharityMail='{}'".format(mail))
    cid = cur.fetchone();

    ind = np.where(cha[0] == cid)
    sorted_user_predictions = preds_df.iloc[int(ind[0])].sort_values(ascending=False)

    greaterz = sorted_user_predictions[sorted_user_predictions > 0]
    rechot = greaterz.index

    sql = "select HotelName,AvailLeftOut,ExpTime,AvailID,Hotel.HotelID from  Availability natural join Hotel where AvailLeftOut > 0 and ExpTime > datetime('now','localtime') and Hotel.HotelID in {}".format(str(tuple(rechot)))
    cur.execute(sql)
    orderrows = cur.fetchall();

    return render_template("CharityRecommend.html", rows=orderrows)



@app.route('/charityrecommendmore<hid>')
def charityrecommendmore(hid):

    if  session.get('mail')==None:
	    return render_template('Login.html')
    try:
        #print(hid)
        mail = session['mail']
        #print(mail)
        con = sqlite3.connect("acms.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select CharityAddress from Charity WHERE CharityMail='{}'".format(mail))
        CharityAddress = cur.fetchone();
        #print(cid)
        #print(CharityAddress[0])
        con.close()

        with sqlite3.connect("acms.db") as con:
            cur = con.cursor()
            cur.execute("select HotelName,HotelPhone,HotelMail,HotelAddress from Hotel WHERE HotelID='{}'".format(hid))
            HotelName, HotelPhone, HotelMail, HotelAddress= cur.fetchone();
            #print(HotelAddress)
            #cur.execute("select CharityAddress from Charity WHERE CharityID='{}'".format(cid))
            #CharityAddress = cur.fetchone();
            #print(CharityAddress)
            return render_template('CharityRecommendMore.html', HotelName=HotelName, HotelPhone=HotelPhone, HotelMail=HotelMail, HotelAddress=HotelAddress, CharityAddress=CharityAddress[0])
            con.commit()


    except:
        msgDeatils = "Selection Failed Please check the query / db "
        con.rollback()
        return render_template("result1.html", msgDeatils=msgDeatils)
        con.close()
    #finally:



@app.route('/charityrecommendorder<aid>')
def charityrecommendorder(aid):

    if  session.get('mail')==None:
	    return render_template('Login.html')
    try:

        #print(aid)
        with sqlite3.connect("acms.db") as con:
            cur = con.cursor()
            cur.execute("select HotelName,HotelPhone,HotelMail,HotelAddress,ExpTime,Availability.AvailID from Availability natural join Hotel WHERE Availability.AvailID='{}'".format(aid))
            HotelName, HotelPhone, HotelMail, HotelAddress,ExpTime,AvailID= cur.fetchone();
            #print(HotelName)

            return render_template('CharityRecommendOrder.html', HotelName=HotelName, HotelPhone=HotelPhone, HotelMail=HotelMail, HotelAddress=HotelAddress, ExpTime=ExpTime, AvailID=AvailID)
            con.commit()

    except:
        msgDeatils = "Selection Failed Please check the query / db "
        con.rollback()
        return render_template("result1.html", msgDeatils=msgDeatils)
        con.close()
    #finally:



@app.route('/charityrecommendorderentry', methods=['POST', 'GET'])
def charityrecommendorderentry():

    if  session.get('mail')==None:
	    return render_template('Login.html')
    if request.method == 'POST':
        try:
            aid = request.form['aid']
            count=request.form['count']
            #print(aid)
            #print(count)
            mail = session['mail']
            #print(mail)
            con = sqlite3.connect("acms.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("select CharityID from Charity WHERE CharityMail='{}'".format(mail))
            cid = cur.fetchone();
            con.commit()
            #print(cid[0])
            cur.execute("select AvailLeftOut from Availability WHERE AvailID='{}'".format(aid))
            apeople = cur.fetchone();
            con.commit()
            #print(apeople[0])

            #print("hello1")

            if int(count)>int(apeople[0]):
                msgDeatils = "Ordered more than available"
                return render_template("result1.html", msgDeatils=msgDeatils)

            con.close()

            #print("hello")
            with sqlite3.connect("acms.db") as con:
                #print("hey")
                cur = con.cursor()
                #print("hey")

                cur.execute("INSERT INTO OrderPlaced (CharityID ,AvailID ,People )VALUES(?, ?, ?)",(cid[0],aid,count) )
                con.commit()
                #print("Order Added successfully")
                leftout=int(apeople[0])-int(count)
                #print(leftout)
                cur.execute('''UPDATE Availability SET AvailLeftOut = ?  WHERE AvailID = ?''',(leftout, aid))
                con.commit()
                #print("Availability updated successfully")
                return redirect(url_for('charity'))


        except:
            msgDeatils = "Insertion Failed Please check the query / db "
            con.rollback()
            return render_template("result.html", msgDeatils=msgDeatils)
            con.close()
        #finally:




if __name__ == '__main__':
    app.run(debug=True)