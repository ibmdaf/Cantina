# 🚀 Guia de Deploy em Produção

## Opções de Deploy

### 1. VPS (Recomendado para Controle Total)
- DigitalOcean
- Linode
- AWS EC2
- Google Cloud
- Azure

### 2. PaaS (Mais Fácil)
- Heroku
- Railway
- Render
- PythonAnywhere

### 3. Servidor Próprio
- Ubuntu Server
- CentOS
- Debian

---

## 📋 Checklist Pré-Deploy

- [ ] Código testado localmente
- [ ] Banco de dados de produção configurado
- [ ] Variáveis de ambiente definidas
- [ ] Arquivos estáticos coletados
- [ ] HTTPS configurado
- [ ] Backup configurado
- [ ] Monitoramento configurado

---

## 🔧 Configuração para Produção

### 1. Criar arquivo de configuração de produção

`cantina_system/settings_prod.py`:

```python
from .settings import *
import os

DEBUG = False

ALLOWED_HOSTS = ['seudominio.com', 'www.seudominio.com']

# Secret Key de variável de ambiente
SECRET_KEY = os.environ.get('SECRET_KEY')

# Banco de dados PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Segurança
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/cantina/error.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### 2. Atualizar requirements.txt

```bash
pip install gunicorn psycopg2-binary whitenoise
pip freeze > requirements.txt
```

### 3. Criar arquivo .env

`.env`:
```bash
SECRET_KEY=sua-chave-secreta-super-segura-aqui
DEBUG=False
DB_NAME=cantina_db
DB_USER=cantina_user
DB_PASSWORD=senha-super-segura
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=seu-email@gmail.com
EMAIL_PASSWORD=sua-senha-app
```

---

## 🐧 Deploy em Ubuntu Server

### 1. Preparar Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install python3-pip python3-venv nginx postgresql postgresql-contrib -y

# Criar usuário para aplicação
sudo adduser cantina
sudo usermod -aG sudo cantina
su - cantina
```

### 2. Configurar PostgreSQL

```bash
sudo -u postgres psql

CREATE DATABASE cantina_db;
CREATE USER cantina_user WITH PASSWORD 'senha-super-segura';
ALTER ROLE cantina_user SET client_encoding TO 'utf8';
ALTER ROLE cantina_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE cantina_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE cantina_db TO cantina_user;
\q
```

### 3. Clonar e Configurar Projeto

```bash
cd /home/cantina
git clone seu-repositorio.git cantina
cd cantina

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
nano .env
# (Cole as variáveis de ambiente)

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Migrar banco de dados
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

### 4. Configurar Gunicorn

`gunicorn_config.py`:
```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/cantina/gunicorn-error.log"
accesslog = "/var/log/cantina/gunicorn-access.log"
loglevel = "info"
```

### 5. Criar Serviço Systemd

`/etc/systemd/system/cantina.service`:
```ini
[Unit]
Description=Cantina System
After=network.target

[Service]
User=cantina
Group=www-data
WorkingDirectory=/home/cantina/cantina
Environment="PATH=/home/cantina/cantina/venv/bin"
EnvironmentFile=/home/cantina/cantina/.env
ExecStart=/home/cantina/cantina/venv/bin/gunicorn \
    --config /home/cantina/cantina/gunicorn_config.py \
    cantina_system.wsgi:application

[Install]
WantedBy=multi-user.target
```

Ativar serviço:
```bash
sudo systemctl daemon-reload
sudo systemctl start cantina
sudo systemctl enable cantina
sudo systemctl status cantina
```

### 6. Configurar Nginx

`/etc/nginx/sites-available/cantina`:
```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    client_max_body_size 10M;

    location /static/ {
        alias /home/cantina/cantina/staticfiles/;
    }

    location /media/ {
        alias /home/cantina/cantina/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Ativar site:
```bash
sudo ln -s /etc/nginx/sites-available/cantina /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 7. Configurar SSL com Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

---

## 🚀 Deploy no Heroku

### 1. Preparar Projeto

`Procfile`:
```
web: gunicorn cantina_system.wsgi --log-file -
```

`runtime.txt`:
```
python-3.11.0
```

### 2. Instalar Heroku CLI e Deploy

```bash
# Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Criar app
heroku create nome-do-seu-app

# Adicionar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Configurar variáveis
heroku config:set SECRET_KEY=sua-chave-secreta
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Migrar banco
heroku run python manage.py migrate

# Criar superusuário
heroku run python manage.py createsuperuser

# Abrir app
heroku open
```

---

## 🐳 Deploy com Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "cantina_system.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=cantina_db
      - POSTGRES_USER=cantina_user
      - POSTGRES_PASSWORD=senha-segura

  web:
    build: .
    command: gunicorn cantina_system.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

Deploy:
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 📊 Monitoramento

### 1. Sentry (Rastreamento de Erros)

```bash
pip install sentry-sdk
```

`settings_prod.py`:
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="sua-dsn-do-sentry",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### 2. Logs

```bash
# Criar diretório de logs
sudo mkdir -p /var/log/cantina
sudo chown cantina:cantina /var/log/cantina

# Ver logs em tempo real
tail -f /var/log/cantina/error.log
tail -f /var/log/cantina/gunicorn-error.log
```

---

## 🔄 Backup Automático

### Script de Backup

`backup.sh`:
```bash
#!/bin/bash

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/cantina/backups"

# Criar diretório se não existir
mkdir -p $BACKUP_DIR

# Backup do banco de dados
pg_dump cantina_db > $BACKUP_DIR/db_$DATE.sql

# Backup dos arquivos media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/cantina/cantina/media

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup concluído: $DATE"
```

Agendar no crontab:
```bash
crontab -e

# Backup diário às 2h da manhã
0 2 * * * /home/cantina/backup.sh
```

---

## 🔒 Segurança

### Checklist de Segurança

- [ ] DEBUG = False
- [ ] SECRET_KEY em variável de ambiente
- [ ] HTTPS configurado
- [ ] Firewall configurado
- [ ] Senhas fortes
- [ ] Backup automático
- [ ] Logs configurados
- [ ] Rate limiting
- [ ] CORS configurado
- [ ] SQL injection protegido (ORM)
- [ ] XSS protegido (templates)
- [ ] CSRF protegido (middleware)

### Configurar Firewall

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

---

## 📈 Performance

### 1. Cache com Redis

```bash
pip install redis django-redis
```

`settings_prod.py`:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### 2. CDN para Arquivos Estáticos

Use Cloudflare, AWS CloudFront ou similar.

---

## 🆘 Troubleshooting

### Erro 502 Bad Gateway
```bash
sudo systemctl status cantina
sudo journalctl -u cantina -n 50
```

### Erro de Permissão
```bash
sudo chown -R cantina:www-data /home/cantina/cantina
sudo chmod -R 755 /home/cantina/cantina
```

### Banco de Dados não Conecta
```bash
sudo systemctl status postgresql
sudo -u postgres psql -c "\l"
```

---

## ✅ Checklist Final

Antes de ir ao ar:

- [ ] Testado em ambiente de staging
- [ ] Backup configurado e testado
- [ ] SSL/HTTPS funcionando
- [ ] Domínio configurado
- [ ] Email configurado
- [ ] Logs funcionando
- [ ] Monitoramento ativo
- [ ] Documentação atualizada
- [ ] Equipe treinada
- [ ] Plano de rollback pronto

---

## 📞 Suporte Pós-Deploy

Mantenha documentado:
- Credenciais de acesso
- IPs dos servidores
- Configurações de DNS
- Contatos de suporte
- Procedimentos de emergência

**Boa sorte com o deploy! 🚀**
