# 🍽️ Sistema de Gestão para Restaurante

Sistema completo de gestão para restaurantes desenvolvido em Django com interface moderna e responsiva.

## 🎯 Funcionalidades

### 7 Módulos Principais:

1. **Autenticação** - Sistema multi-usuário e multi-empresa
2. **Caixa** - Interface para operadores registrarem pedidos
3. **Cozinha** - Gestão de pedidos em tempo real
4. **Acompanhamento** - Cliente acompanha pedido via QR Code único
5. **Painel de Status** - Visão geral de todos os pedidos
6. **Autoatendimento** - Totem para clientes fazerem pedidos
7. **Cardápio Cliente** - Visualização do cardápio

## 🎨 Design

- Paleta de cores: Preto, Laranja (#FF6B35) e Branco
- Interface moderna e responsiva
- Otimizado para desktop, tablet e mobile

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clone o repositório** (ou já está no diretório)

2. **Ative o ambiente virtual**
```bash
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute as migrações**
```bash
python manage.py migrate
```

5. **Popule o banco de dados** (opcional - dados de exemplo)
```bash
python populate_db.py
```

6. **Inicie o servidor**
```bash
python manage.py runserver
```

7. **Acesse o sistema**
- URL: http://localhost:8000

## 👥 Credenciais de Acesso

Após executar o `populate_db.py`:

| Usuário | Senha | Tipo |
|---------|-------|------|
| admin | senha123 | Administrador |
| caixa1 | senha123 | Operador de Caixa |
| cozinha1 | senha123 | Cozinha |
| gerente | senha123 | Gerente |

## 📱 Acessando as Telas

### Para Funcionários (requer login):
- **Login**: http://localhost:8000/auth/login/
- **Caixa**: http://localhost:8000/caixa/
- **Cozinha**: http://localhost:8000/cozinha/
- **Painel de Status**: http://localhost:8000/painel/
- **Admin**: http://localhost:8000/admin/

### Para Clientes (sem login):
- **Autoatendimento**: http://localhost:8000/autoatendimento/1/
- **Cardápio**: http://localhost:8000/cardapio/1/
- **Acompanhamento**: http://localhost:8000/acompanhamento/{QR_CODE}/

*Nota: O QR Code é gerado automaticamente ao criar um pedido*

## 🏗️ Estrutura do Projeto

```
cantina_system/
├── authentication/      # Autenticação e usuários
├── caixa/              # Módulo do caixa
├── cozinha/            # Módulo da cozinha
├── acompanhamento/     # Acompanhamento por QR Code
├── painel_status/      # Painel de status geral
├── autoatendimento/    # Totem de autoatendimento
├── cliente/            # Cardápio para clientes
├── templates/          # Templates HTML
├── static/             # CSS e JavaScript
│   ├── css/
│   └── js/
└── media/              # Upload de imagens
```

## 🔧 Tecnologias

- **Backend**: Django 6.0.2
- **Banco de Dados**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Design**: Responsivo com CSS Grid e Flexbox

## 📊 Fluxo de Trabalho

1. **Caixa** registra o pedido
2. Pedido aparece na **Cozinha** como "Pendente"
3. Cozinha marca como "Preparando"
4. Quando pronto, marca como "Pronto"
5. Cliente acompanha via **QR Code** no celular
6. **Painel de Status** mostra visão geral em tempo real

## 🎯 Recursos Especiais

- ✅ Sistema multi-empresa
- ✅ QR Code único por pedido
- ✅ Auto-refresh nas telas (cozinha, painel)
- ✅ Interface responsiva
- ✅ Gestão de categorias e produtos
- ✅ Diferentes tipos de pedido (balcão, mesa, delivery)
- ✅ Observações por item
- ✅ Cálculo automático de totais

## 📝 Próximos Passos

Para produção, considere:
- Configurar banco de dados PostgreSQL
- Implementar WebSockets para atualizações em tempo real
- Adicionar impressão de comandas
- Integração com sistemas de pagamento
- Relatórios e dashboards analíticos
- Backup automático

## 🤝 Suporte

Para dúvidas ou problemas, verifique:
- Logs do Django
- Console do navegador (F12)
- Arquivo de configuração `settings.py`

## 📄 Licença

Projeto desenvolvido para fins educacionais e comerciais.
