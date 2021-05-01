# JukeHome-BackEnd

# Compil

pip3 install -r requirement.txt

# Configure MariaDB first time

sudo systemctl start mariadb
sudo mariadb
CREATE USER IF NOT EXISTS devs IDENTIFIED BY 'P@5s';
GRANT ALL PRIVILEGES ON *.* TO 'devs' IDENTIFIED BY 'P@5s';
exit;
mariadb -u devs -p

# Execute

./createTable.py

# or

python3 createTable.py
