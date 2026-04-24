import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.pqr_model import Pqr
from fastapi.encoders import jsonable_encoder
from services.email_service import notify_pqr_creada, notify_cambio_estado_pqr

class PqrController:

    def _get_usuario_correo(self, cursor, id_usuario: int):
        try:
            cursor.execute("SELECT nombre, correo FROM usuario WHERE id_usuario = %s", (id_usuario,))
            row = cursor.fetchone()
            return (row[0], row[1]) if row else (None, None)
        except Exception:
            return (None, None)

    def _get_nombre(self, cursor, tabla: str, campo_id: str, campo_nombre: str, valor_id: int):
        try:
            cursor.execute(f"SELECT {campo_nombre} FROM {tabla} WHERE {campo_id} = %s", (valor_id,))
            row = cursor.fetchone()
            return row[0] if row else str(valor_id)
        except Exception:
            return str(valor_id)

    def create_pqr(self, pqr: Pqr):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pqr
            (descripcion,fecha,id_usuario,id_tipo,id_estado,id_departamento,id_prioridad)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            RETURNING id_pqr
        """, (
            pqr.descripcion,
            pqr.fecha,
            pqr.id_usuario,
            pqr.id_tipo,
            pqr.id_estado,
            pqr.id_departamento,
            pqr.id_prioridad
        ))

        nuevo_id = cursor.fetchone()[0]
        conn.commit()

        print("PQR creada:", nuevo_id)

        nombre_u, correo_u = self._get_usuario_correo(cursor, pqr.id_usuario)

        print("Usuario:", nombre_u)
        print("Correo:", correo_u)

        tipo = self._get_nombre(cursor, "tipo_pqr", "id_tipo", "nombre", pqr.id_tipo)
        depto = self._get_nombre(cursor, "departamento", "id_departamento", "nombre", pqr.id_departamento)

        print("Tipo:", tipo)
        print("Depto:", depto)

        if correo_u:
            notify_pqr_creada(
                correo_usuario=correo_u,
                nombre_usuario=nombre_u or "Usuario",
                id_pqr=nuevo_id,
                descripcion=pqr.descripcion,
                tipo=tipo,
                departamento=depto,
                fecha=str(pqr.fecha)
            )
            print("Correo enviado")
        else:
            print("No hay correo")

        return {"resultado": "PQR creada"}

    except Exception as e:
        print("ERROR CREATE PQR:", e)
        conn.rollback()

    finally:
        conn.close()

    def get_pqr(self, pqr_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pqr WHERE id_pqr = %s", (pqr_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Pqr no encontrada")
            content = {
                'id_pqr': result[0], 'descripcion': result[1], 'fecha': result[2],
                'id_usuario': result[3], 'id_tipo': result[4], 'id_estado': result[5],
                'id_departamento': result[6], 'id_prioridad': result[7]
            }
            return jsonable_encoder(content)
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def get_pqrs(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pqr")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id_pqr': data[0], 'descripcion': data[1], 'fecha': data[2],
                    'id_usuario': data[3], 'id_tipo': data[4], 'id_estado': data[5],
                    'id_departamento': data[6], 'id_prioridad': data[7]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay PQRs")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def update_pqr(self, pqr_id: int, pqr: Pqr):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pqr SET descripcion = %s, fecha = %s, id_usuario = %s, id_tipo = %s,
                id_estado = %s, id_departamento = %s, id_prioridad = %s WHERE id_pqr = %s
            """, (pqr.descripcion, pqr.fecha, pqr.id_usuario, pqr.id_tipo, pqr.id_estado,
                  pqr.id_departamento, pqr.id_prioridad, pqr_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Pqr no encontrado")
            return {"resultado": "Pqr actualizado"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    def delete_pqr(self, pqr_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pqr WHERE id_pqr = %s", (pqr_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Pqr no encontrado")
            return {"resultado": "Pqr eliminado"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    # Cambiar solo el estado de una PQR y notificar al usuario
    def update_estado_pqr(self, pqr_id: int, nuevo_estado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT p.id_usuario, p.id_estado, e.nombre FROM pqr p"
                " JOIN estado e ON e.id_estado = p.id_estado WHERE p.id_pqr = %s", (pqr_id,)
            )
            row = cursor.fetchone()
            id_usuario_pqr  = row[0] if row else None
            nombre_anterior = row[2] if row else "Desconocido"
            cursor.execute("UPDATE pqr SET id_estado = %s WHERE id_pqr = %s", (nuevo_estado_id, pqr_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="PQR no encontrada")
            cursor.execute("SELECT nombre FROM estado WHERE id_estado = %s", (nuevo_estado_id,))
            row_nuevo = cursor.fetchone()
            nombre_nuevo = row_nuevo[0] if row_nuevo else str(nuevo_estado_id)
            if id_usuario_pqr:
                nombre_u, correo_u = self._get_usuario_correo(cursor, id_usuario_pqr)
                if correo_u:
                    notify_cambio_estado_pqr(
                        correo_usuario=correo_u,
                        nombre_usuario=nombre_u or "Usuario",
                        id_pqr=pqr_id,
                        estado_anterior=nombre_anterior,
                        estado_nuevo=nombre_nuevo
                    )
            return {"resultado": "Estado de PQR actualizado"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    # Obtener todas las PQRs de un usuario
    def get_pqrs_by_usuario(self, usuario_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pqr WHERE id_usuario = %s", (usuario_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id_pqr': data[0], 'descripcion': data[1],
                    'fecha': data[2], 'id_usuario': data[3],
                    'id_tipo': data[4], 'id_estado': data[5],
                    'id_departamento': data[6], 'id_prioridad': data[7]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No se encontraron PQRs para este usuario")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    # Filtrar PQRs por estado
    def get_pqrs_by_estado(self, estado_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pqr WHERE id_estado = %s", (estado_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id_pqr': data[0], 'descripcion': data[1],
                    'fecha': data[2], 'id_usuario': data[3],
                    'id_tipo': data[4], 'id_estado': data[5],
                    'id_departamento': data[6], 'id_prioridad': data[7]
                }
                payload.append(content)
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay PQRs con ese estado")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    # Filtrar PQRs por departamento
    def get_pqrs_by_departamento(self, departamento_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pqr WHERE id_departamento = %s", (departamento_id,))
            result = cursor.fetchall()
            payload = [
                {'id_pqr': d[0], 'descripcion': d[1], 'fecha': d[2],
                 'id_usuario': d[3], 'id_tipo': d[4], 'id_estado': d[5],
                 'id_departamento': d[6], 'id_prioridad': d[7]} for d in result
            ]
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay PQRs para ese departamento")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()

    # Filtrar PQRs por prioridad
    def get_pqrs_by_prioridad(self, prioridad_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pqr WHERE id_prioridad = %s", (prioridad_id,))
            result = cursor.fetchall()
            payload = [
                {'id_pqr': d[0], 'descripcion': d[1], 'fecha': d[2],
                 'id_usuario': d[3], 'id_tipo': d[4], 'id_estado': d[5],
                 'id_departamento': d[6], 'id_prioridad': d[7]} for d in result
            ]
            if result:
                return {"resultado": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail="No hay PQRs con esa prioridad")
        except psycopg2.Error as err:
            print(err)
            conn.rollback()
        finally:
            conn.close()