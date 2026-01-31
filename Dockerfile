# Multi-stage build para otimização

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Instala dependências
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copia dependências do builder
COPY --from=builder /root/.local /root/.local

# Copia código da aplicação
COPY app/ .

# Adiciona .local/bin ao PATH
ENV PATH=/root/.local/bin:$PATH

# Expõe a porta
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Comando para iniciar a aplicação
CMD ["python", "main.py"]
