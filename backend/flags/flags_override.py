"""
Override temporário para forçar todas as flags como habilitadas
Este arquivo substitui as verificações de flags para sempre retornar True
"""

import logging

logger = logging.getLogger(__name__)

# Lista de flags que devem ser sempre habilitadas
FORCE_ENABLED_FLAGS = {
    'custom_agents',
    'agentPlaygroundFlagFrontend',
    'marketplaceFlagFrontend',
    'agentPlaygroundEnabled',
    'marketplaceEnabled',
    'agent_marketplace',
    'knowledge_base',
    'agent_builder',
    'workflows',
    'scheduling',
    'secure_mcp'
}

async def is_enabled_override(key: str) -> bool:
    """
    Override da função is_enabled para sempre retornar True para flags específicas
    """
    if key in FORCE_ENABLED_FLAGS:
        logger.debug(f"Flag '{key}' forced to True (override active)")
        return True
    
    # Para outras flags, também retorna True por padrão
    logger.debug(f"Flag '{key}' defaulting to True (override active)")
    return True 