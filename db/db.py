import  sqlite3
from flask import g
import time


DB = "comidas.db"


def abrirConexion ():
    db = getattr(g, '_database', None)
    try:
        if db is None:
            db = g._database = sqlite3.connect(DB)
            print("db conectada, Hora: {}".format(time.ctime()))
            
    except Exception as err:
        print("Error", err)

    return db

def cerrarConexion ():
    db = getattr(g, '_database', None)
    try:
        if db is not None:
            db.close()
            print("db Desconectada, Hora {}".format(time.ctime()))
            
    except Exception as err:
        print(err)    
    

def insertInto(sql, data):
    try:
        conexion = abrirConexion()
        cur = conexion.cursor()
        cur.execute(sql, data)     
        conexion.commit()
        cur.close()
        
    except Exception as err:
        print(err)
        
 

def getInfoDb(sql):
    output = None
    try:
        conexion = abrirConexion()
        cur = conexion.cursor()
        cur.execute(sql)     
        conexion.commit()
        output = cur.fetchall()
        cur.close()
    except Exception as err:
        print(err)
    
    return output
       

def updateInfo(sql, state, id):
    
    try:
        conexion = abrirConexion()
        cur = conexion.cursor()
        cur.execute(sql, [state, id])
        conexion.commit()
        cur.close() 
        
    except Exception as err:
        print(err)
    