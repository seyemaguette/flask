from flask import Flask, render_template, redirect, request
from flask_mysqldb import MySQL 

app=Flask(__name__)

# -------- pour connecter Flask MySQL----------
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'gestion_de_budget'
mysql = MySQL(app)

with app.app_context():
    cursor = mysql.connection.cursor()


@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    depense=0
    revenu=0
    solde =0
    cursor.execute("SELECT * FROM depense")
    depenseDetails = cursor.fetchall()
    cursor.execute("SELECT * FROM revenu")
    revenuDetails = cursor.fetchall()
    for depenses in depenseDetails:
        depense+=depenses[1]
    for revenus in revenuDetails:
        revenu+=revenus[1]
    solde= revenu - depense
    return render_template('index.html',depenseDetails=depenseDetails, revenuDetails=revenuDetails,depense=depense, revenu=revenu, solde=solde)
    
    


@app.route("/depense",methods=['POST','GET'])
def depense():
     if request.method == 'POST':
        depenseDetails = request.form
        titre =  depenseDetails['titre']
        montant =  depenseDetails['montant']
        if titre!='' and montant!='':
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO depense(titre, montant) VALUES(%s, %s)",(titre, montant))
            mysql.connection.commit()
            cursor.close()
            return redirect('/')  
     return render_template("depense.html")


@app.route("/revenu",methods=['POST','GET'])
def revenu():
    if request.method == 'POST':
        revenuDetails = request.form
        titre =  revenuDetails['titre']
        montant =  revenuDetails['montant']
        if titre!='' and montant!='':
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO revenu(titre, montant) VALUES(%s, %s)",(titre, montant))
            mysql.connection.commit()
            cursor.close()
            return redirect('/')  
    return render_template("revenu.html")



@app.route("/delete/<int:id>/")
def delete(id):
    cursor = mysql.connection.cursor()
    query= "DELETE FROM depense WHERE id=%s"
    values=(id,)
    cursor.execute(query,values)
    mysql.connection.commit()
    query= "DELETE FROM revenu WHERE id=%s"
    values=(id,)
    cursor.execute(query,values)
    mysql.connection.commit()
    depense=0
    revenu=0
    solde =0
    cursor.execute("SELECT * FROM depense")
    depenseDetails = cursor.fetchall()
    cursor.execute("SELECT * FROM revenu")
    revenuDetails = cursor.fetchall()
    for depenses in depenseDetails:
        depense+=depenses[1]
    for revenus in revenuDetails:
        revenu+=revenus[1]
    solde= revenu - depense
    return render_template('index.html',depenseDetails=depenseDetails,  revenuDetails=revenuDetails,depense=depense, revenu=revenu, solde=solde)


@app.route("/update/<int:titre>", methods=['GET','POST'])
def update(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM depense WHERE titre=%s",(id,))
    updateDepense=cursor.fetch()
    if request.method == "POST":
        titre=request.form['titre']
        montant=request.form['montant']
        query="UPDATE depense SET titre=%s,montant=%s WHERE titre=%s "
        values=(titre,montant,id,)
        cursor.execute(query,values)
        mysql.connection.commit()
        depense=0
        revenu=0
        solde =0
        cursor.execute("SELECT * FROM depense")
        depenseDetails = cursor.fetchall()
        cursor.execute("SELECT * FROM revenu")
        revenuDetails = cursor.fetchall()
        for depenses in depenseDetails:
            depense+=depenses[1]
        for revenus in revenuDetails:
            revenu+=revenus[1]
        solde= revenu - depense
        return render_template('index.html',depenseDetails=depenseDetails, depense=depense, revenu=revenu, solde=solde)
    return render_template('update.html',depense=updateDepense)
    
   
    
    
    
    
    
    
    
if __name__=="__main__":
    app.run(debug=True,port=5001,host='192.168.56.1')