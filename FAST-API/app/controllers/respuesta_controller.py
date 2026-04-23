import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.respuesta_model import Respuesta
from fastapi.encoders import jsonable_encoder
from services.email_service import notify_respuesta_pqr

class RespuestaController:

    def create_respuesta(self, respuesta: Respuesta):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO respuesta (mensaje,fecha,id_pqr,id_usuario) VALUES (%s, %s, %s, %s)",
                (respuesta.mensaje, respuesta.fecha, respuesta.id_pqr, respuesta.id_usuario)
            )
            conn.commit()

            # Obtener correo del dueño de la PQR y nombre del responsable que responde
            cursor.execute(
                "SELECT p.id_usuario FROM pqr p WHERE p.id_pqr = %s",
                (respuesta.id_pqr,)
            )
            pqr_row = cursor.fetchone()

            cursor.execute(
                "SELECT nombre FROM usuario WHERE id_usuario = %s",
                (respuesta.id_usuario,)
            )
            responsable_row = cursor.fetchone()

            if pqr_row:
                cursor.execute(
                    "SELECT nombre, correo FROM usuario WHERE id_usuario = %s",
                    (pqr_row[0],)
                )
                dueno = cursor.fetchone()
                if dueno and dueno[1]:
                    notify_respuesta_pqr(
                        correo_usuario=dueno[1],
                        nombre_usuario=dueno[0] or "Usuario",
                        id_pqr=respuesta.id_pqr,
                        mensaje_respuesta=respuesta.mensaje,
                        nombre_responsable=responsable_row[0] if responsable_row else "Responsable"
                    )

            return {"resultado": "Respuesta creado"}
        except psycopg2.Error as err:
            conn.rollback()
            print(err)
        finally:
            conn.close()

    def get_respuesta(self, respuesta_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM respuesta WHERE id_respuesta = %s", (respuesta_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Respuesta no encontrada")
            content = {
                'id_respuesta': int(result[0]), 'mensaje': result[1],
                'fecha': result[2], 'id_pqr': result[3], 'id_usuario': result[4]
            }
            return jsonable_encoder(content)
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_respuestas(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM respuesta")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id_respuesta': data[0], 'mensaje': data[1],
                    'fecha': data[2], 'id_pqr': data[3], 'id_usuario': data[4]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay respuestas")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def update_respuesta(self, respuesta_id: int, respuesta: Respuesta):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE respuesta
                SET mensaje = %s, fecha = %s, id_pqr = %s, id_usuario = %s
                WHERE id_respuesta = %s
            """, (respuesta.mensaje, respuesta.fecha, respuesta.id_pqr,
                  respuesta.id_usuario, respuesta_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Respuesta no encontrada")
            return {"resultado": "Respuesta actualizada"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def delete_respuesta(self, respuesta_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM respuesta WHERE id_respuesta = %s", (respuesta_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Respuesta no encontrada")
            return {"resultado": "Respuesta eliminada"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_respuestas_by_pqr(self, pqr_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM respuesta WHERE id_pqr = %s ORDER BY fecha ASC", (pqr_id,))
            result = cursor.fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="No hay respuestas para esta PQR")
            payload = []
            for data in result:
                content = {
                    'id_respuesta': data[0], 'mensaje': data[1],
                    'fecha': data[2], 'id_pqr': data[3], 'id_usuario': data[4]
                }
                payload.append(content)
            return {"resultado": jsonable_encoder(payload)}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_respuestas_by_usuario(self, usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM respuesta WHERE id_usuario = %s ORDER BY fecha DESC",
                           (usuario_id,))
            result = cursor.fetchall()
            if not result:
                raise HTTPException(status_code=404, detail="No hay respuestas de este usuario")
            payload = []
            for data in result:
                content = {
                    'id_respuesta': data[0], 'mensaje': data[1],
                    'fecha': data[2], 'id_pqr': data[3], 'id_usuario': data[4]
                }
                payload.append(content)
            return {"resultado": jsonable_encoder(payload)}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()
