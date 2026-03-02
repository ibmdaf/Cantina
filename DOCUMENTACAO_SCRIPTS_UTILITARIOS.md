# 🛠️ Documentação - Scripts Utilitários

## Visão Geral

Este documento descreve os scripts utilitários disponíveis no projeto para manutenção e gerenciamento do sistema.

---

## 📝 atualizar_nomes_usuarios.py

### Descrição
Script interativo para preencher o campo `first_name` (nome) de usuários que estão com este campo vazio.

### Quando Usar
- Após migração de sistema antigo
- Quando usuários foram criados sem o campo nome
- Para atualizar nomes em lote

### Como Executar
```bash
source venv/bin/activate
python atualizar_nomes_usuarios.py
```

### Funcionamento
1. Busca todos os usuários com `first_name` vazio
2. Para cada usuário, exibe:
   - Username
   - Tipo de usuário
3. Solicita que você digite o nome da pessoa
4. Salva o nome no banco de dados
5. Exibe resumo final de todos os usuários

### Exemplo de Uso
```
Encontrados 3 usuários sem nome (first_name vazio)

Para cada usuário, digite o nome da pessoa:
(Pressione Enter para pular)

Usuário: admin
Tipo: Administrador
Digite o nome da pessoa: João Silva
✅ Nome 'João Silva' salvo para admin

Usuário: tay
Tipo: Caixa
Digite o nome da pessoa: Tayna Costa
✅ Nome 'Tayna Costa' salvo para tay

✅ Atualização concluída!

📋 Resumo dos usuários:
  - admin: João Silva (Administrador)
  - tay: Tayna Costa (Caixa)
```

---

## 🗂️ criar_categoria_combo.py

### Descrição
Script para criar a categoria especial "Combos" no sistema, necessária para o funcionamento do sistema de combos.

### Quando Usar
- Na primeira configuração do sistema
- Se a categoria Combos foi excluída acidentalmente
- Ao configurar uma nova empresa

### Como Executar
```bash
source venv/bin/activate
python criar_categoria_combo.py
```

### Funcionamento
1. Verifica se já existe uma categoria "Combos"
2. Se não existir, cria com:
   - Nome: "Combos"
   - Emoji: 🎁
   - Flag `is_sistema=True` (categoria do sistema)
   - Ativa por padrão
3. Exibe mensagem de sucesso ou aviso se já existir

### Características da Categoria Combos
- **is_sistema=True**: Não pode ser excluída pelo usuário
- **Emoji**: 🎁
- **Uso**: Produtos do tipo combo são automaticamente associados a esta categoria

---

## 🧹 limpar_categorias_inativas.py

### Descrição
Script para remover categorias inativas do banco de dados.

### Quando Usar
- Limpeza periódica do banco de dados
- Remoção de categorias antigas não utilizadas
- Otimização de espaço

### Como Executar
```bash
source venv/bin/activate
python limpar_categorias_inativas.py
```

### Funcionamento
1. Busca todas as categorias com `ativo=False`
2. Exibe lista de categorias que serão removidas
3. Solicita confirmação
4. Remove as categorias do banco de dados
5. Exibe quantidade de categorias removidas

### Atenção
- ⚠️ Esta ação é **irreversível**
- Produtos associados às categorias removidas ficarão sem categoria
- Recomenda-se fazer backup antes de executar

---

## 🔍 verificar_categorias.py

### Descrição
Script para listar todas as categorias do sistema e suas informações.

### Quando Usar
- Auditoria de categorias
- Verificação de dados
- Debug de problemas com categorias

### Como Executar
```bash
source venv/bin/activate
python verificar_categorias.py
```

### Funcionamento
1. Lista todas as categorias do banco de dados
2. Para cada categoria, exibe:
   - ID
   - Nome
   - Emoji
   - Status (Ativa/Inativa)
   - Flag is_sistema
   - Quantidade de produtos associados

### Exemplo de Saída
```
📋 Categorias no Sistema:

ID: 1
Nome: Lanches
Emoji: 🍔
Status: Ativa
Sistema: Não
Produtos: 15

ID: 2
Nome: Bebidas
Emoji: 🥤
Status: Ativa
Sistema: Não
Produtos: 8

ID: 3
Nome: Combos
Emoji: 🎁
Status: Ativa
Sistema: Sim
Produtos: 5
```

---

## 📦 verificar_produtos_inativos.py

### Descrição
Script para listar todos os produtos inativos do sistema.

### Quando Usar
- Auditoria de produtos
- Identificar produtos que podem ser removidos
- Verificação de estoque

### Como Executar
```bash
source venv/bin/activate
python verificar_produtos_inativos.py
```

### Funcionamento
1. Busca todos os produtos com `ativo=False`
2. Para cada produto, exibe:
   - ID
   - Nome
   - Categoria
   - Preço
   - Quantidade em estoque
   - Data de criação

### Exemplo de Saída
```
📦 Produtos Inativos:

Total: 3 produtos inativos

ID: 45
Nome: X-Bacon Especial
Categoria: Lanches
Preço: R$ 18.50
Estoque: 0
Criado em: 2024-01-15

ID: 67
Nome: Suco de Laranja 500ml
Categoria: Bebidas
Preço: R$ 6.00
Estoque: 5
Criado em: 2024-02-20
```

---

## 🗄️ populate_db.py

### Descrição
Script para popular o banco de dados com dados de exemplo para testes e desenvolvimento.

### Quando Usar
- Primeira configuração do ambiente de desenvolvimento
- Testes de funcionalidades
- Demonstrações do sistema
- Reset do banco de dados para estado inicial

### Como Executar
```bash
source venv/bin/activate
python populate_db.py
```

### O que o Script Cria

#### 1. Empresa
- Nome: "Cantina Exemplo"
- Dados básicos configurados

#### 2. Usuários
- **Admin**: username "admin", senha "admin123"
- **Gerente**: username "gerente", senha "gerente123"
- **Caixa**: username "caixa", senha "caixa123"
- **Cozinha**: username "cozinha", senha "cozinha123"

#### 3. Categorias
- Lanches 🍔
- Bebidas 🥤
- Sobremesas 🍰
- Combos 🎁 (categoria do sistema)

#### 4. Produtos
- 10-15 produtos de exemplo em cada categoria
- Com preços, descrições e quantidades em estoque
- Alguns produtos ativos, outros inativos

#### 5. Combos
- 2-3 combos de exemplo
- Com slots configurados
- Itens associados aos slots

### Atenção
- ⚠️ Este script **limpa** dados existentes antes de popular
- Use apenas em ambiente de desenvolvimento
- **Não execute em produção** com dados reais

---

## 🔄 restart_server.py

### Descrição
Script para reiniciar o servidor Django de forma programática.

### Quando Usar
- Após mudanças em configurações
- Após instalação de novos pacotes
- Para aplicar mudanças que requerem restart

### Como Executar
```bash
python restart_server.py
```

### Funcionamento
1. Identifica o processo do servidor Django
2. Envia sinal de término
3. Aguarda finalização
4. Inicia novo processo do servidor

### Observações
- Funciona apenas se o servidor foi iniciado via script
- Em produção, use comandos do supervisor/systemd
- Para desenvolvimento, pode ser mais fácil usar Ctrl+C e reiniciar manualmente

---

## 🚀 start.sh

### Descrição
Script shell para iniciar o servidor Django com configurações otimizadas.

### Quando Usar
- Iniciar o servidor em desenvolvimento
- Iniciar o servidor em produção
- Automatizar inicialização

### Como Executar
```bash
chmod +x start.sh  # Primeira vez apenas
./start.sh
```

### Funcionamento
1. Ativa o ambiente virtual
2. Aplica migrações pendentes
3. Coleta arquivos estáticos (se necessário)
4. Inicia o servidor Django
5. Configura host e porta

### Configurações
```bash
# Desenvolvimento
python manage.py runserver 0.0.0.0:8000

# Produção (exemplo)
gunicorn cantina_system.wsgi:application --bind 0.0.0.0:8000
```

---

## 📋 Boas Práticas

### Antes de Executar Scripts
1. ✅ Faça backup do banco de dados
2. ✅ Ative o ambiente virtual
3. ✅ Verifique se está no diretório correto
4. ✅ Leia a documentação do script

### Após Executar Scripts
1. ✅ Verifique os logs de saída
2. ✅ Teste as funcionalidades afetadas
3. ✅ Documente mudanças realizadas

### Segurança
- 🔒 Não execute scripts desconhecidos
- 🔒 Revise o código antes de executar
- 🔒 Use apenas em ambientes apropriados
- 🔒 Mantenha backups atualizados

---

## 🆘 Troubleshooting

### Erro: "No module named 'django'"
**Solução**: Ative o ambiente virtual
```bash
source venv/bin/activate
```

### Erro: "django.db.utils.OperationalError"
**Solução**: Verifique se o banco de dados está acessível e as migrações foram aplicadas
```bash
python manage.py migrate
```

### Erro: "Permission denied"
**Solução**: Dê permissão de execução ao script
```bash
chmod +x nome_do_script.sh
```

### Script não encontra módulos
**Solução**: Execute do diretório raiz do projeto
```bash
cd /caminho/para/Cantina
python script.py
```
