#!/bin/bash


if [ -f "/etc/apache2/ports.bck" ]; then
    sudo cp /etc/apache2/ports.bck /etc/apache2/ports.conf
    sudo rm -f /etc/apache2/ports.bck

fi


if [ -d "/var/www/bck/" ]; then
    sudo mv -f /var/www/bck/* /var/www/html/ 2>/dev/null
    sudo rm -rf /var/www/bck/

fi

if [ -f "/etc/apache2/apache2.bck" ]; then
    sudo cp /etc/apache2/apache2.bck /etc/apache2/apache2.conf
    sudo rm -f /etc/apache2/apache2.bck

fi
#!/bin/bash

CONFIG_DIR="/etc/apache2/sites-available"

# Delete all .conf files
sudo find "$CONFIG_DIR" -type f -name "*.conf" -exec rm -f {} \;

# Copy .bck files to .conf
for file in "$CONFIG_DIR"/*.bck; do
    if [ -f "$file" ]; then
        sudo cp "$file" "${file%.bck}.conf"
        sudo rm -f "$file"
    fi
done


TARGET_PATHS=(
    "Snake_Package/VirtualHostFile"
    "Snake_Package/sites"
    "Snake_Package/SSLCertificate"
    "Snake_config"
)

find / -type d \( \
    -name "VirtualHostFile" \
    -o -name "sites" \
    -o -name "SSLCertificate" \
    -o -name "Snake_config" \
\) 2>/dev/null | while read -r target; do
    for valid_path in "${TARGET_PATHS[@]}"; do
        if [[ "$target" == *"$valid_path" ]]; then
            sudo rm -rf "$target"
            break
        fi
    done
done
exit 0
