#!/bin/bash -xe

APT_INSTALL_ARGS="--yes --force-yes"
apt_install()
{
	DEBIAN_FRONTEND=noninteractive apt-get install $APT_INSTALL_ARGS $*
}

GEM_ARGS="--no-rdoc --no-ri"
install_chef()
{
    chef_binary=/var/lib/gems/1.9.1/gems/chef-0.10.4/bin/chef-solo

    # Are we on a vanilla system?
    if ! test -f "$chef_binary"; then
        apt_install ruby1.8 ruby1.8-dev curl make
        cd /tmp
        curl -O http://production.cf.rubygems.org/rubygems/rubygems-1.8.10.tgz
        tar zxf rubygems-1.8.10.tgz
        cd rubygems-1.8.10
        ruby setup.rb --no-format-executable
        gem install $GEM_ARGS chef && gem install $GEM_ARGS moneta -v '~> 0.6.0' && gem uninstall moneta -v '>= 0.7.0'
        mkdir -p -m 0777 /var/chef
    fi

}

disable_network_manager()
{
    sed -ie "s/^dns/#dns/" /etc/NetworkManager/NetworkManager.conf
    restart network-manager
    cat << EOF > /etc/network/interfaces
auto lo eth0 eth1
iface lo inet loopback
iface eth0 inet dhcp
iface eth1 inet static
    address 10.0.0.1
    netmask 255.255.255.0
EOF
    service networking restart

}
if [[ $UID != 0 ]];
then
	echo "please run as root"
	exit 1
fi


disable_network_manager
install_chef
echo "deb http://apt.opscode.com/ precise-0.10 main" | tee /etc/apt/sources.list.d/opscode.list

mkdir -p /etc/apt/trusted.gpg.d
gpg --keyserver keys.gnupg.net --recv-keys 83EF826A
gpg --export packages@opscode.com | tee /etc/apt/trusted.gpg.d/opscode-keyring.gpg &>/dev/null

apt-get update

echo "chef	chef/chef_server_url	string	chefserver.cloud.arcticwolf.biz:446" | debconf-set-selections
apt_install aptitude vim  openssh-server debconf-utils


