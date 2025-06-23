Tecnologías utilizadas:
Python, Django,Bootstrap.

REQUISITOS PREVIOS 
Antes de comenzar, asegúrate de tener lo siguiente instalado en tu sistema:
Python 3.8+
pip (gestor de paquetes de Python)

1. Clonar el repositorio
git clone https://github.com/MontseDlg/SNAKE.git
cd SNAKE

2. Crear entorno virtual
python3 -m venv config

3. Activar el entorno virtual
source config/bin/acticate

4. Instalar paquetes necesarios
pip install -r requirements.txt

5. Crear un archivo .env con los datos de la base de datos
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_HOST=''
DB_PORT=''

6. Ejecutar la aplicación
python3 manage.py runserver 9001
