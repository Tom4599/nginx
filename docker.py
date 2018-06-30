# importation des librairies nécessaires
import os
import subprocess
import string
import base64

array_ssh_login = []

print ("\n******************************** Get namespaces *******************************************\n")


# Liste des namespaces non voulu
array_namespaces_non_voulu=["default","glusterfs","kube-public","kube-service-catalog","kube-system","logging","management-infra",
"openshift","openshift-ansible-service-broker","openshift-infra","openshift-node","openshift-template-service-broker","openshift-web-console"]


# Création de la commande pour avoir les namespaces
COMMAND = "kubectl get namespaces"

for namespace in array_namespaces_non_voulu:
    COMMAND=COMMAND + " | grep -v " + namespace

COMMAND += "| awk '{print $1}'"


# Execution de la commande et insertion dans un tableau
p = subprocess.Popen(COMMAND, stdout=subprocess.PIPE, shell=True)
(outputnamespace, err) = p.communicate()
array_namespace=outputnamespace.decode().split('\n')
del array_namespace[0]
del array_namespace[-1]
print (array_namespace)


print ("\n******************************** Get pods by namespace ***********************************\n")

#Création de la commande pour avoir les pods par namespace
COMMANDNAMESPACE="kubectl get pods --namespace="
COMMANDESECRET="kubectl get secret --namespace="
for namespace in array_namespace:
    COMMANDNAMESPACEFINALE=COMMANDNAMESPACE + namespace + " | awk '{print $1}'"

    print("\n************** NAMESPACE : " + namespace + " **************\n")

    # Execution de la commande et insertion dans un tableu
    p = subprocess.Popen(COMMANDNAMESPACEFINALE, stdout=subprocess.PIPE, shell=True)
    (outputpods, err) = p.communicate()
    array_pods=outputpods.decode().split('\n')
    outputpods=outputpods.decode()
    del array_pods[0]
    if outputpods != "":
        del array_pods[-1]
        ### Pour name sans les chiffres aléatoires à la fin ###
        array_new_name_pod = []

        for name in array_pods:
            array_name_pod = name.split('-')
            del array_name_pod[-1]
            del array_name_pod[-1]
            name_pod = '-'.join(array_name_pod)
            array_new_name_pod.append(name_pod)

    print (array_new_name_pod)

    for new_name_pod in array_new_name_pod:
        futur_ssh_login=namespace + "-" + new_name_pod
        secret_possible=futur_ssh_login+"-secret"

        COMMANDSECRETFINALE=COMMANDESECRET + namespace + " | awk '{print $1}' | grep " + secret_possible

        # Execution de la commande et insertion dans un tableu
        p = subprocess.Popen(COMMANDSECRETFINALE, stdout=subprocess.PIPE, shell=True)
        (outputsecret, err) = p.communicate()
        array_secret=outputsecret.decode().split('\n')
        if array_secret == ['']:
            ssh_login=namespace + "-" + new_name_pod
            os.environ['loginname'] = ssh_login
            os.environ["login"] = base64.b64encode(ssh_login.encode('UTF-8')).decode('ascii')

            COMMANDEPASS = "pwgen -cB -1 10 -H /dev/null#" + namespace
            p = subprocess.Popen(COMMANDEPASS, stdout=subprocess.PIPE, shell=True)
            (outputpass, err) = p.communicate()
            ssh_password=outputpass.decode()
            os.environ["password"] = base64.b64encode(ssh_password.encode('UTF-8')).decode('ascii')

            ssh_key="ssh-rsa AAAAB3NzaC1y[.........]U4g1A4ciLOicjHV1KkaOpGLsvRCyE7 support@sudokeys.com"
            os.environ["key"] = base64.b64encode(ssh_key.encode('UTF-8')).decode('ascii')

            p = subprocess.Popen("envtpl templatesecret.yaml --output-file secret.yaml --keep-template --allow-missing", stdout=subprocess.PIPE, shell=True)
            p = subprocess.Popen("kubectl create --namespace="+namespace+" -f secret.yaml", stdout=subprocess.PIPE, shell=True)

            print("Secret créé")

        else:
            print("Secret déjà existant")
