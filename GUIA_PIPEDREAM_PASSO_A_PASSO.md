# Guia Passo a Passo - Como Usar o Pipedream no Suna

## ✅ Status da Configuração

Sua configuração do Pipedream está **funcionando corretamente**! As credenciais estão configuradas e a conexão com a API está estabelecida.

## 📋 Passo a Passo para Conectar Apps

### 1. Acesse a Configuração do Agente

1. Abra o Suna em seu navegador: http://localhost:3000
2. Vá para a página **"Agents"** no menu lateral
3. Crie um novo agente ou edite um existente
4. Clique na aba **"Integrations"** ou **"MCP Servers"**

### 2. Acesse o Pipedream Registry

1. Na aba de integrações, procure por um botão chamado:
   - **"Pipedream Apps"**
   - **"Browse Apps"**
   - Ou um ícone de loja/grid

2. Isso abrirá o Pipedream Registry com mais de 2.700 apps disponíveis

### 3. Conecte um App (Exemplo: Google Sheets)

1. **Busque o App**:
   - Use a barra de pesquisa para encontrar "Google Sheets"
   - Ou navegue pelas categorias

2. **Clique no App**:
   - Clique no card do Google Sheets
   - Uma janela de conexão será aberta

3. **Crie um Perfil de Credencial**:
   - Dê um nome ao perfil (ex: "Minha Conta Google Pessoal")
   - Clique em **"Connect"** ou **"Conectar"**

4. **Autentique com o Google**:
   - Uma nova janela/aba será aberta
   - Faça login na sua conta Google
   - Autorize o acesso do Pipedream
   - A janela fechará automaticamente após sucesso

5. **Selecione as Ferramentas**:
   - Após conectar, você verá uma lista de ferramentas disponíveis
   - Marque as que deseja usar (ex: "Criar planilha", "Ler dados", etc.)
   - Clique em **"Save"** ou **"Salvar"**

### 4. Testando a Integração

Após configurar, volte ao chat com o agente e teste:

```
"Liste todas as minhas planilhas do Google Sheets"
```

```
"Crie uma nova planilha chamada 'Vendas 2025'"
```

```
"Adicione uma linha na planilha com os dados: Nome: João, Valor: R$ 1000"
```

## 🔧 Resolução de Problemas Comuns

### Problema 1: "Popup bloqueado"
**Solução**: Permita popups para localhost:3000 nas configurações do navegador

### Problema 2: "Erro de autenticação"
**Soluções**:
1. Certifique-se de que cookies de terceiros estão habilitados
2. Tente usar outro navegador (Chrome/Edge funcionam melhor)
3. Desative extensões de bloqueio de anúncios temporariamente

### Problema 3: "App não aparece na lista"
**Soluções**:
1. Recarregue a página (F5)
2. Limpe o cache do navegador
3. Verifique se digitou o nome corretamente

### Problema 4: "Ferramentas não funcionam"
**Soluções**:
1. Verifique se selecionou e salvou as ferramentas
2. Reconecte o app (delete o perfil e crie novamente)
3. Verifique os logs do agente para mensagens de erro

## 🌟 Apps Populares para Conectar

### Comunicação
- **Slack**: Enviar mensagens, criar canais
- **Discord**: Postar em servidores, gerenciar roles
- **Gmail**: Ler/enviar emails, gerenciar labels

### Produtividade
- **Google Sheets**: Manipular planilhas
- **Google Drive**: Upload/download de arquivos
- **Notion**: Criar páginas, gerenciar databases

### Desenvolvimento
- **GitHub**: Criar issues, pull requests
- **GitLab**: Gerenciar projetos
- **Jira**: Criar tickets, atualizar status

### CRM/Vendas
- **Salesforce**: Gerenciar leads, oportunidades
- **HubSpot**: Contatos, deals
- **Pipedrive**: Pipeline de vendas

### Outros
- **Stripe**: Processar pagamentos
- **Shopify**: Gerenciar loja
- **Twitter/X**: Postar tweets
- **LinkedIn**: Postar atualizações

## 💡 Dicas Importantes

1. **Nomes de Perfis**: Use nomes descritivos como "Gmail Trabalho" ou "Slack Empresa XYZ"

2. **Segurança**: 
   - Cada perfil é isolado e criptografado
   - Revise e remova perfis não utilizados
   - As credenciais nunca são expostas

3. **Múltiplas Contas**: Você pode criar vários perfis para o mesmo app (ex: Gmail pessoal e trabalho)

4. **Limites de API**: Esteja ciente dos limites de cada serviço externo

## 🚀 Exemplos de Uso Prático

### Exemplo 1: Automação de Email
```
"Verifique meus emails não lidos no Gmail e resuma os mais importantes"
```

### Exemplo 2: Relatório de Vendas
```
"Pegue os dados da planilha 'Vendas Q1' e crie um resumo com total por mês"
```

### Exemplo 3: Notificação Slack
```
"Envie uma mensagem no canal #vendas do Slack com o relatório de hoje"
```

### Exemplo 4: GitHub Issues
```
"Crie uma issue no repositório 'meu-projeto' com o título 'Bug no login'"
```

## ❓ Precisa de Ajuda?

Se continuar com problemas:

1. **Verifique os logs**:
   ```bash
   docker-compose logs backend -f | grep -i pipedream
   ```

2. **Teste a conexão**:
   ```bash
   python test_pipedream.py
   ```

3. **Verifique o navegador**:
   - Abra o Console do Desenvolvedor (F12)
   - Veja se há erros na aba Console
   - Verifique a aba Network para requisições falhadas

## 📝 Observações Finais

- O Pipedream está em modo "development", ideal para testes
- Suas credenciais estão seguras e funcionando
- A integração transforma o Suna em uma plataforma de automação poderosa
- Você pode conectar quantos apps quiser

Agora você está pronto para usar o poder do Pipedream com seus agentes Suna!