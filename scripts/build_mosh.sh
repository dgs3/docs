#!/bin/sh

# This script builds mosh (since ssh + tmux fails), and adds mosh's required
# ports to /sbin/iptables

PROTOBUF="protobuf-2.5.0"
PROTO_EXT=".tar.bz2"
wget https://protobuf.googlecode.com/files/$PROTOBUF$PROTO_EXT
tar -xf $PROTOBUF$PROTO_EXT
cd $PROTOBUF
./configure
make
make install

cd ..

MOSH=mosh-1.2.4
MOSH_EXT=.tar.gz
wget http://mosh.mit.edu/$MOSH$MOSH_EXT
tar -xf $MOSH$MOSH_EXT
cd $MOSH
LD_LIBRARY_PATH=/usr/local/lib PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./configure
LD_LIBRARY_PATH=/usr/local/lib PKG_CONFIG_PATH=/usr/local/lib/pkgconfig make
make install

cd ..

iptables -I INPUT 1 --proto udp --match udp --match multiport --dports 60000:61000 -j ACCEPT
service iptables save
service iptables restart

echo "/usr/local/lib" >> /etc/ld.so.conf
ldconfig
