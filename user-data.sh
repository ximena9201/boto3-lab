#!/bin/bash
DOMAIN=sb.anacondaconnect.com
LOCAL_IP=$(/usr/bin/curl -s  http://169.254.169.254/latest/meta-data/local-ipv4 | cut -d = -f 2)

FQDN=$LOCAL_IP.$DOMAIN
echo $FQDN > /etc/hostname

cat >/etc/hosts <<EOF
127.0.0.1 localhost localhost.localdomain localhost4 localhost4.localdomain4 ${FQDN}
::1 localhost6 localhost6.localdomain6 ${FQDN}
EOF
