import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.usuario_model import Usuario
from fastapi.encoders import jsonable_encoder
from services.email_service import notify_usuario_eliminado

class UsuarioController:
        
    def create_usuario(self, usuario: Usuario):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO usuario (nombre,cedula,carrera,semestre,cargo,celular,correo,id_rol) VALUES 
            (%s, %s, %s, %s, %s , %s, %s, %s)""", (usuario.nombre, usuario.cedula, usuario.carrera, usuario.semestre, usuario.cargo, usuario.celular, usuario.correo, usuario.id_rol))
            conn.commit()
            return {"resultado": "Usuario creado"}
        except psycopg2.Error as err:
            conn.rollback()
            print(err)
        finally:
            conn.close()

    def get_usuario(self, usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (usuario_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            content = {
                'id_usuario': int(result[0]), 'nombre': result[1], 'cedula': result[2],
                'carrera': result[3], 'semestre': result[4], 'cargo': result[5],
                'celular': result[6], 'correo': result[7], 'id_rol': result[8]
            }
            return jsonable_encoder(content)
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_usuarios(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id_usuario': data[0], 'nombre': data[1], 'cedula': data[2],
                    'carrera': data[3], 'semestre': data[4], 'cargo': data[5],
                    'celular': data[6], 'correo': data[7], 'id_rol': data[8]
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

    def update_usuario(self, usuario_id: int, usuario: Usuario):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE usuario
                SET nombre = %s, cedula = %s, carrera = %s, semestre = %s, cargo = %s,
                    celular = %s, correo = %s, id_rol = %s
                WHERE id_usuario = %s
            """, (usuario.nombre, usuario.cedula, usuario.carrera, usuario.semestre,
                  usuario.cargo, usuario.celular, usuario.correo, usuario.id_rol, usuario_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {"resultado": "Usuario actualizado"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def delete_usuario(self, usuario_id: int):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            # Obtener datos ANTES de eliminar para el correo
            cursor.execute(
                "SELECT nombre, cedula, cargo, correo FROM usuario WHERE id_usuario = %s",
                (usuario_id,)
            )
            usuario_data = cursor.fetchone()

            cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (usuario_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Notificar por correo
            if usuario_data:
                notify_usuario_eliminado(
                    correo_admin=usuario_data[3],
                    nombre_usuario=usuario_data[0],
                    cedula=usuario_data[1],
                    cargo=usuario_data[2] or "No especificado"
                )

            return {"resultado": "Usuario eliminado"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_usuarios_by_rol(self, rol_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuario WHERE id_rol = %s", (rol_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id_usuario': data[0], 'nombre': data[1], 'cedula': data[2],
                    'carrera': data[3], 'semestre': data[4], 'cargo': data[5],
                    'celular': data[6], 'correo': data[7], 'id_rol': data[8]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay usuarios con ese rol")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
