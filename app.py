from smb.SMBConnection import SMBConnection
from webdav3.client import Client
import os
import shutil
import tempfile
from smbwebdav import procesar_archivos_recursivamente
from smbwebdav import procesar_archivos_recursivamente_condicionespecial
import json
import logging


# Declaracion de filtro para excluir mensajes específicos
class ExcludeSpecificLogFilter(logging.Filter):
    def filter(self, record):
        # Define la cadena que deseas excluir
        exclude_message = 'Authentication with remote machine'

        # Si el mensaje de log contiene la cadena, no lo registres
        return exclude_message not in record.getMessage()

# Configura el directorio donde se guardarán los logs
log_directory = "./logs"
os.makedirs(log_directory, exist_ok=True)

# Configura el logging
logging.basicConfig(filename=os.path.join(log_directory, 'contaFacturas.log'),
level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Crea un filtro para excluir mensajes específicos
exclude_filter = ExcludeSpecificLogFilter()
logging.getLogger().addFilter(exclude_filter)

smb_logger = logging.getLogger('SMB.SMBConnection')
smb_logger.addFilter(exclude_filter)


# Cargar las variables desde el archivo JSON
with open('configuracion.json') as f:
    data = json.load(f)

"""
Se pueden obtener los datos de JSON, pero se recomienda usar variables de entorno

nombre_usuario = data['nombre_usuario']
contraseña = data['pass']
nombre_servidor = data['nombre_servidor']
nombre_cliente = data['nombre_cliente']
direccion_servidor = data['direccion_servidor']

#Configuracion de conexion WebDav
options = data['options']

webdav_client = Client(options)
"""

# Intenta obtener las credenciales desde variables de entorno
nombre_usuario = os.getenv('NOMBRE_USUARIO')
contraseña = os.getenv('PASS')
nombre_servidor = os.getenv('NOMBRE_SERVIDOR')
nombre_cliente = os.getenv('NOMBRE_CLIENTE')
direccion_servidor = os.getenv('DIRECCION_SERVIDOR')

# Configuración de conexión WebDav
webdav_hostname = os.getenv('WEBDAV_HOSTNAME')
webdav_login = os.getenv('WEBDAV_LOGIN')
webdav_password = os.getenv('WEBDAV_PASSWORD')

options = {
    'webdav_hostname': webdav_hostname,
    'webdav_login': webdav_login,
    'webdav_password': webdav_password
}

webdav_client = Client(options)

try:
    # Conexión al servidor SMB
    print('Conectando...')
    logging.info('Conectando... Con servidor SMB')
    conn = SMBConnection(nombre_usuario, contraseña, nombre_cliente, nombre_servidor, use_ntlm_v2=True, is_direct_tcp=True)
    print('Conectando...2x')
    conn.connect(direccion_servidor, 445)
    print('Conectado')
    logging.info('Conectado a SMB')

    # Base de la ruta WebDAV (modifica según tu configuración de Nextcloud)
    base_webdav_path = data['base_webdav_path']
    # Rutas de los recursos compartidos y destino
    servicio_nombre = data['servicio_nombre']
    
         # RUTAS Empresa1
    ruta_compartida = data['ruta_compartida_tb']
    print(ruta_compartida)
    destino_m = data['destino_m_tb']
    print(destino_m)
    destino_s = data['destino_s_tb']
    print(destino_s)
    logging.info('Procesando archivos de la primera empresa')
    for ruta, dest_m, dest_s in zip(ruta_compartida, destino_m, destino_s):    
        
        procesar_archivos_recursivamente(conn, servicio_nombre, ruta, dest_m, '-M', webdav_client)
        procesar_archivos_recursivamente(conn, servicio_nombre, ruta, dest_s, '-S', webdav_client)

    # RUTAS Empresa2
    ruta_compartida = data['ruta_compartida_mg']
    destino_m = data['destino_m_mg']    
    destino_s = data['destino_s_mg']
    logging.info('Procesando archivos de de la segunda empresa')
    for ruta, dest_m, dest_s in zip(ruta_compartida, destino_m, destino_s):    
        
        procesar_archivos_recursivamente(conn, servicio_nombre, ruta, dest_m, '-M', webdav_client)
        procesar_archivos_recursivamente(conn, servicio_nombre, ruta, dest_s, '-S', webdav_client)
        
    # RUTAS Empresa3
    ruta_compartida = data['ruta_compartida_my']
    destino_m = data['destino_m_my']    
    destino_s = data['destino_s_my']
    destino_o = data['destino_o_my']
    logging.info('Procesando archivos de la tercera empresa con condicion especial')
    for ruta, dest_m, dest_s, dest_o in zip(ruta_compartida, destino_m, destino_s, destino_o):    
        
        procesar_archivos_recursivamente(conn, servicio_nombre, ruta, dest_m, '-M', webdav_client)
        procesar_archivos_recursivamente(conn, servicio_nombre, ruta, dest_s, '-S', webdav_client)
        procesar_archivos_recursivamente_condicionespecial(conn, servicio_nombre, ruta, dest_o, 'OK', webdav_client)    
except Exception as e:
    print(e)
    logging.error(e)

finally:
    # Cerrar la conexión
    if conn:
        conn.close()
        print('Conexión cerrada')
        logging.info('Conexión cerrada')
        logging.info('Conexión cerrada')
