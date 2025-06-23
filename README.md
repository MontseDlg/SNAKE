# SNAKE

### Tecnologías utilizadas:
- Python  
- Django  
- Bootstrap  

---

### REQUISITOS PREVIOS  
Antes de comenzar, asegúrate de tener lo siguiente instalado en tu sistema:  
- Python 3.8+  
- pip (gestor de paquetes de Python)

---

### Pasos para ejecutar el proyecto:

1. **Clona el repositorio:**
```sh
git clone https://github.com/MontseDlg/SNAKE.git
cd SNAKE
```

2. **Crea un entorno virtual:**
```sh
python3 -m venv config
```

3. **Activa el entorno virtual:**
```sh
source config/bin/activate

```

4. **Instala los paquetes necesarios:**
```sh
pip install -r requirements.txt
```

5. **Crea un archivo `.env`** con los datos de tu base de datos:
```dotenv
DB_NAME="tu_nombre_bd"
DB_USER="tu_usuario"
DB_PASSWORD="tu_contraseña"
DB_HOST="localhost"
DB_PORT="5432"
```

6. **Aplica las migraciones:**
```sh
python manage.py migrate
```

7. **Ejecuta la aplicación:**
```sh
python3 manage.py runserver 9001
```

---

