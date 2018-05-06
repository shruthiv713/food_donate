import sqlite3
from flask import Flask ,render_template,request
import smtplib
from email.mime.text import MIMEText
smtp_ssl_host = 'smtp.gmail.com' # smtp.mail.yahoo.com
smtp_ssl_port = 465
username = 'donatefood4'
password = '@donatefood4'
sender = 'donatefood4@gmail.com'

app = Flask(__name__)
@app.route('/')
def mainfun():
    return render_template('Login.html')


@app.route('/signup')
def signup():
    return render_template('Signup.html')

@app.route('/forgot')
def forgot():
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
                    msgDeatils = "Hotel Added successfully"
                    con.commit()
                if category == 'orphanage':
                    cur.execute("INSERT INTO Charity (CharityName ,CharityPhone ,CharityMail ,CharityPassword ,CharityAddress)VALUES(?, ?, ?, ? ,?)",(name,mob,mail,psw,address) )
                    msgDeatils = "Charity Added successfully"
                    con.commit()
        except:
            msgDeatils = "Insertion Failed Please check the query / db "
            con.rollback()
        finally:
            return render_template("result.html",msgDeatils=msgDeatils)
            con.close()


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
                    msgDeatils = "Hotel logged successfully"
                    if hp[0]==psw:
                        return render_template("result.html", msgDeatils=msgDeatils)
                    else:
                        msgDeatils = "Hotel Password incorrect"
                        return render_template("result.html", msgDeatils=msgDeatils)
                if category == 'orphanage':
                    cur.execute("SELECT CharityPassword from Charity WHERE CharityMail='{}'".format(mail))
                    hp = cur.fetchone();
                    msgDeatils = "Charity logged successfully"
                    if hp[0] == psw:
                        return render_template("result.html", msgDeatils=msgDeatils)
                    else:
                        msgDeatils = "Charity Password incorrect"
                        return render_template("result.html", msgDeatils=msgDeatils)


                con.commit()
        except:
            msgDeatils = "Incorrect email "
            con.rollback()
        finally:
            return render_template("result.html",msgDeatils=msgDeatils)
            con.close()


if __name__ == '__main__':
    app.run()