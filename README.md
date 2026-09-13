# IntegralTUI

Aplicación de Terminal User Interface (TUI) para consultar los datos académicos del sistema **Integral** de la **FIUNI** (Facultad de Ingeniería de la Universidad Nacional de Itapúa).

Permite visualizar en la terminal las materias favoritas del estudiante, sus tareas (homework) y la asistencia a clases, consumiendo la API pública de IntegralFIUNI.

## Requisitos

- Python >= 3.13
- Docker (opcional, solo para el despliegue con contenedores)

## Configuración

Copia el archivo `.env.example` a `.env` y ajusta los valores según corresponda:

```bash
cp .env.example .env
```

| Variable                  | Descripción                                                                 |
| ------------------------- | --------------------------------------------------------------------------- |
| `BASE_URL_INTEGRALFIUNI`  | URL base de la API de IntegralFIUNI.                                        |
| `SSH_PASSWORD`            | Contraseña del usuario en el contenedor SSH. Vacía = sin contraseña         |
| `DEBUG_MODE`              | `1` para activar el modo debug, cualquier otro valor para desactivarlo.     |
| `MAIL`                    | Email del estudiante (solo se usa con el modo debug activado).              |
| `PASSWORD`                | Contraseña del estudiante (solo se usa con el modo debug activado).         |

## Ejecución en local

1. Crea y activa un entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta la aplicación:

   ```bash
   python main.py
   ```

Sin el modo debug, la aplicación te pedirá tu email y contraseña de Integral para iniciar sesión.

### Compilar un binario ejecutable (opcional)

Si tienes instalado `pyinstaller`, puedes generar un binario independiente con:

```bash
pyinstaller main.spec
```

El ejecutable resultante se genera en `dist/`.

## Despliegue con Docker

La imagen construye el contenedor con un servidor OpenSSH que ejecuta la TUI como shell forzada (`ForceCommand`). El acceso se realiza mediante **SSH** por el puerto `2222`.

1. Construye la imagen y levanta el contenedor:

   ```bash
   docker compose up --build
   ```

2. También puedes ejecutarlo directamente con `docker run`:

   ```bash
   docker build -t integral-tui .
   docker run --env-file .env -p 2222:2222 integral-tui
   ```

## Conexión por SSH

Con el contenedor en ejecución, conéctate como el usuario `integral` usando la contraseña definida en `SSH_PASSWORD`:

```bash
ssh -p 2222 integral@localhost
```

Por ejemplo, si la contraseña configurada es `mi-clave`:

```bash
ssh -p 2222 integral@localhost
# y escribes la contraseña cuando la pida
```

Al conectarte, la TUI de Integral se iniciará automáticamente.

> **Nota:** el despliegue con Docker no está muy testeado. Úsalo con cuidado y con expectativas bajas.
