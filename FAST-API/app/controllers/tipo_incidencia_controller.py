from fastapi import HTTPException
from config.db_config import get_db_connection
from models.tipo_incidencia_model import Tipo_incidencia
from fastapi.encoders import jsonable_encoder

class Tipo_incidenciaController:
        
    def create_tipo_incidencia(self, tipo_incidencia: Tipo_incidencia):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tipo_incidencia (nombre,incidencias) VALUES (%s, %s)", (user.nombre, user.incidencias))
            conn.commit()
            conn.close()
            return {"resultado": "Tipo_incidencia creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_tipo_incidencia(self, tipo_incidencia_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tipo_incidencia WHERE id = %s", (tipo_incidencia_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id':int(result[0]),
                    'nombre':result[1],
                    'incidencias':result[2]
                    
            }
            payload.append(content)
            
            json_data = jsonable_encoder(content)            
            if result:
               return  json_data
            else:
                ##Esto interrumpe la ejecución y responde al cliente con un código 404
                ## comunica al cliente de la API qué pasó (error HTTP).
                ##código 404,comportamiento correcto según las reglas HTTP
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.Error as err:
            print(err)
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            ##Maneja el estado de la transacción en la base de datos.Si un INSERT, UPDATE o DELETE falla dentro de una transacción, rollback() revierte esos cambios.
            conn.rollback()
        finally:
            conn.close()
       
    def get_tipo_incidencias(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tipo_incidencia")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id':data[0],
                    'nombre':data[1],
                    'incidencias':data[2]
                    
                }
                payload.append(content)
                content = {}
            json_data = jsonable_encoder(payload)        
            if result:
               return {"resultado": json_data}
            else:
                raise HTTPException(status_code=404, detail="User not found")  
                
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
    
    
       

##user_controller = UserController()