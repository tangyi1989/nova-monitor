
echo "--------------------------------------"
echo "lidesheng: Hi!This program is desgined by Li Desheng."
echo "Now I will guide you to install nginx,configure nginx and run nginx.Then....!"
echo "--------------------------------------"
echo "lidesheng: 1.1 Add the source to /etc/apt/sources.list."
echo "deb http://nginx.org/packages/ubuntu/ codename nginx"
echo "deb-src http://nginx.org/packages/ubuntu/ codename nginx."
read -p "Please press [Enter]..." yn
vim /etc/apt/sources.list

read -p "lidesheng: 1.2 run [apt-get update] and [apt-get install nginx].Please press [Enter]..." yn

apt-get update
apt-get install nginx

