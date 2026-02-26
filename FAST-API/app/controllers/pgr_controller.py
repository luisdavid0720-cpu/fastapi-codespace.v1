from fastapi import HTTPException
from config.db_config import get_db_connection
from models.pqr_model_model import Incidencia
from fastapi.encoders import jsonable_encoder

class IncidenciaController:
        
    def create_pqr(self, pqr: pqr):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pqr (fecha,descripcion,id_usuario,id_tipo,id_estado,id_departamento,id_prioridad,departamento,estado,prioridad,tipo_pqr)\
             VALUES (%s, %s, %s, %s, %s ,%s, %s, %s, %s, %s ,%s)", (pqr.fecha, pqr.descripcion, pqr.id_usuario, pqr.id_tipo, pqr.id_estado, pqr.id_departamento, pqr.id_prioridad, pqr.departamento, pqr.estado, pqr.prioridad, pqr.tipo_pqr))
            conn.commit()
            conn.close()
            return {"resultado": "pqr creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_pqr(self, pqr_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pqr WHERE id = %s", (pqr_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_pqr':int(result[0]),
                    'fecha':data[1],
                    'descripcion':data[2],
                    'id_usuario':data[3],
                    'id_tipo':data[4],
                    'id_estado':data[5],
                    'id_departamento':data[6],
                    'id_prioridad':data[7],
                    'departamento':data[8],
                    'estado':data[9],
                    'prioridad':data[10],
                    'tipo_pqr':data[11]
                    
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
       
    def get_pqr(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pqr")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_pqr':data[0],
                    'fecha':data[1],
                    'descripcion':data[2],
                    'id_usuario':data[3],
                    'id_tipo':data[4],
                    'id_estado':data[5],
                    'id_departamento':data[6],
                    'id_prioridad':data[7],
                    'departamento':data[8],
                    'estado':data[9],
                    'prioridad':data[10],
                    'tipo_pqr':data[11]
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
    
    
##pqr_controller = pqrController()