# Etapes à suivre pour deployer un certificat let's encrypt sur un container rancher

1. Deployer le cert-manager, depuis le catalogue rancher.

2. Rendre le pod accesible de l'extérieur (avec ingress ou traefik) 

3. Lancer kubectl depuis le cluster et créer le fichier suivant : clusterissuer.yaml

```
apiVersion: certmanager.k8s.io/v1alpha1
kind: ClusterIssuer
metadata:
  name: letsencrypt-cluster
  namespace: default
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: tom@phosphore.si  # <= spécifier l'adresse email qui va recevoir des alertes concernant le certificat
    privateKeySecretRef:
      name: letsencrypt-cluster
    http01: {}

```

4. Lancer la commande suivante, qui permet de créer l'Issuer Cluster

`kubectl create -f clusterissuer.yaml`

Verifier que celui-ci est bien déployer avec la commande : 

`kubectl get clusterissuers --all-namespaces`

5. Créer ensuite le fichier suivant : certificate.yaml

```
apiVersion: certmanager.k8s.io/v1alpha1
kind: Certificate
metadata:
  name: odoo-generac-phosphore-si # <= nom du certificat, vous pouvez mettre nimporte quoi
  namespace: odootest2 # <= spécifier le namespace du pod qui va recevoir le certificat
spec:
  secretName: odoo-generac-phosphore-si-tls # <= nom du secret, vous pouvez mettre nimporte quoi
  issuerRef:
    kind: ClusterIssuer
    name: letsencrypt-cluster
  commonName: odoo.generac.phosphore.si # <= spécifier le nom de domaine qui va recevoir le certificat
  acme:
    config:
    - http01:
        ingressClass: nginx
      domains:
        - odoo.generac.phosphore.si # <= spécifier le nom de domaine qui va recevoir le certificat
```

6. Lancer la commande suivante, qui permet de créer le certificat

`kubectl create -f certificate.yaml`

Verifier que celui-ci est bien déployer avec la commande : 

`kubectl describe certificate <nom_du_certificat> --namespace=<namespace>`

Après 30sec environ relancez la dernière commande et si cela à fonctionner vous devriez voir :

```
Normal  IssueCert       32m   cert-manager  Issuing certificate...
Normal  CertObtained    32m   cert-manager  Obtained certificate from ACME server
Normal  CertIssued      32m   cert-manager  Certificate issued successfully 
```

Si vous ne voyez pas ceci allez voir les logs du conatiner cert-manager.

7. Vous pouvez maintenant voir votre certificat sur rancher dans l'onglet Ressources puis Certificats du project.

8. Dans l'onglet Load Balancing éditer votre règle en spécifiant le bon namespace, vous devriez pouvoir ajouter votre certificat dans l'onglet SSL/TLS Certificates et ajouter le nom de domaine en dessous 

## Problème connus :

Si vous obtenez l'erreur  http-01 self check failed for domain "<nom_de_domaine>"

Connecter vous au container cert-manager et faite un ping de votre nom de domaine, vous devez voir l'ip privée du master apparaître et non l'ip public.

													
