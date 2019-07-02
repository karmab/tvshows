yum -y install mariadb-server
sed -i '/\[server\]/a  bind-address=0.0.0.0' /etc/my.cnf.d/server.cnf
systemctl enable --now mariadb
