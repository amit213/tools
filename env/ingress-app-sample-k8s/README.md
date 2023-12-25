


1) deploy k8s

2) install nginx-ingress for baremetal

https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/baremetal/deploy.yaml

Ref https://medium.com/@cagri.ersen/kubernetes-nginx-ingress-controller-for-on-premise-environments-e64ee3aa04e


3) install apple and banana sample apps

kubectl apply -f apple.yaml and banana.yaml

ref https://matthewpalmer.net/kubernetes-app-developer/articles/kubernetes-ingress-guide-nginx-example.html


4) install ingress for the app specific 


https://matthewpalmer.net/kubernetes-app-developer/articles/kubernetes-ingress-guide-nginx-example.html

kubectl apply -f app-specific-ingress.yaml

NS=apps envsubst < ingress.yml | kubectl apply -f -


https://aws.amazon.com/blogs/containers/exposing-kubernetes-applications-part-3-nginx-ingress-controller/

curl localhost:8080/first -H 'Host: a.example.com'
curl localhost:8080/second -H 'Host: b.example.com'
curl localhost:8080/first -H 'Host: b.example.com'
curl localhost:8080/first -H 'Host: b.example.net'


