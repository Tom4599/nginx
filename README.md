```
$ ansible-playbook ~/openshift-ansible/playbooks/prerequisites.yml
$ ansible-playbook ~/openshift-ansible/playbooks/deploy_cluster.yml
```
test
```
$ sudo docker run -d --restart=unless-stopped -p 80:80 -p 443:443 rancher/rancher
```
test2
```
sudo systemctl enable docker
```
