# MCP Server Setup for MES Production Scheduler

## Overview
This project is configured with Model Context Protocol (MCP) servers to enhance Claude Code's capabilities when working with the MES Production Scheduler.

## Available MCP Servers

### 1. PostgreSQL Database Server
- **Purpose**: Direct database queries and schema inspection
- **Connection**: `postgresql://almir:numipipdeedee@192.168.1.25:5432/mes_production`
- **Capabilities**:
  - Query work orders, products, operations
  - Inspect database schema
  - Execute SQL queries for data analysis
  - Monitor database performance

### 2. File System Server
- **Purpose**: Enhanced file operations and project navigation
- **Root**: Project directory
- **Capabilities**:
  - Read/write files across the entire project
  - Search for files and content
  - Navigate project structure efficiently
  - Monitor file changes

### 3. Web Search Server
- **Purpose**: Real-time web searches for documentation and troubleshooting
- **API**: Brave Search API (requires API key)
- **Capabilities**:
  - Search for React/FastAPI documentation
  - Find troubleshooting solutions
  - Research best practices
  - Get latest library information

### 4. Git Server
- **Purpose**: Advanced Git operations and repository management
- **Repository**: Current project repository
- **Capabilities**:
  - Advanced Git history analysis
  - Branch management
  - Commit analysis
  - Repository statistics

### 5. Fetch Server
- **Purpose**: HTTP/HTTPS content fetching and web scraping
- **Capabilities**:
  - Fetch web pages and APIs
  - Download documentation and resources
  - Access REST APIs for integration
  - Retrieve real-time data from web services

### 6. Context7 Server
- **Purpose**: Context management and memory enhancement
- **Capabilities**:
  - Maintain conversation context across sessions
  - Store and retrieve project-specific information
  - Manage long-term memory for development tasks
  - Context-aware assistance and recommendations

## Configuration File Location
The MCP configuration is stored in: `claude_desktop_config.json`

## Setup Instructions

### 1. Copy Configuration to Claude Desktop
Copy the `claude_desktop_config.json` file to your Claude Desktop configuration directory:

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### 2. Install MCP Server Dependencies
The MCP servers will be automatically installed via npx when first used, but you can pre-install them:

```bash
npm install -g @modelcontextprotocol/server-postgres
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-web-search
npm install -g @modelcontextprotocol/server-git
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-context7
```

### 3. Configure Web Search API Key
For the web search server, you'll need a Brave Search API key:

1. Go to https://api.search.brave.com/
2. Sign up for an API key
3. Replace `your-brave-api-key-here` in the configuration

### 4. Restart Claude Desktop
After copying the configuration file, restart Claude Desktop for the changes to take effect.

## Usage Examples

### Database Queries
```sql
-- Find all urgent work orders
SELECT * FROM work_orders WHERE priority_level = 1;

-- Get work center utilization
SELECT wc.name, COUNT(o.id) as operation_count 
FROM work_centers wc 
LEFT JOIN operations o ON wc.id = o.work_center_id 
GROUP BY wc.id, wc.name;
```

### File Operations
- Read configuration files
- Search for specific code patterns
- Monitor log files
- Navigate complex project structures

### Web Search
- "FastAPI async database best practices"
- "React TypeScript drag and drop scheduling"
- "PostgreSQL performance optimization"

### Git Operations
- Analyze commit history
- Find code changes by author
- Track feature development
- Generate repository statistics

### Fetch Operations
- Fetch API documentation from official sources
- Download configuration files and templates
- Access external REST APIs for integration
- Retrieve real-time data from web services

### Context7 Operations
- Maintain development session context
- Store project-specific knowledge
- Remember coding patterns and decisions
- Context-aware code suggestions

## Security Considerations

- Database credentials are included in the configuration
- File system access is limited to the project directory
- Web search API key should be kept secure
- Git operations are read-only by default

## Troubleshooting

### Common Issues
1. **MCP Server Not Found**: Ensure npx is installed and accessible
2. **Database Connection Failed**: Verify PostgreSQL server is running at 192.168.1.25
3. **File Access Denied**: Check file permissions in project directory
4. **Web Search Rate Limited**: Monitor API key usage

### Testing MCP Servers
You can test MCP server functionality by asking Claude to:
- Query the database schema
- Read specific project files
- Search for documentation
- Analyze Git history

## Benefits for Development

- **Faster Development**: Direct database access without manual queries
- **Better Context**: Real-time file system awareness
- **Enhanced Debugging**: Direct access to logs and configuration
- **Research Integration**: Web search integrated into development workflow
- **Version Control**: Advanced Git operations and history analysis
- **Web Integration**: Direct HTTP/HTTPS content fetching and API access
- **Context Awareness**: Persistent memory and context management across sessions