# MCP Server Setup Guide

## Overview

The Blaze documentation site includes a built-in **Model Context Protocol (MCP)** server powered by [`vitepress-plugin-mcp`](https://github.com/Hal-Spidernight/vitepress-plugin-mcp). This allows AI coding agents — such as **GitHub Copilot coding agent** — to search and reference the Blaze documentation directly from your development environment.

The MCP server **starts automatically** whenever the VitePress dev server is running. No additional setup is required to launch it.

## How It Works

When you run the dev server with `npm run dev`, the MCP plugin automatically:

1. Indexes all documentation pages
2. Starts a Streamable HTTP server at `http://localhost:4000/mcp`
3. Starts an SSE (Server-Sent Events) server at `http://localhost:4000/mcp/__sse`

The MCP server exposes a `search_vitepress_docs` tool that AI agents can use to search the documentation using keywords.

## Quick Start

### 1. Start the Dev Server

```bash
npm run dev
```

You should see the following output confirming the MCP server is running:

```
MCPPlugin is running...

  Starting MCP server...
VitePress Plugin MCP
  Stremable Server is running on http://localhost:4000/mcp
  SSE Server is running on http://localhost:4000/mcp/__sse
```

### 2. Configure Your AI Agent

Use the MCP server URL in your agent configuration (see below for specific agent setup guides).

## GitHub Copilot Coding Agent Setup

### Automatic Setup (Copilot Coding Agent)

The repository includes a `.github/copilot-setup-steps.yml` file that automatically starts the VitePress dev server (and MCP server) before the Copilot coding agent begins working. This means the agent can use the `search_vitepress_docs` MCP tool out of the box — no manual server startup required.

The setup steps:

1. Install Node.js and project dependencies
2. Start the dev server in the background (`npm run dev`)
3. Wait for the MCP server on port 4000 to be ready

### VS Code User Settings (Alternative)

You can also add the MCP server to your VS Code user settings (`Ctrl+Shift+P` → "Preferences: Open User Settings (JSON)"):

```json
{
  "mcp": {
    "servers": {
      "blaze-docs": {
        "type": "http",
        "url": "http://localhost:4000/mcp",
        "tools": ["search_vitepress_docs"]
      }
    }
  }
}
```

### Workspace-Level Configuration (Recommended)

For project-specific setup, the repository already includes a `.vscode/mcp.json` file:

```json
{
  "mcpServers": {
    "blaze-docs": {
      "type": "http",
      "url": "http://localhost:4000/mcp",
      "tools": ["search_vitepress_docs"]
    }
  }
}
```

This means anyone cloning the repo automatically gets the MCP server configured in their VS Code workspace — just run `npm run dev` and the agent can search the docs.

## Other AI Agent Configurations

### Claude Desktop

Add to your Claude Desktop config file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "blaze-docs": {
      "type": "http",
      "url": "http://localhost:4000/mcp",
      "tools": ["search_vitepress_docs"]
    }
  }
}
```

### Cursor

Add to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "blaze-docs": {
      "type": "sse",
      "url": "http://localhost:4000/mcp/__sse",
      "tools": ["search_vitepress_docs"]
    }
  }
}
```

### Generic MCP Client

Any MCP-compatible client can connect using:

```json
{
  "mcpServers": {
    "blaze-docs": {
      "type": "http",
      "url": "http://localhost:4000/mcp",
      "tools": ["search_vitepress_docs"]
    }
  }
}
```

| Transport | Type | URL |
|-----------|------|-----|
| Streamable HTTP | `http` | `http://localhost:4000/mcp` |
| SSE | `sse` | `http://localhost:4000/mcp/__sse` |

## Available MCP Tools

| Tool Name | Description |
|-----------|-------------|
| `search_vitepress_docs` | Search the Blaze documentation. Provide up to five keywords as single words (e.g., `BrightOS`, `Arduino`, `plugins`, `tutorials`, `setup`). |

### Example Usage

Once configured, you can ask your AI agent things like:

- *"Search the Blaze docs for how to set up BrightOS"*
- *"Find documentation about plugin development"*
- *"Look up the build guide in the project docs"*

The agent will use the `search_vitepress_docs` tool to find relevant documentation pages and include the information in its responses.

## Auto-Start Behavior

The MCP server is integrated directly into the VitePress configuration (`docs/.vitepress/config.mjs`) as a Vite plugin:

```javascript
import { MCPPlugin } from 'vitepress-plugin-mcp'

export default defineConfig({
  // ...
  vite: {
    plugins: [
      MCPPlugin({ port: 4000 }),
      // ... other plugins
    ]
  }
})
```

This means:

- ✅ **Auto-starts** with `npm run dev` — no separate process needed
- ✅ **Auto-indexes** all documentation pages
- ✅ **Auto-restarts** when documentation files change (hot reload)
- ❌ Does **not** run during `npm run build` (production builds skip the MCP server)

## Configuration

The MCP plugin is configured in `docs/.vitepress/config.mjs`:

```javascript
MCPPlugin({ port: 4000 })
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `port` | `4000` | The port the MCP server listens on |

To change the port, update the value in `config.mjs` and update your agent configuration to match.

## Troubleshooting

### MCP server doesn't start

- Make sure the dev server is running: `npm run dev`
- Check that `vitepress-plugin-mcp` is installed: `npm ls vitepress-plugin-mcp`
- Verify `themeConfig.search.options` is defined in `config.mjs` (required by the plugin)

### Agent can't connect

- Confirm the dev server is running and the MCP server output appears in the terminal
- Check that the port (default `4000`) is not in use by another process
- Verify the URL matches your transport type (`/mcp` for Streamable HTTP, `/mcp/__sse` for SSE)
- Try `curl http://localhost:4000/mcp` to test connectivity

### No search results

- The search index is built from VitePress's local search. Make sure `themeConfig.search.provider` is set to `'local'`
- Try restarting the dev server to rebuild the search index
- Ensure your documentation pages have content (empty pages won't be indexed)

### Port conflict

If port `4000` is already in use:

1. Update `config.mjs`:
   ```javascript
   MCPPlugin({ port: 4001 })
   ```
2. Update your agent configuration URL to use the new port

## Architecture

```
Developer's Machine
├── VS Code / Editor
│   └── GitHub Copilot (or other AI agent)
│       └── MCP Client → connects to MCP Server
│
├── VitePress Dev Server (port 5173)
│   └── vitepress-plugin-mcp
│       └── MCP Server (port 4000)
│           ├── /mcp (Streamable HTTP)
│           └── /mcp/__sse (SSE)
│
└── Documentation Source (docs/)
    └── Indexed by VitePress local search
        └── Available via search_vitepress_docs tool
```

## Resources

- [vitepress-plugin-mcp on GitHub](https://github.com/Hal-Spidernight/vitepress-plugin-mcp)
- [vitepress-plugin-mcp on npm](https://www.npmjs.com/package/vitepress-plugin-mcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [VS Code MCP Support](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
