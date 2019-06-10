---
title: vpn
copyright: true
date: 2019-06-10 21:52:10
categories: vpn
tags: vpn Shadowsocks 
---

The complete guide on how to set up your own personal Shadowsocks server in under 30 minutes!

ShadowSocks setup workflow
(Time commitment; 30+ minutes)

Step 1: Set up VPS Hosting on DigitalOcean or Vultr

Step 2: Login to VPS with SSH

Step 3: Install Shadowsocks onto VPS

Step 4: Download Shadowsocks client for devices

Step 5: Enter VPS server credentials into Shadowsocks client

Step 6: Connect to Shadowsocks server


sudo apt-get update


Now we are ready to move onto the real stuff.

1.) Update everything.

$ sudo apt-get update

2.) Install Shadowsocks with two commands.

$ sudo apt-get install python-pip

You will be presented with “Do you want to continue? [Y/n]”

Type capital Y and click enter.

$ sudo pip install shadowsocks


3.) Shadowsocks supports a number of encryption methods. For optimized performance, we suggest using the ChaCha20 encryption method. However, we need to install it first. Below are the commands to setup the ChaCha20 encryption. 

Enter the following commands one at a time, and make sure to wait until the command finishes before entering the next time.

$ apt-get install python-m2crypto

$ apt-get install build-essential

$ wget https://github.com/jedisct1/libsodium/releases/download/1.0.16/libsodium-1.0.16.tar.gz

$ tar xf libsodium-1.0.16.tar.gz && cd libsodium-1.0.16

$ ./configure && make -j2

$ make install

$ sudo ldconfig

If you are presented with the following screen, you have succeeded and are you are ready to proceed to the next step.

$ nano /etc/shadowsocks.json

{
    "server":"your_droplet's_IP_address",
    "server_port":8000,
    "local_port":1080,
    "password":"your_password",
    "timeout":600,
    "method":"aes-256-cfb"
}


5.) Next we need to configure the firewall to allow the port number 8000 to be used.

$ ufw allow 8000

$ ufw allow 22

Then enable the firewall

$ ufw enable

“Command may disrupt existing ssh connections. Proceed with operation (y|n)?” will appear. Click “Y + Enter” to accept.

Now we can check if the firewall allows port 8000

$ ufw status verbose

If you see the same thing as what is stated in the picture, your firewall is set up.


6.) Now we need to start our shadowsocks sever with this command.

$ ssserver -c /etc/shadowsocks.json -d start

If you see this message then it means you have succeeded.

In the future, if you want to stop the Shadowsocks server, use this command:

$ ssserver -c /etc/shadowsocks.json -d stop

If you want to restart the Shadowsocks server, use this command:

$ ssserver -c /etc/shadowsocks.json -d restart