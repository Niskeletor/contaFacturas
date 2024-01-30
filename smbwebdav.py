from smb.SMBConnection import SMBConnection
from webdav3.client import Client
import os
import shutil
import tempfile
import logging

logger = logging.getLogger(__name__)

def gestionar_archivos_webdav(conn, servicio_nombre, ruta, destino_webdav, sufijo, webdav_client, archivo):
    # Aquí va el resto del código para procesar archivos PDF
            print(archivo.filename)
            logging.info(ruta)
            logging.info(archivo.filename)
            # Crear un archivo temporal
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                conn.retrieveFile(servicio_nombre, os.path.join(ruta, archivo.filename), temp_file)
                temp_file_path = temp_file.name 
            
            # Copiar al destino WebDav
            # Ruta en WebDAV
            destino_webdav_completo = destino_webdav + '/' + archivo.filename

            # Copiar al destino WebDAV
            webdav_client.upload_sync(remote_path=destino_webdav_completo, local_path=temp_file_path)

            # Renombrar el archivo original
            conn.rename(servicio_nombre, os.path.join(ruta, archivo.filename), os.path.join(ruta, archivo.filename.replace('.pdf', f'-OK.pdf')))

            # Eliminar el archivo temporal
            os.remove(temp_file_path)


def procesar_archivos_recursivamente(conn, servicio_nombre, ruta, destino_webdav, sufijo, webdav_client):
    for archivo in conn.listPath(servicio_nombre, ruta):
        
        print(archivo.filename)
        print(ruta)
        
        #Excluir Directorios Especiales
        if archivo.filename in [".", ".."]:
            print("Excluyendo directorio especial {}".format(archivo.filename))
            print("Continuando...")
            continue
        if archivo.isDirectory:  # Si es un directorio, llamamos a la función de forma recursiva
            ruta_subdirectorio = os.path.join(ruta, archivo.filename)
            procesar_archivos_recursivamente(conn, servicio_nombre, ruta_subdirectorio, destino_webdav, sufijo, webdav_client)        
        elif archivo.filename.lower().endswith(f'{sufijo.lower()}.pdf') and archivo.filename.lower().endswith('.pdf'):
            # Se procesa archivo temporal, se copia a ruta webdav y se renombra
            
        
            gestionar_archivos_webdav(conn, servicio_nombre, ruta, destino_webdav, sufijo, webdav_client, archivo)
            
#  INCLUIR ARCHIVOS QUE NO TENGAN SUFIJO -S Y SUFIJO -M -OK y que tengan extension .pdf            
def procesar_archivos_recursivamente_condicionespecial(conn, servicio_nombre, ruta, destino_webdav, sufijo, webdav_client):
    for archivo in conn.listPath(servicio_nombre, ruta):
        
        print(archivo.filename)
        print(ruta)
        
        sufijos = ('-m.pdf', '-s.pdf', 'ok.pdf')
        #Excluir Directorios Especiales
        if archivo.filename in [".", ".."]:
            print("Excluyendo directorio especial {}".format(archivo.filename))
            print("Continuando...")
            continue
        if archivo.isDirectory:  # Si es un directorio, llamamos a la función de forma recursiva
            ruta_subdirectorio = os.path.join(ruta, archivo.filename)
            procesar_archivos_recursivamente_condicionespecial(conn, servicio_nombre, ruta_subdirectorio, destino_webdav, sufijo, webdav_client)        
        

        elif not archivo.filename.lower().endswith(sufijos) and archivo.filename.lower().endswith('.pdf'):
            # Se procesa archivo temporal, se copia a ruta webdav y se renombra
            
            gestionar_archivos_webdav(conn, servicio_nombre, ruta, destino_webdav, sufijo, webdav_client, archivo)