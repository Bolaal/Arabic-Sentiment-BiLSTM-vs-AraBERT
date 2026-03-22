# Deployment Guide

Complete guide for deploying the Arabic Sentiment Analysis API to production environments.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Environment Variables](#environment-variables)
6. [Scaling](#scaling)
7. [Monitoring](#monitoring)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Tools
- **Docker** 20.10+ (for containerization)
- **docker-compose** 2.0+ (for local orchestration)
- **kubectl** 1.24+ (for Kubernetes deployment)
- **Kubernetes cluster** (EKS, GKE, AKS, or local)

### Optional Tools
- **Helm** 3.0+ (for advanced K8s deployments)
- **k9s** (Kubernetes cluster management)
- **Lens** (Kubernetes IDE)

---

## Local Development

### Option 1: Python Virtual Environment

```bash
# Clone repository
git clone https://github.com/Bolaal/Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT.git
cd Arabic-Sentiment-BiLSTM-vs-AraBERT

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run the API
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Access the API at: `http://localhost:8000`

### Option 2: Docker Compose (Recommended)

```bash
# Build and start the service
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop the service
docker-compose down
```

Access the API at: `http://localhost:8000`

---

## Docker Deployment

### Build Docker Image

```bash
# Build the image
docker build -t arabic-sentiment-api:latest -f Dockerfile .

# Verify the image
docker images | grep arabic-sentiment-api
```

### Run Container

```bash
# Run with default settings
docker run -d \
  --name arabic-sentiment-api \
  -p 8000:8000 \
  arabic-sentiment-api:latest

# Run with custom environment variables
docker run -d \
  --name arabic-sentiment-api \
  -p 8000:8000 \
  -e MODEL_NAME=Belall87/arabert-arabic-sentiment \
  -e WORKERS=2 \
  -e LOG_LEVEL=info \
  arabic-sentiment-api:latest

# View logs
docker logs -f arabic-sentiment-api

# Stop container
docker stop arabic-sentiment-api
docker rm arabic-sentiment-api
```

### Test the Deployment

```bash
# Health check
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "هذا المنتج رائع"}'
```

---

## Kubernetes Deployment

### Prerequisites

Ensure you have:
- A running Kubernetes cluster
- `kubectl` configured to access the cluster
- Docker image pushed to a container registry

### Push Image to Registry

```bash
# Tag for Docker Hub
docker tag arabic-sentiment-api:latest yourusername/arabic-sentiment-api:latest

# Push to Docker Hub
docker push yourusername/arabic-sentiment-api:latest

# Or tag for AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker tag arabic-sentiment-api:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/arabic-sentiment-api:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/arabic-sentiment-api:latest
```

### Deploy to Kubernetes

```bash
# Apply ConfigMap first
kubectl apply -f k8s/configmap.yaml

# Deploy the application
kubectl apply -f k8s/deployment.yaml

# Create service
kubectl apply -f k8s/service.yaml

# Optional: Apply HPA for autoscaling
kubectl apply -f k8s/hpa.yaml

# Optional: Apply Ingress for external access
kubectl apply -f k8s/ingress.yaml
```

### Verify Deployment

```bash
# Check deployment status
kubectl get deployments
kubectl describe deployment arabic-sentiment-api

# Check pods
kubectl get pods -l app=arabic-sentiment-api
kubectl logs -f deployment/arabic-sentiment-api

# Check service
kubectl get services
kubectl describe service arabic-sentiment-api

# Check HPA
kubectl get hpa
```

### Test the API

```bash
# Port-forward for local testing
kubectl port-forward service/arabic-sentiment-api 8000:80

# In another terminal, test the API
curl http://localhost:8000/health
```

### Access via LoadBalancer (if configured)

```bash
# Get external IP
kubectl get service arabic-sentiment-api-external

# Test using external IP
curl http://EXTERNAL_IP:8000/health
```

---

## Environment Variables

### Available Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_NAME` | `Belall87/arabert-arabic-sentiment` | Hugging Face model identifier |
| `PORT` | `8000` | API server port |
| `WORKERS` | `1` | Number of Uvicorn workers |
| `LOG_LEVEL` | `info` | Logging level (debug, info, warning, error) |
| `MAX_LENGTH` | `128` | Maximum token length for input |
| `CORS_ORIGINS` | `*` | Allowed CORS origins (comma-separated) |

### Docker Example

```bash
docker run -d \
  -e MODEL_NAME=Belall87/arabert-arabic-sentiment \
  -e WORKERS=2 \
  -e LOG_LEVEL=debug \
  -p 8000:8000 \
  arabic-sentiment-api:latest
```

### Kubernetes Example

Edit `k8s/deployment.yaml`:
```yaml
env:
- name: WORKERS
  value: "2"
- name: LOG_LEVEL
  value: "debug"
```

---

## Scaling

### Docker Compose Scaling

```bash
# Scale to 3 instances
docker-compose up -d --scale api=3
```

### Kubernetes Manual Scaling

```bash
# Scale to 5 replicas
kubectl scale deployment arabic-sentiment-api --replicas=5

# Verify
kubectl get pods -l app=arabic-sentiment-api
```

### Kubernetes Auto-Scaling (HPA)

The HPA configuration automatically scales based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)
- Min replicas: 2
- Max replicas: 10

```bash
# Monitor HPA status
kubectl get hpa arabic-sentiment-api-hpa -w

# See detailed metrics
kubectl describe hpa arabic-sentiment-api-hpa
```

---

## Monitoring

### Container Logs

```bash
# Docker
docker logs -f arabic-sentiment-api

# Docker Compose
docker-compose logs -f api

# Kubernetes
kubectl logs -f deployment/arabic-sentiment-api
kubectl logs -f -l app=arabic-sentiment-api --all-containers=true
```

### Health Checks

```bash
# Check health endpoint
curl http://localhost:8000/health

# Check model info
curl http://localhost:8000/model/info
```

### Kubernetes Metrics

```bash
# Pod resource usage
kubectl top pods -l app=arabic-sentiment-api

# Node resource usage
kubectl top nodes
```

### Prometheus & Grafana (Optional)

For production monitoring, consider:
- Prometheus for metrics collection
- Grafana for visualization
- Loki for log aggregation

---

## Troubleshooting

### Issue: Container fails to start

**Symptom:** Container exits immediately

**Solution:**
```bash
# Check logs
docker logs arabic-sentiment-api

# Common issues:
# 1. Model download failed - check internet connectivity
# 2. Insufficient memory - increase memory limits
# 3. Port already in use - change port mapping
```

### Issue: Model loading takes too long

**Symptom:** Health checks fail during startup

**Solution:**
```bash
# Increase startup probe failure threshold in k8s/deployment.yaml
startupProbe:
  failureThreshold: 20  # 200 seconds max
```

### Issue: Out of memory

**Symptom:** Pod gets OOMKilled

**Solution:**
```bash
# Increase memory limits in k8s/deployment.yaml
resources:
  limits:
    memory: "6Gi"  # Increase from 4Gi
```

### Issue: Slow predictions

**Symptom:** API response time > 1 second

**Solutions:**
1. Check CPU resources
2. Enable GPU if available
3. Reduce `MAX_LENGTH` if possible
4. Scale horizontally (add more replicas)

### Issue: Connection refused

**Symptom:** Cannot connect to API

**Solution:**
```bash
# Check if service is running
kubectl get pods
kubectl get services

# Port-forward to test locally
kubectl port-forward service/arabic-sentiment-api 8000:80

# Check firewall rules and security groups
```

---

## Production Checklist

Before deploying to production:

- [ ] Environment variables configured correctly
- [ ] Docker image pushed to private registry
- [ ] Resource limits set appropriately
- [ ] Health checks configured
- [ ] HPA enabled for auto-scaling
- [ ] Ingress with TLS/SSL configured
- [ ] Monitoring and logging set up
- [ ] Rate limiting configured
- [ ] CORS origins restricted (not `*`)
- [ ] Security groups/firewall rules configured
- [ ] Backup and disaster recovery plan
- [ ] Load testing completed

---

## Support

For deployment issues:
- **GitHub Issues:** [Bolaal/Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT](https://github.com/Bolaal/Arabic-Sentiment-Analysis-BiLSTM-vs-AraBERT/issues)
- **Email:** belalmahmoud8787@gmail.com

---

**Last Updated:** March 2026
