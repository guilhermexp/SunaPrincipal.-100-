# Pipedream Integration Documentation for Suna

## Overview

Pipedream is a powerful workflow automation and integration platform that has been integrated into Suna to provide access to over 2,700+ apps and services. This integration allows Suna agents to interact with external services through OAuth connections and API integrations.

## What is Pipedream?

Pipedream is an integration platform that:
- Provides OAuth-based connections to thousands of third-party services
- Exposes connected apps as Model Context Protocol (MCP) servers
- Enables no-code integration with external APIs
- Manages authentication and credentials securely

## Key Features

### 1. App Connections
- **2,700+ Supported Apps**: Connect to popular services like Google, Slack, GitHub, Salesforce, and thousands more
- **OAuth Authentication**: Secure authentication flow for connecting external accounts
- **Multiple Profiles**: Support for multiple credential profiles per app (e.g., personal and work accounts)

### 2. MCP Integration
- **Automatic Tool Discovery**: When an app is connected, Pipedream automatically discovers available tools/actions
- **Tool Selection**: Users can choose which tools to enable for their agents
- **Real-time Execution**: Agents can call these tools during conversations

### 3. Security
- **Encrypted Credentials**: OAuth tokens are encrypted before storage in Supabase
- **Profile Isolation**: Each credential profile is isolated and can be managed independently
- **Rate Limiting**: Built-in rate limit handling with automatic token management

## How to Use Pipedream in Suna

### Step 1: Configure an Agent with Pipedream

1. Navigate to the Agents page
2. Create or edit an agent
3. Go to the "Integrations" or "MCP Servers" tab
4. Click "Browse Apps" or "Pipedream Apps"

### Step 2: Connect an App

1. Search for the app you want to connect (e.g., "Google Sheets")
2. Click on the app card
3. Create a credential profile with a descriptive name
4. Click "Connect" to start the OAuth flow
5. Authenticate with the external service
6. Return to Suna after successful authentication

### Step 3: Enable Tools

1. After connecting, you'll see available tools for that app
2. Select which tools you want to enable for your agent
3. Save the configuration

### Step 4: Use in Conversations

Once configured, you can ask your agent to use the connected services:

```
"Read my latest emails from Gmail"
"Send a message to #general channel in Slack"
"Create a new issue in my GitHub repository"
"Add a row to my Google Sheet with today's data"
```

## Configuration Requirements

To use Pipedream, the following environment variables must be set in the backend:

```env
PIPEDREAM_PROJECT_ID=<your-project-id>
PIPEDREAM_CLIENT_ID=<your-client-id>
PIPEDREAM_CLIENT_SECRET=<your-client-secret>
PIPEDREAM_X_PD_ENVIRONMENT=development|production
```

## Architecture

### Backend Components

1. **PipedreamClient** (`/backend/pipedream/client.py`)
   - Handles API communication with Pipedream
   - Manages OAuth tokens and rate limiting
   - Discovers MCP servers and tools

2. **Profile Manager** (`/backend/pipedream/profiles.py`)
   - Manages credential profiles
   - Encrypts and stores OAuth tokens
   - Handles profile lifecycle

3. **API Endpoints** (`/backend/pipedream/api.py`)
   - `/pipedream/apps` - List available apps
   - `/pipedream/connection-token` - Create connection tokens
   - `/pipedream/profiles` - Manage credential profiles
   - `/pipedream/mcp/discover` - Discover MCP tools

### Frontend Components

1. **PipedreamRegistry** - Main UI for browsing and connecting apps
2. **PipedreamConnector** - Handles the connection flow
3. **CredentialProfileManager** - Manages credential profiles
4. **ToolsManager** - Allows tool selection and configuration

## Example Use Cases

### 1. CRM Integration
Connect to Salesforce to:
- Look up customer information
- Create new leads
- Update opportunity status
- Generate reports

### 2. Communication Automation
Connect to Slack/Discord to:
- Send notifications
- Monitor channels
- Create threads
- Share files

### 3. Document Management
Connect to Google Drive to:
- Create documents
- Read spreadsheets
- Upload files
- Share with team

### 4. Project Management
Connect to Jira/Asana to:
- Create tasks
- Update ticket status
- Assign work
- Track progress

### 5. Data Analysis
Connect to data sources to:
- Query databases
- Fetch analytics
- Generate visualizations
- Export reports

## Best Practices

1. **Profile Naming**: Use descriptive names for credential profiles (e.g., "Work Gmail", "Personal GitHub")

2. **Tool Selection**: Only enable tools that your agent needs to minimize complexity

3. **Security**: Regularly review and remove unused credential profiles

4. **Rate Limits**: Be aware of API rate limits for connected services

5. **Testing**: Test integrations in a development environment first

## Troubleshooting

### Common Issues

1. **Connection Failed**
   - Check if popup blockers are preventing OAuth window
   - Ensure cookies are enabled for third-party auth
   - Try disconnecting and reconnecting the app

2. **Tools Not Appearing**
   - Refresh the page after connecting
   - Check if the app actually provides MCP tools
   - Verify the profile is marked as "connected"

3. **Rate Limiting**
   - Pipedream handles rate limits automatically
   - If persistent, wait a few minutes before retrying

4. **Missing Apps**
   - Not all Pipedream apps may have MCP tool support
   - Check Pipedream documentation for app availability

## Security Considerations

1. **Credential Storage**: All OAuth tokens are encrypted using Fernet encryption before database storage

2. **Access Control**: Profiles are user-specific and cannot be accessed by other users

3. **Token Refresh**: OAuth tokens are automatically refreshed when needed

4. **Audit Trail**: All connections and tool usage can be monitored through logs

## Future Enhancements

The Pipedream integration is continuously being improved. Planned features include:
- Workflow automation beyond single tool calls
- Custom tool creation
- Enhanced error handling and retry logic
- Bulk operations support
- Advanced filtering and search capabilities

## Support

For issues with Pipedream integration:
1. Check the agent logs for detailed error messages
2. Verify your Pipedream configuration in the backend
3. Ensure the external service is properly connected
4. Contact support with specific error details

## Conclusion

The Pipedream integration transforms Suna from a standalone AI assistant into a powerful automation platform capable of interacting with virtually any web service. This enables agents to perform real-world tasks across multiple platforms, making them significantly more useful for business automation and personal productivity.