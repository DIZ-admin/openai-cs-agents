# ERNI Gruppe Building Agents - Frontend Guide

## 🚀 Quick Start

### Start Frontend Development Server
```bash
cd ui
npm run dev:next
```

The application will be available at:
- **Local:** http://localhost:3000
- **Network:** http://192.168.1.182:3000

## 📋 Prerequisites

### Required Software
- **Node.js:** v23.11.0 (or compatible version)
- **npm:** 10.9.2 (or compatible version)
- **Backend:** Must be running on http://127.0.0.1:8000

### Verify Installation
```bash
node --version  # Should show v23.x.x or higher
npm --version   # Should show 10.x.x or higher
```

## 🔧 Installation

### First Time Setup
```bash
# Navigate to UI directory
cd ui

# Install dependencies (automatically uses pnpm)
npm install

# Or manually with pnpm
pnpm install
```

### Dependencies Installed
- **Next.js:** 15.5.4 (React framework)
- **React:** 19.2.0
- **TypeScript:** 5.9.3
- **Tailwind CSS:** 3.4.18 (styling)
- **Radix UI:** Component library
- **Lucide React:** Icons
- **react-markdown:** Markdown rendering
- **OpenAI SDK:** 4.104.0

## 🌐 API Configuration

### Proxy Setup (next.config.mjs)
The frontend uses Next.js rewrites to proxy API requests to the backend:

```javascript
async rewrites() {
  return [
    {
      source: "/chat",
      destination: "http://127.0.0.1:8000/chat",
    },
  ];
}
```

**Benefits:**
- No CORS issues
- Simplified API calls
- Backend URL hidden from client
- Easy to change backend URL

### API Client (lib/api.ts)
```typescript
export async function callChatAPI(message: string, conversationId: string) {
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ conversation_id: conversationId, message }),
  });
  return res.json();
}
```

## 🎨 UI Components

### Main Page (app/page.tsx)
- **State Management:** React hooks (useState, useEffect)
- **Components:** AgentPanel, Chat
- **Features:** Real-time updates, conversation persistence

### Agent Panel (components/agent-panel.tsx)
Displays:
- Available agents (6 ERNI agents)
- Active guardrails (Input: Relevance, Jailbreak | Output: PII)
- Conversation context (customer data, project info)
- Runner output (agent events, tool calls)

### Guardrails Component (components/guardrails.tsx)
Displays security and validation checks for agent interactions:

**Input Guardrails** (validate user messages):
- **Relevance Guardrail** - Ensures messages are related to building/construction
- **Jailbreak Guardrail** - Detects attempts to bypass system instructions

**Output Guardrails** (validate agent responses):
- **PII Guardrail** - Prevents exposure of Personally Identifiable Information

Features:
- Unified card-based display for all guardrails
- Real-time status badges (Passed/Failed)
- Color-coded indicators (green for passed, red for failed)
- Detailed descriptions for each guardrail type

### Chat Interface (components/chat.tsx)
Features:
- Message input with send button
- Message history display
- Loading indicator
- Markdown support
- Syntax highlighting

## 🎯 Available Scripts

### Development
```bash
# Start Next.js dev server only
npm run dev:next

# Start both frontend and backend (concurrently)
npm run dev

# Start backend only
npm run dev:server
```

### Production
```bash
# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## 🔍 Testing the Application

### 1. Verify Backend is Running
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

### 2. Start Frontend
```bash
cd ui
npm run dev:next
```

### 3. Open Browser
Navigate to: http://localhost:3000

### 4. Test Chat Functionality
Try these example queries:
- "Hello, I want to build a house"
- "I need a cost estimate for a 150m² Einfamilienhaus"
- "What's the status of project 2024-156?"
- "I want to book a consultation with an architect"
- "Why should I choose wood for my house?"

### 5. Monitor Agent Activity
Watch the left panel to see:
- Which agent is currently active
- Context updates as conversation progresses
- Guardrail checks being performed
- Tool calls and handoffs in runner output

## 🛠️ Development Workflow

### Hot Reload
Next.js automatically reloads when you save changes:
1. Edit any file in `ui/` directory
2. Save the file
3. Browser automatically refreshes
4. Changes appear instantly

### Browser DevTools
Press **F12** to open DevTools:
- **Console:** Check for errors and logs
- **Network:** Monitor API requests
- **React DevTools:** Inspect component state

### Common Development Tasks

#### Add a New Component
```bash
# Create component file
touch components/my-component.tsx

# Import in page.tsx
import { MyComponent } from "@/components/my-component";
```

#### Modify Styling
Edit `app/globals.css` or use Tailwind classes:
```tsx
<div className="bg-blue-500 text-white p-4 rounded-lg">
  Content
</div>
```

#### Update API Endpoint
Edit `lib/api.ts` to add new API calls:
```typescript
export async function callNewAPI(data: any) {
  const res = await fetch("/new-endpoint", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}
```

## 🐛 Troubleshooting

### Port 3000 Already in Use
```bash
# Find process using port 3000
lsof -ti:3000

# Kill the process
kill $(lsof -ti:3000)

# Or use a different port
PORT=3001 npm run dev:next
```

### Backend Not Responding
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not running, start it
cd ../python-backend
.venv/bin/uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

### Dependencies Not Installing
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json pnpm-lock.yaml
npm install
```

### TypeScript Errors
```bash
# Regenerate TypeScript config
npx tsc --init

# Check for type errors
npm run lint
```

### Build Errors
```bash
# Clear Next.js cache
rm -rf .next

# Rebuild
npm run build
```

## 📁 Project Structure

```
ui/
├── app/                      # Next.js App Router
│   ├── page.tsx             # Main page component
│   ├── layout.tsx           # Root layout
│   └── globals.css          # Global styles
├── components/              # React components
│   ├── agent-panel.tsx      # Agent view panel
│   ├── chat.tsx             # Chat interface
│   ├── agents-list.tsx      # Agent cards
│   ├── conversation-context.tsx  # Context display
│   ├── guardrails.tsx       # Guardrail checks (input + output)
│   ├── runner-output.tsx    # Event log
│   └── ui/                  # Reusable UI components
│       ├── badge.tsx
│       ├── card.tsx
│       └── scroll-area.tsx
├── lib/                     # Utilities
│   ├── api.ts              # API client
│   ├── types.ts            # TypeScript types
│   └── utils.ts            # Helper functions
├── public/                  # Static assets
├── next.config.mjs         # Next.js configuration
├── tailwind.config.ts      # Tailwind CSS config
├── tsconfig.json           # TypeScript config
└── package.json            # Dependencies
```

## 🎨 Styling Guide

### ERNI Brand Colors
```css
/* Primary brand color */
#928472  /* Brown/Beige */

/* Usage in Tailwind */
bg-[#928472]
text-[#928472]
border-[#928472]
```

### Tailwind CSS Classes
```tsx
// Layout
<div className="flex flex-col h-screen gap-2 p-4">

// Styling
<div className="bg-white rounded-lg shadow-sm border border-gray-200">

// Typography
<h1 className="text-2xl font-bold text-gray-900">

// Responsive
<div className="w-full md:w-1/2 lg:w-1/3">
```

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Start Production Server
```bash
npm start
```

### Environment Variables
Create `.env.local` for production:
```bash
NEXT_PUBLIC_API_URL=https://api.erni-gruppe.ch
```

## 📚 Additional Resources

- **Next.js Documentation:** https://nextjs.org/docs
- **React Documentation:** https://react.dev
- **Tailwind CSS:** https://tailwindcss.com/docs
- **TypeScript:** https://www.typescriptlang.org/docs
- **Radix UI:** https://www.radix-ui.com

## 🔗 Related Documentation

- **Backend Guide:** `../python-backend/SERVER_CONTROL.md`
- **Agent Documentation:** `../.augment/rules/AGENTS.md`
- **Project README:** `../README.md`
- **Deployment Guide:** `../DEPLOYMENT.md`

---

**Last Updated:** 2025-10-04  
**Next.js Version:** 15.5.4  
**React Version:** 19.2.0  
**Node.js Version:** 23.11.0

