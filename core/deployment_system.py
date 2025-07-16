#!/usr/bin/env python3
"""
Deployment System for +++A Project Builder 2030
- Docker containerization
- Kubernetes orchestration
- CI/CD pipelines (GitHub Actions, GitLab CI)
- Infrastructure as Code (Terraform, Pulumi)
- Monitoring and logging setup
"""

import os
import json
import yaml
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()

class DeploymentTarget(Enum):
    """Deployment target environments"""
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class InfrastructureProvider(Enum):
    """Infrastructure providers"""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    DIGITAL_OCEAN = "digitalocean"
    KUBERNETES = "kubernetes"
    DOCKER = "docker"

@dataclass
class DeploymentConfig:
    """Deployment configuration"""
    name: str
    target: DeploymentTarget
    provider: InfrastructureProvider
    resources: Dict[str, Any]
    scaling: Dict[str, Any]
    monitoring: Dict[str, Any]
    security: Dict[str, Any]

class ModernDeploymentSystem:
    """Modern deployment and infrastructure management system"""
    
    def __init__(self):
        self.console = console
    
    def generate_dockerfile(self, project_type: str = "nextjs", node_version: str = "20") -> str:
        """Generate optimized Dockerfile for different project types"""
        
        if project_type == "nextjs":
            return f'''# Multi-stage Dockerfile for Next.js application
FROM node:{node_version}-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies based on the preferred package manager
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./
RUN \\
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \\
  elif [ -f package-lock.json ]; then npm ci; \\
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \\
  else echo "Lockfile not found." && exit 1; \\
  fi

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Environment variables for build
ENV NEXT_TELEMETRY_DISABLED 1
ENV NODE_ENV production

# Build the application
RUN \\
  if [ -f yarn.lock ]; then yarn run build; \\
  elif [ -f package-lock.json ]; then npm run build; \\
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm run build; \\
  else echo "Lockfile not found." && exit 1; \\
  fi

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

# Create nextjs user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy public assets
COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# Start the application
CMD ["node", "server.js"]
'''
        
        elif project_type == "nodejs_api":
            return f'''# Dockerfile for Node.js API
FROM node:{node_version}-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Development dependencies for building
FROM base AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

# Create app user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nodejs

# Copy built application
COPY --from=deps --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/package.json ./package.json

USER nodejs

EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
'''
        
        return "# Dockerfile template not available for this project type"
    
    def generate_docker_compose(self, services: List[str] = None) -> str:
        """Generate docker-compose.yml for local development"""
        
        if services is None:
            services = ["app", "db", "redis"]
        
        compose_config = {
            "version": "3.8",
            "services": {},
            "networks": {
                "app-network": {
                    "driver": "bridge"
                }
            },
            "volumes": {
                "postgres_data": {},
                "redis_data": {}
            }
        }
        
        # Application service
        if "app" in services:
            compose_config["services"]["app"] = {
                "build": {
                    "context": ".",
                    "dockerfile": "Dockerfile"
                },
                "ports": ["3000:3000"],
                "environment": [
                    "NODE_ENV=development",
                    "DATABASE_URL=postgresql://postgres:password@db:5432/myapp",
                    "REDIS_URL=redis://redis:6379"
                ],
                "depends_on": ["db", "redis"],
                "networks": ["app-network"],
                "volumes": [
                    ".:/app",
                    "/app/node_modules"
                ],
                "restart": "unless-stopped"
            }
        
        # PostgreSQL service
        if "db" in services:
            compose_config["services"]["db"] = {
                "image": "postgres:16-alpine",
                "environment": [
                    "POSTGRES_DB=myapp",
                    "POSTGRES_USER=postgres",
                    "POSTGRES_PASSWORD=password"
                ],
                "ports": ["5432:5432"],
                "volumes": [
                    "postgres_data:/var/lib/postgresql/data",
                    "./prisma/init.sql:/docker-entrypoint-initdb.d/init.sql"
                ],
                "networks": ["app-network"],
                "restart": "unless-stopped"
            }
        
        # Redis service
        if "redis" in services:
            compose_config["services"]["redis"] = {
                "image": "redis:7-alpine",
                "ports": ["6379:6379"],
                "volumes": ["redis_data:/data"],
                "networks": ["app-network"],
                "restart": "unless-stopped",
                "command": "redis-server --appendonly yes"
            }
        
        # Nginx reverse proxy
        if "nginx" in services:
            compose_config["services"]["nginx"] = {
                "image": "nginx:alpine",
                "ports": ["80:80", "443:443"],
                "volumes": [
                    "./nginx.conf:/etc/nginx/nginx.conf",
                    "./ssl:/etc/nginx/ssl"
                ],
                "depends_on": ["app"],
                "networks": ["app-network"],
                "restart": "unless-stopped"
            }
        
        return yaml.dump(compose_config, default_flow_style=False, sort_keys=False)
    
    def generate_kubernetes_manifests(self, app_name: str = "myapp") -> Dict[str, str]:
        """Generate Kubernetes deployment manifests"""
        
        manifests = {}
        
        # Namespace
        manifests["namespace.yaml"] = f'''apiVersion: v1
kind: Namespace
metadata:
  name: {app_name}
  labels:
    app: {app_name}
---
'''
        
        # ConfigMap
        manifests["configmap.yaml"] = f'''apiVersion: v1
kind: ConfigMap
metadata:
  name: {app_name}-config
  namespace: {app_name}
data:
  NODE_ENV: "production"
  PORT: "3000"
  DATABASE_HOST: "postgres-service"
  REDIS_HOST: "redis-service"
---
'''
        
        # Secret
        manifests["secret.yaml"] = f'''apiVersion: v1
kind: Secret
metadata:
  name: {app_name}-secrets
  namespace: {app_name}
type: Opaque
data:
  # Base64 encoded values
  DATABASE_PASSWORD: cGFzc3dvcmQ=  # password
  JWT_SECRET: c3VwZXJzZWNyZXRrZXk=      # supersecretkey
  API_KEY: YXBpa2V5MTIzNDU2            # apikey123456
---
'''
        
        # Application Deployment
        manifests["deployment.yaml"] = f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}-deployment
  namespace: {app_name}
  labels:
    app: {app_name}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {app_name}:latest
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          valueFrom:
            configMapKeyRef:
              name: {app_name}-config
              key: NODE_ENV
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {app_name}-secrets
              key: DATABASE_PASSWORD
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
---
'''
        
        # Service
        manifests["service.yaml"] = f'''apiVersion: v1
kind: Service
metadata:
  name: {app_name}-service
  namespace: {app_name}
spec:
  selector:
    app: {app_name}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 3000
  type: ClusterIP
---
'''
        
        # Ingress
        manifests["ingress.yaml"] = f'''apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {app_name}-ingress
  namespace: {app_name}
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - {app_name}.yourdomain.com
    secretName: {app_name}-tls
  rules:
  - host: {app_name}.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {app_name}-service
            port:
              number: 80
---
'''
        
        # HorizontalPodAutoscaler
        manifests["hpa.yaml"] = f'''apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {app_name}-hpa
  namespace: {app_name}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {app_name}-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
---
'''
        
        return manifests
    
    def generate_github_actions_workflow(self, app_name: str = "myapp") -> str:
        """Generate GitHub Actions CI/CD workflow"""
        
        return f'''name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{{{ github.repository }}}}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Type checking
      run: npm run type-check
    
    - name: Linting
      run: npm run lint
    
    - name: Unit tests
      run: npm run test
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379
    
    - name: E2E tests
      run: npm run test:e2e
    
    - name: Build application
      run: npm run build

  security:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  build-and-push:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    permissions:
      contents: read
      packages: write
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{{{ env.REGISTRY }}}}
        username: ${{{{ github.actor }}}}
        password: ${{{{ secrets.GITHUB_TOKEN }}}}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}
        tags: |
          type=ref,event=branch
          type=sha,prefix={{{{branch}}}}-
          type=raw,value=latest,enable={{{{is_default_branch}}}}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{{{ steps.meta.outputs.tags }}}}
        labels: ${{{{ steps.meta.outputs.labels }}}}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy-staging:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{{{ secrets.KUBE_CONFIG_STAGING }}}}
    
    - name: Deploy to staging
      run: |
        # Update image tag in deployment
        sed -i "s|{app_name}:latest|${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}:develop-${{{{ github.sha }}}}|" k8s/deployment.yaml
        
        # Apply Kubernetes manifests
        kubectl apply -f k8s/ -n {app_name}-staging
        
        # Wait for rollout
        kubectl rollout status deployment/{app_name}-deployment -n {app_name}-staging

  deploy-production:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{{{ secrets.KUBE_CONFIG_PROD }}}}
    
    - name: Deploy to production
      run: |
        # Update image tag in deployment
        sed -i "s|{app_name}:latest|${{{{ env.REGISTRY }}}}/${{{{ env.IMAGE_NAME }}}}:latest|" k8s/deployment.yaml
        
        # Apply Kubernetes manifests
        kubectl apply -f k8s/ -n {app_name}
        
        # Wait for rollout
        kubectl rollout status deployment/{app_name}-deployment -n {app_name}
    
    - name: Notify deployment
      uses: 8398a7/action-slack@v3
      with:
        status: ${{{{ job.status }}}}
        channel: '#deployments'
        webhook_url: ${{{{ secrets.SLACK_WEBHOOK }}}}
      if: always()
'''
    
    def generate_terraform_config(self, provider: str = "aws", app_name: str = "myapp") -> Dict[str, str]:
        """Generate Terraform infrastructure configuration"""
        
        configs = {}
        
        if provider == "aws":
            # Main configuration
            configs["main.tf"] = f'''# Terraform configuration for AWS deployment
terraform {{
  required_version = ">= 1.6"
  
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
    kubernetes = {{
      source  = "hashicorp/kubernetes"
      version = "~> 2.24"
    }}
  }}
  
  backend "s3" {{
    bucket = "{app_name}-terraform-state"
    key    = "infrastructure/terraform.tfstate"
    region = var.aws_region
  }}
}}

provider "aws" {{
  region = var.aws_region
}}

# Data sources
data "aws_availability_zones" "available" {{
  state = "available"
}}

data "aws_caller_identity" "current" {{}}
'''
            
            # Variables
            configs["variables.tf"] = f'''# Input variables
variable "aws_region" {{
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}}

variable "app_name" {{
  description = "Application name"
  type        = string
  default     = "{app_name}"
}}

variable "environment" {{
  description = "Environment name"
  type        = string
  default     = "production"
}}

variable "node_instance_type" {{
  description = "EC2 instance type for EKS nodes"
  type        = string
  default     = "t3.medium"
}}

variable "min_nodes" {{
  description = "Minimum number of nodes"
  type        = number
  default     = 2
}}

variable "max_nodes" {{
  description = "Maximum number of nodes"
  type        = number
  default     = 10
}}

variable "desired_nodes" {{
  description = "Desired number of nodes"
  type        = number
  default     = 3
}}
'''
            
            # VPC configuration
            configs["vpc.tf"] = f'''# VPC Configuration
resource "aws_vpc" "main" {{
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {{
    Name = "${{var.app_name}}-vpc"
    Environment = var.environment
  }}
}}

# Internet Gateway
resource "aws_internet_gateway" "main" {{
  vpc_id = aws_vpc.main.id
  
  tags = {{
    Name = "${{var.app_name}}-igw"
    Environment = var.environment
  }}
}}

# Public Subnets
resource "aws_subnet" "public" {{
  count = 2
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${{count.index + 1}}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = {{
    Name = "${{var.app_name}}-public-subnet-${{count.index + 1}}"
    Environment = var.environment
    "kubernetes.io/role/elb" = "1"
  }}
}}

# Private Subnets
resource "aws_subnet" "private" {{
  count = 2
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${{count.index + 10}}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = {{
    Name = "${{var.app_name}}-private-subnet-${{count.index + 1}}"
    Environment = var.environment
    "kubernetes.io/role/internal-elb" = "1"
  }}
}}

# Route Tables
resource "aws_route_table" "public" {{
  vpc_id = aws_vpc.main.id
  
  route {{
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }}
  
  tags = {{
    Name = "${{var.app_name}}-public-rt"
    Environment = var.environment
  }}
}}

resource "aws_route_table_association" "public" {{
  count = length(aws_subnet.public)
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}}
'''
            
            # EKS configuration
            configs["eks.tf"] = f'''# EKS Cluster
resource "aws_eks_cluster" "main" {{
  name     = "${{var.app_name}}-cluster"
  role_arn = aws_iam_role.cluster.arn
  version  = "1.28"
  
  vpc_config {{
    subnet_ids              = concat(aws_subnet.public[*].id, aws_subnet.private[*].id)
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs     = ["0.0.0.0/0"]
  }}
  
  enabled_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
  
  depends_on = [
    aws_iam_role_policy_attachment.cluster_policy,
    aws_iam_role_policy_attachment.cluster_service_policy
  ]
  
  tags = {{
    Name = "${{var.app_name}}-cluster"
    Environment = var.environment
  }}
}}

# EKS Node Group
resource "aws_eks_node_group" "main" {{
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${{var.app_name}}-nodes"
  node_role_arn   = aws_iam_role.node.arn
  subnet_ids      = aws_subnet.private[*].id
  instance_types  = [var.node_instance_type]
  
  scaling_config {{
    desired_size = var.desired_nodes
    max_size     = var.max_nodes
    min_size     = var.min_nodes
  }}
  
  update_config {{
    max_unavailable = 1
  }}
  
  depends_on = [
    aws_iam_role_policy_attachment.node_policy,
    aws_iam_role_policy_attachment.node_cni_policy,
    aws_iam_role_policy_attachment.node_registry_policy
  ]
  
  tags = {{
    Name = "${{var.app_name}}-node-group"
    Environment = var.environment
  }}
}}
'''
        
        return configs
    
    def generate_monitoring_config(self, app_name: str = "myapp") -> Dict[str, str]:
        """Generate monitoring and logging configuration"""
        
        configs = {}
        
        # Prometheus configuration
        configs["prometheus.yml"] = f'''# Prometheus configuration
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: '{app_name}'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\\d+)?;(\\d+)
        replacement: $1:$2
        target_label: __address__

  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
'''
        
        # Grafana dashboard
        configs["grafana-dashboard.json"] = json.dumps({
            "dashboard": {
                "id": None,
                "title": f"{app_name.title()} Monitoring Dashboard",
                "tags": ["kubernetes", app_name],
                "timezone": "browser",
                "panels": [
                    {
                        "id": 1,
                        "title": "Request Rate",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": f"rate(http_requests_total{{service='{app_name}'}}[5m])",
                                "refId": "A"
                            }
                        ],
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
                    },
                    {
                        "id": 2,
                        "title": "Response Time",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": f"histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{{service='{app_name}'}}[5m]))",
                                "refId": "A"
                            }
                        ],
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
                    },
                    {
                        "id": 3,
                        "title": "Error Rate",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": f"rate(http_requests_total{{service='{app_name}',status=~'5..'}}[5m])",
                                "refId": "A"
                            }
                        ],
                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
                    },
                    {
                        "id": 4,
                        "title": "CPU Usage",
                        "type": "graph",
                        "targets": [
                            {
                                "expr": f"rate(container_cpu_usage_seconds_total{{pod=~'{app_name}.*'}}[5m])",
                                "refId": "A"
                            }
                        ],
                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
                    }
                ],
                "time": {"from": "now-1h", "to": "now"},
                "refresh": "5s"
            }
        }, indent=2)
        
        # Alert rules
        configs["alert_rules.yml"] = f'''# Prometheus alert rules
groups:
  - name: {app_name}_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{{service="{app_name}",status=~"5.."}}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{{{ $value }}}} requests per second"
      
      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket{{service="{app_name}"}}[5m])) > 0.5
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{{{ $value }}}} seconds"
      
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total{{pod=~"{app_name}.*"}}[15m]) > 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Pod is crash looping"
          description: "Pod {{{{ $labels.pod }}}} is restarting frequently"
      
      - alert: HighCPUUsage
        expr: rate(container_cpu_usage_seconds_total{{pod=~"{app_name}.*"}}[5m]) > 0.8
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is {{{{ $value }}}} for pod {{{{ $labels.pod }}}}"
'''
        
        return configs
    
    def display_deployment_summary(self, configs: Dict[str, Any]):
        """Display deployment configuration summary"""
        
        table_data = []
        for config_type, details in configs.items():
            if isinstance(details, dict):
                table_data.append([config_type.title(), str(len(details)), "✅ Generated"])
            else:
                table_data.append([config_type.title(), "1", "✅ Generated"])
        
        console.print("\n📋 Deployment Configuration Summary:")
        for row in table_data:
            console.print(f"  {row[0]}: {row[1]} files {row[2]}")

# Example usage and demonstration
def main():
    """Demonstrate the deployment system"""
    
    deployment_system = ModernDeploymentSystem()
    
    console.print(Panel.fit(
        "🚀 Modern Deployment System 2030",
        style="bold green"
    ))
    
    app_name = "my-saas-app"
    
    # Generate Docker configurations
    dockerfile = deployment_system.generate_dockerfile("nextjs")
    docker_compose = deployment_system.generate_docker_compose()
    
    # Generate Kubernetes manifests
    k8s_manifests = deployment_system.generate_kubernetes_manifests(app_name)
    
    # Generate CI/CD pipeline
    github_workflow = deployment_system.generate_github_actions_workflow(app_name)
    
    # Generate Terraform infrastructure
    terraform_configs = deployment_system.generate_terraform_config("aws", app_name)
    
    # Generate monitoring configuration
    monitoring_configs = deployment_system.generate_monitoring_config(app_name)
    
    # Display summary
    all_configs = {
        "docker": {"Dockerfile": dockerfile, "docker-compose.yml": docker_compose},
        "kubernetes": k8s_manifests,
        "ci_cd": {"github-workflow.yml": github_workflow},
        "terraform": terraform_configs,
        "monitoring": monitoring_configs
    }
    
    deployment_system.display_deployment_summary(all_configs)
    
    console.print(f"\n✅ Complete deployment configuration generated for {app_name}!")
    console.print("📁 Ready for production deployment with:")
    console.print("  • Docker containerization")
    console.print("  • Kubernetes orchestration") 
    console.print("  • CI/CD automation")
    console.print("  • Infrastructure as Code")
    console.print("  • Monitoring & alerting")

if __name__ == "__main__":
    main() 