Vagrant.require_version ">= 2.0.2"

Vagrant.configure(2) do |config|
  config.vm.box = "generic/ubuntu1804"
  config.vm.network "private_network", ip: "172.30.1.5"
  config.ssh.insert_key = false

  config.vm.synced_folder ".", "/vagrant", type: "rsync", rsync__exclude: ".git/"

  config.vm.provision "shell", inline: "apt-add-repository ppa:ansible/ansible && apt-get update && apt-get -y install ansible"

  config.vm.provision "ansible_local" do |ansible|
    ansible.compatibility_mode = "2.0"
    ansible.galaxy_role_file = "requirements.yml"
    ansible.playbook = "nas.yml"
    ansible.become = true
    ansible.raw_arguments = [
      "--extra-vars @tests/test.yml",
      "-vvv"
    ]
  end
end
