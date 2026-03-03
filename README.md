# GitHub Copilot CLI

## Bootstrap Prompt

### Step 1: Setup the Instructions

I want to be able to run the sample that is located in this GitHub repo folder - https://github.com/microsoft/Agents/tree/main/samples/python/copilotstudio-client. Can you download just the folder mentioned and put it into a "Sample" folder within this repo so that I can run it here through the terminal?

```
cd Sample

python3 -m venv ./.venv
source ./.venv/bin/activate
pip install -r requirements.txt

python3 -m src.main

```

### Step 2: Launch GitHub Copilot

```bash

# It is good to do this right away
az login

# Launch GitHub Copilot CLI
copilot --yolo

# Log into GitHub
> /login

# Initialize the session with prompt from above
> /init

# Add plugins if desired

# Microsoft Work IQ
> /plugin marketplace add github/copilot-plugins
> /plugin install workiq@copilot-plugins 

# Microsoft Learn Docs
> /plugin marketplace add microsoftdocs/mcp
> /plugin install microsoft-docs@microsoft-docs-marketplace

```

### Step 3: Possible MCP Servers

- **Azure MCP** - `npx -y @azure/mcp@latest server start`
- **Microsoft Fabric** - `npx -y @microsoft/fabric-mcp@latest server start --mode all   `
- **Playwright** - `npx -y @playwright/mcp@latest`
- **Azure DevOps** - `npx -y @azure-devops/mcp your-org-name`
