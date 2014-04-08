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
PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./configure
make
make install

cd ..

iptables -A INPUT --proto udp --match udp --match multiport --dports 60000:61000 -j ACCEPT

echo "/usr/local/lib" >> /etc/ld.so.conf
