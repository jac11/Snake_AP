#!/bin/bash

if [ -f /etc/apache2/sites-available/000-default.conf ]; then
    sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.bck
    sudo cp /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sites-available/default-ssl.bck
fi
if [ -f /etc/apache2/ports.conf ]; then
    sudo cp /etc/apache2/ports.conf /etc/apache2/ports.bck  
fi
BACKUP_DIR="/var/www/bck/"
if [ ! -d "$BACKUP_DIR" ]; then
    sudo mkdir -p "$BACKUP_DIR"
fi
sudo cp -rf /var/www/html/* "$BACKUP_DIR"

if [ -f /etc/apache2/apache2.conf ]; then
    sudo cp /etc/apache2/apache2.conf /etc/apache2/apache2.bck
fi

exit 0
