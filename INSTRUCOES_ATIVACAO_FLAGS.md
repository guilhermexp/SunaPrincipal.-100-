# Instruções para Ativar Todas as Flags do Suna

## Pré-requisitos

1. **Redis instalado e rodando**
   - macOS: `brew install redis && brew services start redis`
   - Linux: `sudo apt-get install redis-server && sudo systemctl start redis`
   - Docker: `docker run -d -p 6379:6379 redis`

2. **Variáveis de ambiente configuradas**
   - Certifique-se de ter os arquivos `.env` configurados:
     - `backend/.env` (copie de `backend/.env.example`)
     - `frontend/.env.local` (copie de `frontend/.env.example`)

3. **Python 3.8+ instalado**

## Como Ativar as Flags

1. **Execute o script de ativação:**
   ```bash
   python activate_all_flags.py
   ```

2. **O script irá:**
   - Verificar a conexão com o Redis
   - Ativar todas as feature flags conhecidas
   - Listar o status de todas as flags

## Flags Ativadas

O script ativa as seguintes flags:

- `agentPlaygroundFlagFrontend` - Habilita o playground de agentes no frontend
- `marketplaceFlagFrontend` - Habilita o marketplace no frontend  
- `agentPlaygroundEnabled` - Habilita funcionalidade do playground de agentes
- `marketplaceEnabled` - Habilita funcionalidade do marketplace
- `maintenance-notice` - Exibe aviso de manutenção

## Verificando as Flags

### Via API (Backend rodando):
```bash
curl http://localhost:8000/feature-flags
```

### Via Frontend:
- As flags são carregadas automaticamente
- Faça refresh da página após ativar as flags

## Configuração de Ambiente

Para desenvolvimento local, configure `ENV_MODE=local` em:
- `backend/.env`: `ENV_MODE=local`
- `frontend/.env.local`: `NEXT_PUBLIC_ENV_MODE=local`

Isso habilitará automaticamente algumas flags de desenvolvimento.

## Solução de Problemas

1. **Erro de conexão com Redis:**
   - Verifique se o Redis está rodando: `redis-cli ping`
   - Deve retornar `PONG`

2. **Flags não aparecem no frontend:**
   - Certifique-se de que o backend está rodando
   - Limpe o cache do navegador
   - Verifique o console para erros

3. **Erro de importação de módulos:**
   - Execute o script da raiz do projeto Suna
   - Certifique-se de que as dependências estão instaladas