// PATCH TEMPORÁRIO - Remove verificação de flags
// Este arquivo força todas as flags a serem true

// Substitui a função isFlagEnabled globalmente
if (typeof window !== 'undefined') {
  // Patch para o browser
  window.__patchedFlags = true;
  
  // Override da função em todos os contextos possíveis
  const originalFetch = window.fetch;
  window.fetch = function(...args) {
    const url = args[0];
    
    // Se for uma requisição de feature flag, retorna sempre true
    if (typeof url === 'string' && url.includes('/feature-flags/')) {
      return Promise.resolve({
        ok: true,
        status: 200,
        json: () => Promise.resolve({ flag_name: 'custom_agents', enabled: true })
      });
    }
    
    return originalFetch.apply(this, args);
  };
}

// Export para uso em módulos
export const isFlagEnabled = () => Promise.resolve(true);
export const isEnabled = () => Promise.resolve(true);