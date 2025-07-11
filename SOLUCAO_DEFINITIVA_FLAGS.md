# Solução Definitiva para Ativar Flags no Suna

## O Problema
O backend está usando um Redis com hostname "redis" (provavelmente configuração Docker) enquanto você está rodando localmente. Por isso as flags não persistem.

## Solução Rápida (Recomendada)

### 1. Ative as flags no Redis local:
```bash
python ativar_flags_direto.py
```

### 2. Configure variáveis de ambiente:
```bash
cd backend
source .env.flags
```

### 3. Reinicie o backend com as flags:
```bash
# Pare o backend atual
pkill -f "uvicorn api:app"

# Inicie com as variáveis de ambiente
cd backend
source .env.flags
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

### 4. Faça refresh no navegador (Cmd+Shift+R)

## Solução Alternativa

Se ainda não funcionar, adicione estas linhas ao arquivo `backend/.env`:

```
FEATURE_FLAG_CUSTOM_AGENTS=true
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Verificação

Para confirmar que funcionou:
```bash
curl http://localhost:8000/api/feature-flags
```

Deve retornar:
```json
{
  "flags": {
    "custom_agents": true,
    ...
  }
}
```

## Por que isso acontece?

1. O backend está configurado para usar Redis com hostname "redis" (configuração Docker)
2. Localmente, o Redis roda em "localhost"
3. As flags são armazenadas apenas em memória (Redis), não em banco de dados
4. Quando o Redis reinicia, perde todas as flags

Esta solução contorna o problema usando variáveis de ambiente que são lidas na inicialização.