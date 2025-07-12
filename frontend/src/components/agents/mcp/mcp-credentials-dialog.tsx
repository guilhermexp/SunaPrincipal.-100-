import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Key, Eye, EyeOff, Save, AlertCircle } from 'lucide-react';
import { MCPConfiguration } from './types';
import { useCredentialProfilesForMcp } from '@/hooks/react-query/mcp/use-credential-profiles';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

interface MCPCredentialsDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  mcp: MCPConfiguration;
  onSave: (config: MCPConfiguration) => void;
}

export const MCPCredentialsDialog: React.FC<MCPCredentialsDialogProps> = ({
  open,
  onOpenChange,
  mcp,
  onSave
}) => {
  const [showCredentials, setShowCredentials] = useState(false);
  const [config, setConfig] = useState<any>(mcp.config || {});
  const [selectedProfileId, setSelectedProfileId] = useState(mcp.selectedProfileId || '');
  
  const { data: profiles = [] } = useCredentialProfilesForMcp(mcp.qualifiedName);

  useEffect(() => {
    setConfig(mcp.config || {});
    setSelectedProfileId(mcp.selectedProfileId || '');
  }, [mcp]);

  const handleSave = () => {
    const updatedMcp: MCPConfiguration = {
      ...mcp,
      config,
      selectedProfileId: selectedProfileId || undefined
    };
    onSave(updatedMcp);
    onOpenChange(false);
  };

  const handleConfigChange = (key: string, value: string) => {
    setConfig({
      ...config,
      [key]: value
    });
  };

  // Get required fields based on MCP type
  const getRequiredFields = () => {
    // This should be dynamic based on the MCP server requirements
    // For now, we'll show common fields
    const fields = [];
    
    if (mcp.qualifiedName.includes('github')) {
      fields.push({ key: 'github_token', label: 'GitHub Token', type: 'password' });
    } else if (mcp.qualifiedName.includes('slack')) {
      fields.push({ key: 'slack_token', label: 'Slack Token', type: 'password' });
    } else if (mcp.qualifiedName.includes('notion')) {
      fields.push({ key: 'notion_token', label: 'Notion Token', type: 'password' });
    } else {
      // Generic fields
      fields.push({ key: 'api_key', label: 'API Key', type: 'password' });
    }
    
    return fields;
  };

  const requiredFields = getRequiredFields();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md" aria-describedby="mcp-credentials-description">
        <DialogHeader>
          <DialogTitle>Configure {mcp.name}</DialogTitle>
          <DialogDescription id="mcp-credentials-description">
            Set up credentials and configuration for this MCP server
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          {/* Profile Selection */}
          {profiles.length > 0 && (
            <div className="space-y-2">
              <Label>Credential Profile</Label>
              <Select value={selectedProfileId} onValueChange={setSelectedProfileId}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a credential profile" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">None (Manual Configuration)</SelectItem>
                  {profiles.map((profile) => (
                    <SelectItem key={profile.profile_id} value={profile.profile_id}>
                      {profile.profile_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {selectedProfileId && (
                <p className="text-xs text-muted-foreground">
                  Using saved credentials from profile
                </p>
              )}
            </div>
          )}

          {/* Manual Configuration */}
          {(!selectedProfileId || profiles.length === 0) && (
            <>
              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  Enter the required credentials for {mcp.name}. These will be stored securely.
                </AlertDescription>
              </Alert>

              <div className="space-y-4">
                {requiredFields.map((field) => (
                  <div key={field.key} className="space-y-2">
                    <Label htmlFor={field.key}>{field.label}</Label>
                    <div className="relative">
                      <Input
                        id={field.key}
                        type={field.type === 'password' && !showCredentials ? 'password' : 'text'}
                        value={config[field.key] || ''}
                        onChange={(e) => handleConfigChange(field.key, e.target.value)}
                        placeholder={`Enter ${field.label.toLowerCase()}`}
                        className="pr-10"
                      />
                      {field.type === 'password' && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          className="absolute right-0 top-0 h-full px-3 hover:bg-transparent"
                          onClick={() => setShowCredentials(!showCredentials)}
                        >
                          {showCredentials ? (
                            <EyeOff className="h-4 w-4" />
                          ) : (
                            <Eye className="h-4 w-4" />
                          )}
                        </Button>
                      )}
                    </div>
                  </div>
                ))}

                {/* Additional Configuration */}
                <div className="space-y-2">
                  <Label htmlFor="additional">Additional Configuration (JSON)</Label>
                  <textarea
                    id="additional"
                    className="w-full min-h-[100px] p-2 border rounded-md font-mono text-xs"
                    value={JSON.stringify(config, null, 2)}
                    onChange={(e) => {
                      try {
                        const parsed = JSON.parse(e.target.value);
                        setConfig(parsed);
                      } catch (err) {
                        // Invalid JSON, ignore
                      }
                    }}
                    placeholder="{}"
                  />
                </div>
              </div>
            </>
          )}

          {/* Current Configuration Display */}
          {Object.keys(config).length > 0 && (
            <div className="space-y-2">
              <Label>Current Configuration</Label>
              <div className="p-3 bg-muted rounded-md">
                <pre className="text-xs font-mono overflow-x-auto">
                  {JSON.stringify(
                    Object.entries(config).reduce((acc, [key, value]) => {
                      if (key.includes('token') || key.includes('key') || key.includes('secret')) {
                        acc[key] = showCredentials ? value : '***********';
                      } else {
                        acc[key] = value;
                      }
                      return acc;
                    }, {} as any),
                    null,
                    2
                  )}
                </pre>
              </div>
            </div>
          )}
        </div>

        <div className="flex justify-end gap-2 mt-6">
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button onClick={handleSave}>
            <Save className="h-4 w-4 mr-2" />
            Save Configuration
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};