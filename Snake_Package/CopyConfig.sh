#!/bin/bash

# Migrate Apache config files and clean up
[ -f "/etc/apache2/sites-available/000-bckault.bck" ] && \
    sudo cp /etc/apache2/sites-available/000-bckault.bck /etc/apache2/sites-available/000-bckault.conf && \
    sudo rm -f /etc/apache2/sites-available/000-bckault.bck

[ -f "/etc/apache2/ports.bck" ] && \
    sudo cp /etc/apache2/ports.bck /etc/apache2/ports.conf && \
    sudo rm -f /etc/apache2/ports.bck

[ -d "/var/www/bck/" ] && \
    sudo mv -f /var/www/bck/* /var/www/html/ && \
    sudo rm -rf /var/www/bck/

[ -f "/etc/apache2/apache2.bck" ] && \
    sudo cp /etc/apache2/apache2.bck /etc/apache2/apache2.conf && \
    sudo rm -f /etc/apache2/apache2.bck

exit 0