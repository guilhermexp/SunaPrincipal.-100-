import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Zap, Server, Store, Globe } from 'lucide-react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { MCPConfigurationProps, MCPConfiguration as MCPConfigurationType } from './types';
import { ConfiguredMcpList } from './configured-mcp-list';
import { CustomMCPDialog } from './custom-mcp-dialog';
import { PipedreamRegistry } from '@/components/agents/pipedream/pipedream-registry';
import { ToolsManager } from './tools-manager';
import { MCPServerBrowser } from './mcp-server-browser';
import { MCPCredentialsDialog } from './mcp-credentials-dialog';

export const MCPConfigurationNew: React.FC<MCPConfigurationProps> = ({
  configuredMCPs,
  onConfigurationChange,
  agentId
}) => {
  const [showCustomDialog, setShowCustomDialog] = useState(false);
  const [showRegistryDialog, setShowRegistryDialog] = useState(false);
  const [showMCPBrowser, setShowMCPBrowser] = useState(false);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [showPipedreamToolsManager, setShowPipedreamToolsManager] = useState(false);
  const [showCustomToolsManager, setShowCustomToolsManager] = useState(false);
  const [selectedMCPForTools, setSelectedMCPForTools] = useState<MCPConfigurationType | null>(null);
  const [selectedAgentId, setSelectedAgentId] = useState<string | undefined>(agentId);
  const [showCredentialsDialog, setShowCredentialsDialog] = useState(false);
  const [selectedMCPForCredentials, setSelectedMCPForCredentials] = useState<MCPConfigurationType | null>(null);

  useEffect(() => {
    setSelectedAgentId(agentId);
  }, [agentId]);

  const handleAgentChange = (newAgentId: string | undefined) => {
    setSelectedAgentId(newAgentId);
  };

  const handleEditMCP = (index: number) => {
    const mcp = configuredMCPs[index];
    if (mcp.customType === 'pipedream') {
      setEditingIndex(index);
      setShowCustomDialog(true);
    } else {
      setEditingIndex(index);
      setShowCustomDialog(true);
    }
  };

  const handleEditCredentials = (index: number) => {
    const mcp = configuredMCPs[index];
    setSelectedMCPForCredentials(mcp);
    setShowCredentialsDialog(true);
  };

  const handleConfigureTools = (index: number) => {
    const mcp = configuredMCPs[index];
    setSelectedMCPForTools(mcp);
    if (mcp.customType === 'pipedream') {
      const profileId = mcp.selectedProfileId || mcp.config?.profile_id;
      if (profileId) {
        setShowPipedreamToolsManager(true);
      } else {
        console.warn('Pipedream MCP has no profile_id:', mcp);
      }
    } else {
      setShowCustomToolsManager(true);
    }
  };

  const handleRemoveMCP = (index: number) => {
    const newMCPs = [...configuredMCPs];
    newMCPs.splice(index, 1);
    onConfigurationChange(newMCPs);
  };

  const handleSaveCustomMCP = (customConfig: any) => {
    const mcpConfig: MCPConfigurationType = {
      name: customConfig.name,
      qualifiedName: `custom_${customConfig.type}_${Date.now()}`,
      config: customConfig.config,
      enabledTools: customConfig.enabledTools,
      selectedProfileId: customConfig.selectedProfileId,
      isCustom: true,
      customType: customConfig.type as 'http' | 'sse'
    };
    onConfigurationChange([...configuredMCPs, mcpConfig]);
  };

  const handleToolsSelected = (profileId: string, selectedTools: string[], appName: string, appSlug: string) => {
    const pipedreamMCP: MCPConfigurationType = {
      name: appName,
      qualifiedName: `pipedream_${appSlug}_${profileId}`,
      config: {
        url: 'https://remote.mcp.pipedream.net',
        headers: {
          'x-pd-app-slug': appSlug,
        },
        profile_id: profileId
      },
      enabledTools: selectedTools,
      isCustom: true,
      customType: 'pipedream',
      selectedProfileId: profileId
    };
    const nonPipedreamMCPs = configuredMCPs.filter(mcp => 
      mcp.customType !== 'pipedream' || 
      mcp.selectedProfileId !== profileId
    );
    onConfigurationChange([...nonPipedreamMCPs, pipedreamMCP]);
    setShowRegistryDialog(false);
  };

  const handlePipedreamToolsUpdate = (enabledTools: string[]) => {
    if (!selectedMCPForTools) return;
    
    const updatedMCPs = configuredMCPs.map(mcp => 
      mcp === selectedMCPForTools 
        ? { ...mcp, enabledTools }
        : mcp
    );
    onConfigurationChange(updatedMCPs);
    setShowPipedreamToolsManager(false);
    setSelectedMCPForTools(null);
  };

  const handleCustomToolsUpdate = (enabledTools: string[]) => {
    if (!selectedMCPForTools) return;
    
    const updatedMCPs = configuredMCPs.map(mcp => 
      mcp === selectedMCPForTools 
        ? { ...mcp, enabledTools }
        : mcp
    );
    onConfigurationChange(updatedMCPs);
    setShowCustomToolsManager(false);
    setSelectedMCPForTools(null);
  };

  const handleMCPServerSelect = (server: any) => {
    // Create a configuration for the selected MCP server
    const mcpConfig: MCPConfigurationType = {
      name: server.displayName,
      qualifiedName: server.qualifiedName,
      config: {
        // The configuration will need to be set up based on the server requirements
        // For now, we'll just store the basic info
        serverUrl: `https://server.smithery.ai/${server.qualifiedName}/mcp`,
        requiresConfig: true
      },
      enabledTools: [],
      isCustom: false,
      customType: undefined
    };
    
    // Add to the list of configured MCPs
    onConfigurationChange([...configuredMCPs, mcpConfig]);
    setShowMCPBrowser(false);
    
    // Open credentials dialog for configuration
    setSelectedMCPForCredentials(mcpConfig);
    setShowCredentialsDialog(true);
  };

  const handleSaveCredentials = (updatedMcp: MCPConfigurationType) => {
    const updatedMCPs = configuredMCPs.map(mcp => 
      mcp.qualifiedName === updatedMcp.qualifiedName ? updatedMcp : mcp
    );
    onConfigurationChange(updatedMCPs);
    setShowCredentialsDialog(false);
    setSelectedMCPForCredentials(null);
  };

  return (
    <div className="flex flex-col">
      <div className="flex-1 min-h-0 overflow-y-auto">
        {configuredMCPs.length === 0 && (
          <div className="text-center py-12 px-6 bg-muted/30 rounded-xl border-2 border-dashed border-border">
            <div className="mx-auto w-12 h-12 bg-muted rounded-full flex items-center justify-center mb-4">
              <Zap className="h-6 w-6 text-muted-foreground" />
            </div>
            <h4 className="text-sm font-medium text-foreground mb-2">
              No integrations configured
            </h4>
            <p className="text-sm text-muted-foreground mb-6 max-w-sm mx-auto">
              Browse the app registry to connect your apps through Pipedream or add custom MCP servers
            </p>
            <div className="flex gap-2 justify-center flex-wrap">
              <Button onClick={() => setShowMCPBrowser(true)} variant="default">
                <Globe className="h-4 w-4 mr-1" />
                Browse MCPs
              </Button>
              <Button onClick={() => setShowRegistryDialog(true)} variant="outline">
                <Store className="h-4 w-4 mr-1" />
                Pipedream Apps
              </Button>
              <Button onClick={() => setShowCustomDialog(true)} variant="outline">
                <Server className="h-4 w-4 mr-1" />
                Custom MCP
              </Button>
            </div>
          </div>
        )}
        
        {configuredMCPs.length > 0 && (
          <div className="space-y-4">
            <div className="bg-card rounded-xl border border-border overflow-hidden">
              <div className="px-4 py-3 border-b border-border bg-muted/30">
                <h4 className="text-sm font-medium text-foreground">
                  Configured Integrations
                </h4>
              </div>
              <div className="p-2">
                <ConfiguredMcpList
                  configuredMCPs={configuredMCPs}
                  onEdit={handleEditMCP}
                  onRemove={handleRemoveMCP}
                  onConfigureTools={handleConfigureTools}
                  onEditCredentials={handleEditCredentials}
                />
              </div>
            </div>
          </div>
        )}
      </div>
      
      {configuredMCPs.length > 0 && (
        <div className="flex-shrink-0 pt-4 pb-2">
          <div className="flex gap-2 justify-center flex-wrap">
            <Button onClick={() => setShowMCPBrowser(true)} variant="default" size="sm">
              <Globe className="h-4 w-4 mr-1" />
              Browse MCPs
            </Button>
            <Button onClick={() => setShowRegistryDialog(true)} variant="outline" size="sm">
              <Store className="h-4 w-4 mr-1" />
              Pipedream Apps
            </Button>
            <Button onClick={() => setShowCustomDialog(true)} variant="outline" size="sm">
              <Server className="h-4 w-4 mr-1" />
              Custom MCP
            </Button>
          </div>
        </div>
      )}
      
      <Dialog open={showRegistryDialog} onOpenChange={setShowRegistryDialog}>
        <DialogContent className="p-0 max-w-6xl max-h-[90vh] overflow-y-auto" aria-describedby="registry-description">
          <DialogHeader className="sr-only">
            <DialogTitle>Select Integration</DialogTitle>
            <DialogDescription id="registry-description">
              Select and configure integrations for your agent
            </DialogDescription>
          </DialogHeader>
          <PipedreamRegistry showAgentSelector={false} selectedAgentId={selectedAgentId} onAgentChange={handleAgentChange} onToolsSelected={handleToolsSelected} />
        </DialogContent>
      </Dialog>
      <CustomMCPDialog
        open={showCustomDialog}
        onOpenChange={setShowCustomDialog}
        onSave={handleSaveCustomMCP}
      />
      {selectedMCPForTools && selectedMCPForTools.customType === 'pipedream' && (selectedMCPForTools.selectedProfileId || selectedMCPForTools.config?.profile_id) && (
        <ToolsManager
          mode="pipedream"
          agentId={selectedAgentId}
          profileId={selectedMCPForTools.selectedProfileId || selectedMCPForTools.config?.profile_id}
          appName={selectedMCPForTools.name}
          open={showPipedreamToolsManager}
          onOpenChange={setShowPipedreamToolsManager}
          onToolsUpdate={handlePipedreamToolsUpdate}
        />
      )}
      {selectedMCPForTools && selectedMCPForTools.customType !== 'pipedream' && (
        <ToolsManager
          mode="custom"
          agentId={selectedAgentId}
          mcpConfig={selectedMCPForTools.config}
          mcpName={selectedMCPForTools.name}
          open={showCustomToolsManager}
          onOpenChange={setShowCustomToolsManager}
          onToolsUpdate={handleCustomToolsUpdate}
        />
      )}
      <MCPServerBrowser
        open={showMCPBrowser}
        onOpenChange={setShowMCPBrowser}
        onServerSelect={handleMCPServerSelect}
        selectedAgentId={selectedAgentId}
      />
      
      {/* Credentials Dialog */}
      {showCredentialsDialog && selectedMCPForCredentials && (
        <MCPCredentialsDialog
          open={showCredentialsDialog}
          onOpenChange={setShowCredentialsDialog}
          mcp={selectedMCPForCredentials}
          onSave={handleSaveCredentials}
        />
      )}
    </div>
  );
};