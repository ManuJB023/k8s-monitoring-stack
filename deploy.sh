#!/usr/bin/env bash
set -euo pipefail

echo "==> Creating kind cluster..."
kind create cluster --config cluster/kind-config.yaml --wait 60s

echo "==> Adding Helm repos..."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

echo "==> Creating monitoring namespace..."
kubectl create namespace monitoring

echo "==> Installing kube-prometheus-stack..."
helm install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --values helm/prometheus-stack/values.yaml \
  --wait

echo "==> Stack ready. Run:"
echo "    kubectl port-forward svc/kube-prometheus-stack-grafana 3000:80 -n monitoring"
echo "    Then open http://localhost:3000 (admin / prom-operator)"
