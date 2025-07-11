# Instruções para Traduzir o Suna para Português

## Resumo das Mudanças

Criei um sistema básico de tradução para português brasileiro. Aqui está o que foi feito:

### 1. Arquivos Criados

- `/frontend/src/lib/translations/pt-BR.ts` - Arquivo com todas as traduções em português
- `/frontend/src/lib/translations/index.ts` - Sistema de gerenciamento de traduções
- `/frontend/src/hooks/use-translation.ts` - Hook React para usar traduções

### 2. Como Usar as Traduções

#### Em Componentes React:

```tsx
import { useTranslation } from '@/hooks/use-translation';

export function MyComponent() {
  const { t } = useTranslation();
  
  return (
    <div>
      <h1>{t('agents.title')}</h1>
      <button>{t('actions.create')}</button>
      <p>{t('status.loading')}</p>
    </div>
  );
}
```

#### Exemplo Prático - Sidebar:

```tsx
// Antes:
<span>Agents</span>

// Depois:
<span>{t('nav.agents')}</span>
```

### 3. Aplicar Traduções Manualmente

Como o Suna tem muitos componentes, você precisará aplicar as traduções manualmente. Aqui estão os principais arquivos para traduzir:

#### Navegação Principal:
- `/frontend/src/components/sidebar/sidebar-left.tsx`
- `/frontend/src/components/sidebar/sidebar-items.tsx`

#### Página de Agentes:
- `/frontend/src/app/(dashboard)/agents/page.tsx`
- `/frontend/src/components/agents/agent-card.tsx`
- `/frontend/src/components/agents/agent-builder.tsx`

#### Chat:
- `/frontend/src/components/thread/chat-input/chat-input.tsx`
- `/frontend/src/components/thread/message.tsx`

#### Configurações:
- `/frontend/src/app/(dashboard)/settings/page.tsx`

### 4. Padrão de Tradução

O sistema usa chaves hierárquicas. Por exemplo:
- `nav.dashboard` → "Painel"
- `agents.createAgent` → "Criar Agente"
- `status.loading` → "Carregando..."

### 5. Próximos Passos

1. **Aplicar em um componente de teste**:
   ```bash
   # Edite um componente simples primeiro para testar
   ```

2. **Traduzir gradualmente**:
   - Comece pela navegação (sidebar)
   - Depois páginas principais
   - Por fim, componentes menores

3. **Adicionar botão de idioma**:
   - Criar um seletor de idioma nas configurações
   - Permitir trocar entre PT-BR e EN

### 6. Exemplo Completo - Traduzindo a Sidebar

```tsx
// Em /frontend/src/components/sidebar/sidebar-items.tsx

import { useTranslation } from '@/hooks/use-translation';

export function SidebarItems() {
  const { t } = useTranslation();
  
  const items = [
    {
      title: t('nav.dashboard'),
      href: '/dashboard',
      icon: Home,
    },
    {
      title: t('nav.agents'),
      href: '/agents',
      icon: Bot,
    },
    {
      title: t('nav.settings'),
      href: '/settings',
      icon: Settings,
    },
  ];
  
  // resto do código...
}
```

## Observações Importantes

1. **O sistema está configurado mas não aplicado** - Você precisa editar os componentes manualmente
2. **Português como padrão** - O sistema já detecta e usa PT-BR automaticamente
3. **Persistência** - A preferência de idioma é salva no localStorage
4. **Fallback** - Se uma tradução não existir, mostra a chave

## Benefícios

- Interface completamente em português
- Fácil manutenção das traduções
- Possibilidade de adicionar outros idiomas no futuro
- Melhora a experiência para usuários brasileiros

## Como Testar

1. Reconstrua o frontend:
   ```bash
   docker-compose restart frontend
   ```

2. Aplique o hook em um componente

3. Verifique se o texto aparece em português

Se precisar de ajuda para traduzir componentes específicos, me avise!