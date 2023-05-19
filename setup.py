from cx_Freeze import setup, Executable

# Informe o nome do seu arquivo Python principal aqui
# Se houver mais de um arquivo, você pode adicionar todos na lista
executables = [Executable("camera.py")]

setup(
    name="camera_app",
    version="1.0",
    description="Despython setup.py buildcrição do executável",
    executables=executables
)