# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    # Every Vagrant virtual environment requires a box to build off of.
    config.vm.box = "chef/centos-7.0"
    config.vm.boot_timeout = 30

    # SSH agent forwarding makes life easier
    config.ssh.forward_agent = true

    # Configure Salt stack
    config.vm.provision :salt do |config|
        config.install_type = 'stable'
    end

    # Define the vm
    vm_name = "botdev"
    config.vm.define :botdev do |botdev|
        botdev.vm.network :private_network, ip: "172.30.30.30"
        botdev.vm.hostname = vm_name

        botdev.vm.synced_folder "salt/roots/", "/srv/"
        botdev.vm.synced_folder ".",           "/src/"

        # botdev.vm.network :forwarded_port, guest: 22, host: 22, auto_correct: true

        botdev.vm.provider "virtualbox" do |v|
            v.name = vm_name
            v.customize ["modifyvm", :id, "--memory", "256"]
        end

        botdev.vm.provision :salt do |config|
            config.minion_config = "salt/minion.conf"
            config.run_highstate = true
            config.verbose = true
            config.bootstrap_options = "-D"
            config.temp_config_dir = "/tmp"
        end
    end
end
