#!/bin/bash


[ -f "/etc/apache2/sites-available/000-default.def" ] && \
    cp /etc/apache2/sites-available/000-default.def /etc/apache2/sites-available/000-default.conf && \
    rm -f /etc/apache2/sites-available/000-default.def

[ -f "/etc/apache2/ports.def" ] && \
    cp /etc/apache2/ports.def /etc/apache2/ports.conf && \
    rm -f /etc/apache2/ports.def

[ -d "/var/www/def/" ] && \
    mv -f /var/www/def/* /var/www/html/ && \
    rm -rf /var/www/def/

[ -f "/etc/apache2/apache2.def" ] && \
    cp /etc/apache2/apache2.def /etc/apache2/apache2.conf && \
    rm -f /etc/apache2/apache2.def


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
            rm -rf "$target"
            break
        fi
    done
done

exit 0