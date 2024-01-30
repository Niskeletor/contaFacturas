# Proyectos

# ContaFacturas

Es un script en Python diseñado para facilitar la sincronización y gestión de archivos entre servidores SMB (Server Message Block) y WebDAV (Web Distributed Authoring and Versioning). Especialmente útil para empresas que requieren automatizar la transferencia y el procesamiento de archivos PDF entre diferentes plataformas de almacenamiento.

## Características

- Conexión automática a servidores SMB y WebDAV.
- Transferencia y renombramiento de archivos PDF basados en condiciones específicas.
- Filtrado y manejo de archivos recursivamente en directorios de SMB.
- Registro detallado de operaciones para facilitar el seguimiento y la depuración.

## Requisitos

Lista de requisitos previos necesarios para ejecutar tu proyecto. Por ejemplo:

- Python 3.x
- Bibliotecas: `smb.SMBConnection`, `webdav3.client`

## Instalación

Instrucciones paso a paso para instalar y configurar tu proyecto. Por ejemplo:

```bash
git clone <url-de-tu-repositorio>
cd <nombre-de-tu-proyecto>
pip install -r requirements.txt

```

Antes de ejecutar el script, es necesario configurar las credenciales y rutas de los servidores SMB y WebDAV. Estos datos se deben proporcionar a través de un archivo `configuracion.json` o mediante variables de entorno.

Si se opta por la estructura de `configuracion.json`:

```bash
{
  "nombre_usuario": "usuario",
  "pass": "contraseña",
  "nombre_servidor": "nombreServidor",
  "nombre_cliente": "nombreCliente",
  "direccion_servidor": "direccionServidor",
  "base_webdav_path": "/ruta/base/webdav",
  "servicio_nombre": "nombreServicio",
  "ruta_compartida_tb": "/ruta/compartida",
  // ... otras configuraciones
}
```

Si se opta por las variables de entorno :

```bash
NOMBRE_USUARIO=Usuario@dominio.local
PASS=passwordUsuarioDominio
NOMBRE_SERVIDOR=Netbios
NOMBRE_CLIENTE=MiPC
DIRECCION_SERVIDOR=DireccionIPServidor
WEBDAV_HOSTNAME=https://nube.nexcloud.com/remote.php/dav/files/usuario/
WEBDAV_LOGIN=usuarioWebdav
WEBDAV_PASSWORD=passworduserWebdav
```

## Uso

Para ejecutar el script, usa el siguiente comando:

```python
python app.py
```

## Contribuir

Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor, haz un fork del repositorio y crea un pull request con tus cambios.

## Licencia

![Licencia MIT](https://img.shields.io/badge/license-MIT-green)

Este proyecto está licenciado bajo MIT, siéntete de hacer el cambio que necesites!
Espero que esto sea para ti una palanca de ayuda si estás comenzando con el scripting o con algún lenguaje de programación