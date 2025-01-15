from flask import Flask, render_template
import pymysql
from flask import Flask
from flask_cors import CORS, cross_origin
from flaskext.mysql import MySQL
from flask import jsonify
from flask import flash, request
import requests
app = Flask(__name__)
CORS(app)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'scrapingdb'
app.config['MYSQL_DATABASE_HOST'] = 'mysqlServer'
mysql.init_app(app)


@app.route('/maillots')
def prices():
	try:
          
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM maillots")
		pricesRows = cursor.fetchall()
		response = jsonify(pricesRows)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nike_page')
def nike_page():
    return render_template('nike.html')

@app.route('/uni_page')
def uni_page():
    return render_template('unisport.html')

@app.route('/foot_fr_page')
def foot_fr_page():
    return render_template('foot_fr.html')

@app.route('/nike')
def itemsNike():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM maillots WHERE sites='nike.com'")
		pricesRows = cursor.fetchall()
		response = jsonify(pricesRows)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
	
@app.route('/foot_fr')
def itemsFoot():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM maillots WHERE sites='foot.fr'")
		pricesRows = cursor.fetchall()
		response = jsonify(pricesRows)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		


@app.route('/uni')
def itemsUni():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM maillots WHERE sites='unisportstore.fr'")
		pricesRows = cursor.fetchall()
		response = jsonify(pricesRows)
		response.status_code = 200
		return response
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()







def update_database_logic():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Vérifiez si la colonne 'etat' existe déjà
        cursor.execute("""
            SELECT COUNT(*)
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_schema = 'testdb' AND table_name = 'prices' AND column_name = 'etat';
        """)
        if cursor.fetchone()[0] == 0:
            # Si la colonne 'etat' n'existe pas, l'ajouter
            cursor.execute("ALTER TABLE prices ADD COLUMN etat VARCHAR(255);")
        
        # Définir les prix minimum et maximum pour 'Certideal'
        cursor.execute("SELECT MIN(price) FROM prices WHERE seller = 'Certideal';")
        min_price = cursor.fetchone()[0]
        cursor.execute("SELECT MAX(price) FROM prices WHERE seller = 'Certideal';")
        max_price = cursor.fetchone()[0]
        
        # Mise à jour de la colonne 'etat' en fonction des prix
        cursor.execute("""
            UPDATE prices
            SET etat = CASE
                WHEN price <= %s THEN 'Correct'
                WHEN price >= %s THEN 'Parfait'
                ELSE 'Très bon état'
            END
            WHERE seller = 'Certideal';
        """, (min_price, max_price))
        
        # Mise à jour des lignes où 'etat' est NULL à 'premium'
        cursor.execute("UPDATE prices SET etat = 'Premium' WHERE etat IS NULL;")

        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback() # Rollback en cas d'erreur
        print(str(e))
    finally:
        cursor.close()
        conn.close()







@app.route('/update-prices', methods=['POST'])
def update_prices():
    update_database_logic()
    return jsonify(success=True)




@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
