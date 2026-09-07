#!/bin/bash 
#os weiss nun, dass dies mit bash ausgefuehrt wird, es wird der pfad als path, genommen, von
#wo das script gestartet wird, nicht wo es abgespeichert ist

set -e                                                  #Skript sofort abbrechen, wenn ein Befehl fehlschlaegt.
AGENTIMAGE="agent-image:1.0"
DEBUGIMAGE="debug-image:1.0"


echo "=== Checking Minikube ==="
if ! minikube status >/dev/null 2>&1; then
    echo "Minikube is not running. Starting..."
    minikube start
fi

echo "=== 2. Removing old Kubernetes resources ==="
kubectl delete -f k8s/ --ignore-not-found=true

echo "=== 3. Removing old image from Minikube ==="
minikube image rm "$AGENTIMAGE" 2>/dev/null || true
minikube image rm "$DEBUGIMAGE" 2>/dev/null || true

echo "=== 4. Removing old local Docker image ==="
docker image rm "$AGENTIMAGE" 2>/dev/null || true
docker image rm "$DEBUGIMAGE" 2>/dev/null || true

echo "=== 5. Building new image ==="
docker build -f Dockerfile.agent -t "$AGENTIMAGE" .               #baut image aus dockerfile
docker build -f Dockerfile.debug -t "$DEBUGIMAGE" .

echo "=== Loading image into Minikube ==="
minikube image load "$AGENTIMAGE"                                #laedt Image in minikube cluster
minikube image load "$DEBUGIMAGE"

echo "=== Applying Kubernetes manifests ==="
kubectl apply -f k8s/                                           #Kubernetes soll alle YAML-Manifeste im Ordner k8s/ anwenden.

echo "=== Waiting for deployments ==="
kubectl rollout status deployment/agent-alpha                   #Das prueft, ob das Deployment agent-alpha erfolgreich ausgerollt wurde.
kubectl rollout status deployment/agent-beta  
#kubectl exec deployment/agent-alpha -- env


echo "=== Agent logs ==="
kubectl logs -f deployment/agent-alpha --all-containers=true &  # & heisst: Starte diesen Prozess im Hintergrund und fahre mit der naechsten Zeile des Skripts fort.
kubectl logs -f deployment/agent-beta &

wait                                                            #Warte auf die im Hintergrund gestarteten Prozesse