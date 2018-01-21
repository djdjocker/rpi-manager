#Install startx and python deps
apt-get install -y xinit python-pyqt5 python-pyqt5.qtwebkit

#Install last node js
wget https://nodejs.org/dist/v9.3.0/node-v9.3.0-linux-armv6l.tar.xz
xz -d node-v9.3.0-linux-armv6l.tar.xz
tar -xf node-v9.3.0-linux-armv6l.tar

cd node-v9.3.0-linux-armv6l/
sudo rsync -av --exclude="*.md" --exclude="LICENSE" /usr/local/
# ou 
#mv node-v9.3.0-linux-armv6l node
#sed -i "$ a \
#if [ -d \"\$HOME/node\" ] ; then \
#    PATH=\"\$HOME/node/bin:\$PATH\" \
#fi" .profile

sudo reboot