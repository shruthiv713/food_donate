import sqlite3
from flask import Flask ,render_template,request
app = Flask(__name__)
@app.route('/')
def mainfun():
    return render_template('Login.html')


@app.route('/signup')
def signup():
    return render_template('Signup.html')


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
                    cur.execute("INSERT INTO Charity (CharityName ,CharityPhone ,CharityMail ,CharityPassword ,HotelAddress)VALUES(?, ?, ?, ? ,?)",(name,mob,mail,psw,address) )
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
                    hp=cur.execute("SELECT HotelPassword from Hotel WHERE HotelMail='{}'".format(mail))
                    msgDeatils = "Hotel logged successfully"
                    if hp==psw:
                        return render_template("result.html", msgDeatils=msgDeatils)
                    else:
                        msgDeatils = "Hotel Password incorrect"
                        return render_template("result.html", msgDeatils=msgDeatils)
                if category == 'orphanage':
                    hp = cur.execute("SELECT CharityPassword from Charity WHERE CharityMail='{}'".format(mail))
                    msgDeatils = "Charity logged successfully"
                    if hp == psw:
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