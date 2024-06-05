# Message_broker_using_python

Este proyecto es un message broker utilizando gRPC y Tkinter para la interfaz gráfica de usuario. A continuación se detallan los pasos para configurar el entorno y ejecutar el proyecto.

## Requisitos previos

Asegúrese de tener instalado lo siguiente en tu sistema:
- Python3
- pip (el gestor de paquetes de Python)

## Configuración del entorno

Sigua los siguientes pasos para configurar el entorno virtual y las dependencias necesarias:

1. Clone el repositorio y navegue al directorio del proyecto:
   ```sh
   cd Proyecto_2_SO
   
2. Crea un entorno virtual:
    ```sh
    python3 -m venv myenv
    
3. Active el entorno virtual:
     ```sh
     source env/bin/activate
4. Actualice el gestor de paquetes pip e instala las dependencias necesarias:
    ```sh
    sudo apt update
    sudo apt install python3-pip
5. Instale las bibliotecas necesarias:
   ```sh   
    pip install grpcio
    pip install grpcio-tools

6. Instale Tkinter:
   En Ubuntu/Debian:
    ```sh
     sudo apt-get install python3-tk

## Ejecutar el servidor
1. Dentro del entorno virtual se procede a ejecutar el servidor:
   ```sh
   python server.py
   
## Ejecutar el cliente

En cada terminal para ejecutar clientes se procede a hacer lo siguiente:

1. Navegue al directorio del proyecto
     ```sh
     cd Proyecto_2_SO
     
2. Active el entorno virtual:
     ```sh
     source env/bin/activate
     
3. Ejecute el cliente:
   ```sh
     python3 client.py
