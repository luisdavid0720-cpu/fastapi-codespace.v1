import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.asignacion_responsable_model import Asignacion_responsable
from fastapi.encoders import jsonable_encoder
from services.email_service import notify_asignacion_responsable

class Asignacion_responsableController:

    def _get_campo(self, cursor, tabla, campo_id, campo_nombre, valor):
        try:
            cursor.execute(f"SELECT {campo_nombre} FROM {tabla} WHERE {campo_id} = %s", (valor,))
            row = cursor.fetchone()
            return row[0] if row else str(valor)
        except Exception:
            return str(valor)

    def create_asignacion_responsable(self, asignacion_responsable: Asignacion_responsable):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO asignacion_responsable (id_pqr, id_usuario, fecha_asignacion) 
            VALUES (%s, %s, %s)""", (asignacion_responsable.id_pqr, asignacion_responsable.id_usuario,
                                     asignacion_responsable.fecha_asignacion))
            conn.commit()

            # Obtener datos para notificar al responsable asignado
            cursor.execute(
                "SELECT nombre, correo FROM usuario WHERE id_usuario = %s",
                (asignacion_responsable.id_usuario,)
            )
            responsable = cursor.fetchone()

            cursor.execute(
                "SELECT p.descripcion, p.id_departamento, p.id_prioridad FROM pqr p WHERE p.id_pqr = %s",
                (asignacion_responsable.id_pqr,)
            )
            pqr_data = cursor.fetchone()

            if responsable and pqr_data:
                depto     = self._get_campo(cursor, "departamento", "id_departamento", "nombre", pqr_data[1])
                prioridad = self._get_campo(cursor, "prioridad",   "id_prioridad",   "nombre", pqr_data[2])
                notify_asignacion_responsable(
                    correo_responsable=responsable[1],
                    nombre_responsable=responsable[0],
                    id_pqr=asignacion_responsable.id_pqr,
                    descripcion_pqr=pqr_data[0],
                    departamento=depto,
                    prioridad=prioridad,
                    fecha_asignacion=str(asignacion_responsable.fecha_asignacion)
                )

            return {"resultado": "Asignacion_responsable creado"}
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_asignacion_responsable(self, asignacion_responsable_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asignacion_responsable WHERE id_asignacion = %s",
                           (asignacion_responsable_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Asignacion no encontrada")
            content = {
                'id_asignacion': result[0], 'id_pqr': result[1],
                'id_usuario': result[2], 'fecha_asignacion': result[3]
            }
            return jsonable_encoder(content)
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_asignacion_responsables(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asignacion_responsable")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id_asignacion': data[0], 'id_pqr': data[1],
                    'id_usuario': data[2], 'fecha_asignacion': data[3]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay asignaciones")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def update_asignacion_responsable(self, asignacion_responsable_id: int,
                                      asignacion_responsable: Asignacion_responsable):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE asignacion_responsable
                SET id_pqr = %s, id_usuario = %s, fecha_asignacion = %s 
                WHERE id_asignacion = %s
            """, (asignacion_responsable.id_pqr, asignacion_responsable.id_usuario,
                  asignacion_responsable.fecha_asignacion, asignacion_responsable_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Asignacion no encontrada")
            return {"resultado": "Asignacion_responsable actualizado"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def delete_asignacion_responsable(self, asignacion_responsable_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM asignacion_responsable WHERE id_asignacion = %s",
                           (asignacion_responsable_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Asignacion no encontrada")
            return {"resultado": "Asignacion_responsable eliminado"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    # Ver todas las PQRs asignadas a un responsable
    def get_asignaciones_by_usuario(self, usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asignacion_responsable WHERE id_usuario = %s ORDER BY fecha_asignacion DESC",
                           (usuario_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id_asignacion': data[0], 'id_pqr': data[1],
                    'id_usuario': data[2], 'fecha_asignacion': data[3]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay asignaciones para este usuario")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    # Ver quién está asignado a una PQR específica
    def get_asignacion_by_pqr(self, pqr_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asignacion_responsable WHERE id_pqr = %s", (pqr_id,))
            result = cursor.fetchone()
            if result:
                content = {
                    'id_asignacion': result[0], 'id_pqr': result[1],
                    'id_usuario': result[2], 'fecha_asignacion': result[3]
                }
                return jsonable_encoder(content)
            else:
                raise HTTPException(status_code=404, detail="No hay asignacion para esta PQR")
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()