from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from services.supabase import DBConnection
from utils.auth_utils import get_current_user_id_from_jwt
from utils.logger import logger
from pydantic import BaseModel

router = APIRouter(prefix="/integrations", tags=["integrations"])

db = None

def initialize(database: DBConnection):
    """Initialize the integrations API with database connection."""
    global db
    db = database

class OAuthIntegration(BaseModel):
    trigger_id: str
    provider: str
    name: str
    is_active: bool
    workspace_name: str = ""
    bot_name: str = ""
    installed_at: str
    created_at: str

class OAuthIntegrationStatus(BaseModel):
    agent_id: str
    integrations: List[OAuthIntegration]

@router.get("/status/{agent_id}", response_model=OAuthIntegrationStatus)
async def get_integration_status(
    agent_id: str,
    user_id: str = Depends(get_current_user_id_from_jwt)
):
    """Get OAuth integration status for an agent."""
    try:
        # Verify agent ownership
        client = await db.client
        agent_result = await client.table('agents').select('account_id').eq('agent_id', agent_id).execute()
        
        if not agent_result.data:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        if agent_result.data[0]['account_id'] != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Get all triggers for the agent that are OAuth integrations
        triggers_result = await client.table('triggers').select('*').eq(
            'agent_id', agent_id
        ).in_('trigger_type', ['slack', 'discord', 'teams']).execute()
        
        integrations = []
        for trigger in triggers_result.data:
            config = trigger.get('config', {})
            integration = OAuthIntegration(
                trigger_id=trigger['trigger_id'],
                provider=trigger['trigger_type'],
                name=trigger['name'],
                is_active=trigger['is_active'],
                workspace_name=config.get('workspace_name', ''),
                bot_name=config.get('bot_name', ''),
                installed_at=trigger['created_at'],
                created_at=trigger['created_at']
            )
            integrations.append(integration)
        
        return OAuthIntegrationStatus(
            agent_id=agent_id,
            integrations=integrations
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting integration status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

class InstallRequest(BaseModel):
    agent_id: str
    provider: str

class InstallResponse(BaseModel):
    install_url: str
    provider: str

@router.post("/install", response_model=InstallResponse)
async def install_integration(
    request: InstallRequest,
    user_id: str = Depends(get_current_user_id_from_jwt)
):
    """Initiate OAuth installation for an integration."""
    try:
        # Verify agent ownership
        client = await db.client
        agent_result = await client.table('agents').select('account_id').eq('agent_id', request.agent_id).execute()
        
        if not agent_result.data:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        if agent_result.data[0]['account_id'] != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Generate OAuth URL based on provider
        if request.provider == 'slack':
            install_url = "https://slack.com/oauth/v2/authorize?client_id=YOUR_SLACK_CLIENT_ID&scope=channels:history,chat:write,channels:read"
        elif request.provider == 'discord':
            install_url = "https://discord.com/api/oauth2/authorize?client_id=YOUR_DISCORD_CLIENT_ID&permissions=2048&scope=bot"
        elif request.provider == 'teams':
            install_url = "https://teams.microsoft.com/apps/YOUR_TEAMS_APP_ID"
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {request.provider}")
        
        # In a real implementation, you would:
        # 1. Generate a state parameter for security
        # 2. Store the state with the agent_id in Redis/DB
        # 3. Include proper redirect URIs
        # 4. Use actual OAuth app credentials
        
        return InstallResponse(
            install_url=install_url,
            provider=request.provider
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initiating integration installation: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/uninstall/{trigger_id}")
async def uninstall_integration(
    trigger_id: str,
    user_id: str = Depends(get_current_user_id_from_jwt)
):
    """Uninstall an OAuth integration."""
    try:
        client = await db.client
        
        # Get trigger to verify ownership
        trigger_result = await client.table('triggers').select('agent_id').eq('trigger_id', trigger_id).execute()
        
        if not trigger_result.data:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        agent_id = trigger_result.data[0]['agent_id']
        
        # Verify agent ownership
        agent_result = await client.table('agents').select('account_id').eq('agent_id', agent_id).execute()
        
        if not agent_result.data:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        if agent_result.data[0]['account_id'] != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Delete the trigger
        await client.table('triggers').delete().eq('trigger_id', trigger_id).execute()
        
        logger.info(f"Uninstalled integration {trigger_id} for agent {agent_id}")
        
        return {"message": "Integration uninstalled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uninstalling integration: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")