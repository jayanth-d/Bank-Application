from flask import Flask, render_template, request, redirect, url_for
import csv
from account import Account

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if (loginCheck == False):
        return redirect(url_for('login'))
    else:
        return render_template("home.html")
    
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.form
        accno = data["accno"]
        password = data['password']
        for i,k in dictOfClass.items():
            if accno == i:
                if password == k.password:
                    global loginCheck
                    loginCheck = True
                    global currentacc
                    currentacc = k
                    return redirect(url_for('index'))
                else:
                    return render_template("login.html", message = "Wrong Password")
        return render_template("login.html", message = "Account Does NOT exist")   
    else:
        return render_template("login.html")
    
@app.route('/balance')
def balance():
    global currentacc
    bal = currentacc.balance
    return render_template('balance.html', balance = bal)

@app.route('/deposit', methods=["POST", "GET"])
def deposit():
    if request.method == "POST":
        data = request.form
        amount = int(data["amount"])
        global currentacc
        currentacc.deposit(amount)
        return render_template("deposit.html", message = "Your money has been Credited")
    else:
        return render_template("deposit.html")

@app.route('/transfer', methods=["POST", "GET"])
def transfer():
    if request.method == "POST":
        data = request.form
        accno = data["accno"]
        amount = int(data["amount"])
        for i,k in dictOfClass.items():
            if accno == i:
                obj = k
                ret = currentacc.transfer(amount,obj)
                if ret == 0:
                    return render_template("transfer.html", message = "You do NOT have sufficient balance")
                else:
                    return render_template("transfer.html", message = "Your money has been Transfered")
        return render_template("transfer.html", message = "Account Number does NOT exist")
    else:
        return render_template("transfer.html")
        

@app.route('/withdraw', methods=["POST", "GET"])
def withdraw():
    if request.method == "POST":
        data = request.form
        amount = int(data["amount"])
        global currentacc
        ret = currentacc.withdraw(amount)
        if ret == 0:
            return render_template("withdraw.html", message = "You do NOT have sufficient balance")
        else:
            return render_template("withdraw.html", message = "Your money has been Debited")
    else:
        return render_template("withdraw.html")

@app.route('/logout')
def logout():
    global loginCheck
    loginCheck = False
    return redirect(url_for('index'))

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        global dictOfClass
        global loginCheck
        global currentacc
        data = request.form
        username = data['username']
        password = data['password']
        length = len(dictOfClass)
        accno = 'acc00'+str(length+1)
        acc = Account(username, accno, password, '0')
        currentacc = acc
        dictOfClass[accno] = acc
        loginCheck = True
        return redirect(url_for('index'))
    else:
        return render_template('signup.html')

if __name__ == "__main__":
    dictOfClass = {}
    loginCheck = False
    listOflist = []
    with open('data.csv', newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            obj = Account(row[0], row[1], row[2], row[3])
            accno = row[1]
            dictOfClass[accno] = obj
    app.run(debug = False)
    for i in dictOfClass.values():
        list = [i.name, i.accno, i.password, i.balance]
        listOflist.append(list)
    print(listOflist)
    with open('data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(listOflist)
