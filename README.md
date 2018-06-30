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
