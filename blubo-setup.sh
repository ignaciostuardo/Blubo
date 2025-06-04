#!/bin/bash

# Actualización de los repositorios
echo "Actualizando los repositorios..."
sudo apt-get update

# Actualización de paquetes
echo "Actualizando los paquetes..."
sudo apt-get upgrade -y

# Instalación de Git
echo "Instalando Git..."
sudo apt-get install git -y

# Instalación de paquetes de Python
echo "Instalando setuptools..."
sudo pip3 install --upgrade setuptools

echo "Instalando RPi.GPIO..."
sudo pip3 install RPi.GPIO

echo "Instalando Adafruit Blinka..."
sudo pip3 install adafruit-blinka

echo "Instalando Adafruit CircuitPython ADS1x15..."
sudo pip3 install adafruit-circuitpython-ads1x15

echo "Instalando Adafruit IO..."
sudo pip3 install adafruit-io

# Instalación de pigpio
echo "Instalando pigpio..."
sudo apt-get install pigpio python3-pigpio -y

echo "Instalando smbus2..."
sudo pip3 install smbus2

# Creación del servicio pigpiod
echo "Creando el servicio pigpiod en Systemd..."
sudo bash -c 'cat <<EOF > /etc/systemd/system/pigpiod.service
[Unit]
Description=Daemon de pigpio
After=network.target syslog.target

[Service]
ExecStart=/usr/bin/pigpiod
ExecStop=/bin/systemctl kill pigpiod
Type=forking

[Install]
WantedBy=multi-user.target
EOF'

# Recargar Systemd, habilitar e iniciar pigpiod
echo "Recargando Systemd..."
sudo systemctl daemon-reload

echo "Habilitando el servicio pigpiod..."
sudo systemctl enable pigpiod

echo "Iniciando el servicio pigpiod..."
sudo systemctl start pigpiod

# Clonar el repositorio para el Access Point
echo "Clonando el repositorio wifi-connect-headless-rpi..."
git clone https://github.com/drkmsmithjr/wifi-connect-headless-rpi.git

# Cambiar al directorio del script
echo "Accediendo al directorio del script..."
cd wifi-connect-headless-rpi/scripts

# Ejecutar el script de instalación del Access Point
echo "Instalando el Access Point..."
sudo ./rpi_headless_wifi_install.sh

# Regresar al directorio anterior
cd ~

# Activar SSH, I2C, SPI y VNC
echo "Activando SSH..."
sudo systemctl enable ssh
sudo systemctl start ssh

echo "Activando I2C..."
sudo raspi-config nonint do_i2c 0

echo "Activando SPI..."
sudo raspi-config nonint do_spi 0

echo "Activando VNC..."
sudo raspi-config nonint do_vnc 0

# Instalación de Tailscale
echo "Instalando Tailscale..."
sudo apt-get install apt-transport-https -y
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.noarmor.gpg | sudo tee /usr/share/keyrings/tailscale-archive-keyring.gpg > /dev/null
curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.tailscale-keyring.list | sudo tee /etc/apt/sources.list.d/tailscale.list
sudo apt-get update
sudo apt-get install tailscale -y

# Mensaje para completar el registro de Tailscale
read -p "Visita la URL proporcionada por Tailscale para registrar tu dispositivo y escribe 'Y' cuando estés listo: " ready
if [ "$ready" == "Y" ] || [ "$ready" == "y" ]; then
    sudo tailscale up --accept-dns=false
fi

# Instalación de FTP Server
echo "Instalando servidor FTP (proftpd)..."
sudo apt install proftpd -y

# Configuración del archivo proftpd.conf
echo "Abriendo proftpd.conf para editar el nombre del servidor. Cambia la línea ServerName según tus preferencias y guarda el archivo."
sudo nano /etc/proftpd/proftpd.conf

# Recargar el servicio FTP
echo "Recargando el servicio FTP..."
sudo service proftpd reload

# Configuración de autoejecución de main.py
echo "Configurando autoejecución de main.py al inicio..."

# Detectar el directorio del usuario
USER_DIR=$(ls /home | grep blubo[0-9]*)
MAIN_PY_PATH="/home/$USER_DIR/blubo/V3/main.py"

# Verificar si el archivo main.py existe
if [ ! -f "$MAIN_PY_PATH" ]; then
    echo "El archivo main.py no se encuentra en $MAIN_PY_PATH."
    echo "Verifica la ubicación e intenta nuevamente."
    exit 1
fi

# Crear el archivo del servicio de Systemd
echo "Creando servicio para ejecutar main.py al inicio..."
sudo bash -c "cat <<EOF > /etc/systemd/system/mainpy.service
[Unit]
Description=Ejecutar main.py al inicio
After=network.target

[Service]
ExecStart=/usr/bin/python3 $MAIN_PY_PATH
WorkingDirectory=/home/$USER_DIR/blubo/V3
StandardOutput=inherit
StandardError=inherit
Restart=always
User=$USER
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF"

# Recargar Systemd y habilitar el servicio
echo "Recargando Systemd y habilitando el servicio..."
sudo systemctl daemon-reload
sudo systemctl enable mainpy.service

# Iniciar el servicio
echo "Iniciando el servicio main.py..."
sudo systemctl start mainpy.service

# Verificar el estado del servicio
echo "Verificando el estado del servicio..."
sudo systemctl status mainpy.service

# Mensaje final
echo "####Reinicia la Raspberry####"