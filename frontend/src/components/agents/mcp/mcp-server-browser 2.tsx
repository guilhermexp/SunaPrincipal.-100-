import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { Search, Server, ExternalLink, AlertCircle, Users, Clock } from 'lucide-react';
import { useMCPServers, usePopularMCPServers } from '@/hooks/react-query/mcp/use-mcp-servers';
import { useDebounce } from '@/hooks/use-debounce';

interface MCPServerBrowserProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onServerSelect: (server: any) => void;
  selectedAgentId?: string;
}

export const MCPServerBrowser: React.FC<MCPServerBrowserProps> = ({
  open,
  onOpenChange,
  onServerSelect
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTab, setSelectedTab] = useState<'popular' | 'all'>('popular');
  const debouncedSearchQuery = useDebounce(searchQuery, 300);

  // Use the appropriate hook based on selected tab
  const { data: allServers, isLoading: isLoadingAll } = useMCPServers(
    selectedTab === 'all' ? debouncedSearchQuery : undefined,
    1,
    50
  );
  
  const { data: popularServers, isLoading: isLoadingPopular } = usePopularMCPServers(1, 50);

  const isLoading = selectedTab === 'popular' ? isLoadingPopular : isLoadingAll;
  const servers = selectedTab === 'popular' 
    ? popularServers?.servers || [] 
    : allServers?.servers || [];

  const handleServerClick = (server: any) => {
    onServerSelect(server);
    onOpenChange(false);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[85vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle>Browse MCP Servers</DialogTitle>
          <DialogDescription>
            Discover and add Model Context Protocol servers from the Smithery registry
          </DialogDescription>
        </DialogHeader>

        <div className="flex-1 flex flex-col space-y-4">
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search MCP servers..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>

          {/* Tab Selection */}
          <div className="flex gap-2">
            <Button
              variant={selectedTab === 'popular' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedTab('popular')}
            >
              Popular
            </Button>
            <Button
              variant={selectedTab === 'all' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedTab('all')}
            >
              All Servers
            </Button>
          </div>

          {/* Server List */}
          <ScrollArea className="flex-1">
            <div className="grid gap-4 pr-4">
              {isLoading ? (
                // Loading skeletons
                Array.from({ length: 6 }).map((_, i) => (
                  <Card key={i} className="cursor-pointer hover:shadow-md transition-shadow">
                    <CardHeader>
                      <Skeleton className="h-6 w-3/4 mb-2" />
                      <Skeleton className="h-4 w-full" />
                    </CardHeader>
                    <CardContent>
                      <Skeleton className="h-4 w-1/2" />
                    </CardContent>
                  </Card>
                ))
              ) : servers.length === 0 ? (
                <div className="text-center py-12">
                  <AlertCircle className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                  <p className="text-muted-foreground">
                    {searchQuery 
                      ? `No MCP servers found matching "${searchQuery}"`
                      : 'No MCP servers available'}
                  </p>
                </div>
              ) : (
                servers.map((server) => (
                  <Card 
                    key={server.qualifiedName} 
                    className="cursor-pointer hover:shadow-md transition-shadow"
                    onClick={() => handleServerClick(server)}
                  >
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <CardTitle className="text-lg flex items-center gap-2">
                            {server.iconUrl ? (
                              <img 
                                src={server.iconUrl} 
                                alt={server.displayName} 
                                className="w-5 h-5 rounded"
                              />
                            ) : (
                              <Server className="h-5 w-5 text-muted-foreground" />
                            )}
                            {server.displayName}
                          </CardTitle>
                          <CardDescription className="mt-1">
                            {server.description}
                          </CardDescription>
                        </div>
                        {server.isDeployed && (
                          <Badge variant="secondary" className="ml-2">
                            Deployed
                          </Badge>
                        )}
                      </div>
                    </CardHeader>
                    <CardContent>
                      <div className="flex items-center gap-4 text-sm text-muted-foreground">
                        {server.useCount > 0 && (
                          <div className="flex items-center gap-1">
                            <Users className="h-3 w-3" />
                            <span>{server.useCount.toLocaleString()} users</span>
                          </div>
                        )}
                        {server.createdAt && (
                          <div className="flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            <span>{new Date(server.createdAt).toLocaleDateString()}</span>
                          </div>
                        )}
                        {server.homepage && (
                          <a
                            href={server.homepage}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-1 hover:text-primary"
                            onClick={(e) => e.stopPropagation()}
                          >
                            <ExternalLink className="h-3 w-3" />
                            <span>Homepage</span>
                          </a>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                ))
              )}
            </div>
          </ScrollArea>
        </div>
      </DialogContent>
    </Dialog>
  );
};