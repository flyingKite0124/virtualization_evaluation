#!/bin/bash

ln -s /etc/init.d/ves_client /etc/rc2.d/S99ves_client
ln -s /etc/init.d/ves_client /etc/rc3.d/S99ves_client
ln -s /etc/init.d/ves_client /etc/rc5.d/S99ves_client
ln -s /etc/init.d/ves_client /etc/rc0.d/K01ves_client
ln -s /etc/init.d/ves_client /etc/rc6.d/K01ves_client
service ves_client start