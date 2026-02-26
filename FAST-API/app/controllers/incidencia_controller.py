from fastapi import HTTPException
from config.db_config import get_db_connection
from models.incidencia_model import Incidencia
from fastapi.encoders import jsonable_encoder

class IncidenciaController:
        
    def create_incidencia(self, incidencia: Incidencia):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO incidencia (fecha,descripcion,id_usuario,id_tipo,id_estado,id_departamento,id_prioridad,departamento,estado,prioridad,tipo_incidencia)
             VALUES (%s, %s, %s, %s, %s ,%s, %s, %s, %s, %s ,%s)", (incidencia.fecha, incidencia.descripcion, incidencia.id_usuario, incidencia.id_tipo, incidencia.id_estado, incidencia.id_departamento, incidencia.id_prioridad, incidencia.departamento, incidencia.estado, incidencia.prioridad, incidencia.tipo_incidencia))
            conn.commit()
            conn.close()
            return {"resultado": "Incidencia creado"}
        except psycopg2.Error as err:
            print(err)
            # Si falla el INSERT, los datos no quedan guardados parcialmente en la base de datos
            # Se usa para deshacer los cambios de la transacción activa cuando ocurre un error en el try.
            conn.rollback()
        finally:
            conn.close()
        

    def get_incidencia(self, incidencia_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM incidencia WHERE id = %s", (incidencia_id,))
            result = cursor.fetchone()
            payload = []
            content = {} 
            
            content={
                    'id_incidencias':int(result[0]),
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
                    'tipo_incidencia':data[11]
                    
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
       
    def get_incidencias(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM incidencia")
            result = cursor.fetchall()
            payload = []
            content = {} 
            for data in result:
                content={
                    'id_incidencias':data[0],
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
                    'tipo_incidencia':data[11]
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