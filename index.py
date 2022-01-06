from flask import Flask, render_template, request, redirect, url_for
from db import db   

app = Flask(__name__)



@app.route("/", methods=['POST', 'GET'])
def index():   
    if request.method == "POST":   
        try:
            data = list(request.form.values())
            sql = "INSERT INTO todoComidas (nombre, valor) VALUES (?, ?)"
            db.insertInto(sql, data)
            
        except Exception as err :
            print(err)
        return redirect(url_for('pedidos')) 
    return render_template('comida.html')


@app.route("/pedidos", methods=['POST', 'GET'])
def pedidos():
    try:   
        sql = "SELECT * FROM todoComidas"
        comidas = db.getInfoDb(sql)
        print(comidas)          
    except Exception as err :
        print(err)  
    
    if request.method == "POST":        
        try:
            data = list(request.form.values())
            data.append("EN ESPERA")          
            sql = "INSERT INTO pedidos (nombre, articulo, cantidad, direccion, ciudad, telefono, fecha, total, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            db.insertInto(sql, data)
            
        except Exception as err :
            print(err)   
        pass
    
    return render_template('pedidos.html', comidas=comidas)
    

@app.route('/listaDePedidos', methods=['POST', "GET"])
def listaDePedidos():
    try:       
        sql = "SELECT * FROM pedidos"
        pedidos = db.getInfoDb(sql)
    
    except Exception as err :
        print(err)
             
    if request.method == "POST":
        
        id = request.form.get("options")
        print(id)
        
        if request.form.get("preparar") == "Comenzar pedido":    
            try:                        
                sql = "UPDATE pedidos SET estado=? WHERE id=?"
                db.updateInfo(sql, "EN PREPARACION", id)
                
            except Exception as err:
                print(err)
            return redirect(url_for('listaDePedidos')) 
                                
        elif request.form.get("enviar") == "Enviar Pedido":
            try:
                sql = "UPDATE pedidos SET estado=? WHERE id=?"
                db.updateInfo(sql, "EN REPARTO", id)
            
            except Exception as err :
                print(err)
            return redirect(url_for('listaDePedidos'))
        
        elif request.form.get("entregado") == "Pedido entregado":
            try:
                sql = "UPDATE pedidos SET estado=? WHERE id=?"
                db.updateInfo(sql, "ENTREGADO", id)
            
            except Exception as err:
                print(err)
            return redirect(url_for('listaDePedidos'))     
        
    return render_template('listaPedidos.html', pedidos=pedidos)


if __name__ == "__main__":
    app.run(debug=True, port=3000)