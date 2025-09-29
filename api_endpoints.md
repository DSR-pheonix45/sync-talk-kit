# Sync Talk Kit API Endpoints Documentation

## Overview
Complete API documentation for the Sync Talk Kit backend, including all endpoints for workbenches, companies, chat, agents, and reports.

## Authentication
All endpoints require Supabase JWT authentication via `Authorization: Bearer <token>` header.

---

## 🏥 Health & Monitoring

### Health Check
- **GET** `/api/healthz` - Liveness probe
- **GET** `/api/readyz` - Readiness probe

---

## 🏢 Companies API

### Company Management
- **POST** `/api/companies` - Create a new company
- **GET** `/api/companies` - List companies user is a member of
- **GET** `/api/companies/{company_id}` - Get specific company details
- **PATCH** `/api/companies/{company_id}` - Update company details (admin only)

### Company Membership
- **POST** `/api/companies/{company_id}/members` - Add member to company (admin only)
- **GET** `/api/companies/{company_id}/members` - List company members
- **PUT** `/api/companies/{company_id}/members/{member_user_id}` - Update member role (admin only)
- **DELETE** `/api/companies/{company_id}/members/{member_user_id}` - Remove member from company (admin only)

---

## 🛠️ Workbenches API

### Workbench Management
- **POST** `/api/workbenches` - Create a new workbench
- **GET** `/api/workbenches` - List accessible workbenches
- **GET** `/api/workbenches?company_id={id}` - Filter by company
- **GET** `/api/workbenches/{workbench_id}` - Get specific workbench

### Workbench Membership
- **POST** `/api/workbenches/{workbench_id}/members` - Add member to workbench (owners only)
- **GET** `/api/workbenches/{workbench_id}/members` - List workbench members
- **PUT** `/api/workbenches/{workbench_id}/members/{member_user_id}` - Update member role (owners only)
- **DELETE** `/api/workbenches/{workbench_id}/members/{member_user_id}` - Remove member from workbench (owners only)

### File Management
- **POST** `/api/workbenches/{workbench_id}/files` - Upload file (multipart/form-data)
- **GET** `/api/workbenches/{workbench_id}/files` - List workbench files
- **GET** `/api/workbenches/{workbench_id}/files/{file_id}/download` - Get file download URL

### Status & Monitoring
- **GET** `/api/workbenches/{workbench_id}/status` - Get indexing status and errors

---

## 🤖 AI Agents API

### Agent Management
- **POST** `/api/agents` - Create a new AI agent
- **GET** `/api/agents` - List user's agents
- **GET** `/api/agents?workbench_id={id}` - Filter by workbench
- **GET** `/api/agents/{agent_id}` - Get specific agent

### Agent Interaction
- **POST** `/api/agents/{agent_id}/query` - Query agent with message
- **GET** `/api/agents/templates` - Get available agent types and templates

### Available Agent Types
1. **dabby_consultant** - Business financial consultant
2. **analyser** - Data analysis specialist
3. **generator** - Financial report generator

---

## 💬 Chat API

### Chat Sessions
- **POST** `/api/chat/sessions` - Create new chat session
- **GET** `/api/chat/sessions` - List user's chat sessions

### Messages
- **POST** `/api/chat/sessions/{session_id}/messages` - Send message and get AI response
- **GET** `/api/chat/sessions/{session_id}/messages` - Get chat message history

---

## 📊 Reports API

### Workbench Reports
- **POST** `/api/reports/workbench` - Generate workbench report
- **GET** `/api/reports/workbench?workbench_id={id}` - List workbench reports
- **GET** `/api/reports/workbench/{report_id}` - Get specific workbench report

### Company Reports
- **POST** `/api/reports/company` - Generate company report
- **GET** `/api/reports/company?company_id={id}` - List company reports
- **GET** `/api/reports/company/{report_id}` - Get specific company report

### Report Templates
1. **financial_summary** - Key financial metrics overview
2. **business_analysis** - Comprehensive business performance
3. **executive_summary** - High-level leadership overview
4. **detailed_financial** - In-depth financial statements
5. **trend_analysis** - Performance trends and forecasting
6. **risk_assessment** - Risk analysis and mitigation
7. **strategic_plan** - Strategic planning document
8. **performance_dashboard** - Visual KPI dashboard

### Output Formats
- **PDF** - Professional printable reports
- **Excel** - Detailed spreadsheets with calculations
- **Word** - Narrative reports with formatting
- **HTML** - Interactive web dashboards
- **JSON** - Structured data format

---

## 🔐 Request/Response Examples

### Authentication
```bash
curl -H "Authorization: Bearer <supabase_jwt_token>" \
     http://localhost:8000/api/workbenches
```

### Create Workbench
```bash
curl -X POST http://localhost:8000/api/workbenches \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Q4 Financial Analysis", "description": "Quarterly financial review"}'
```

### Upload File
```bash
curl -X POST http://localhost:8000/api/workbenches/{workbench_id}/files \
  -H "Authorization: Bearer <token>" \
  -F "file=@financial_report.pdf"
```

### Query Agent
```bash
curl -X POST http://localhost:8000/api/agents/{agent_id}/query \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Analyze our Q4 revenue trends"}'
```

### Generate Report
```bash
curl -X POST http://localhost:8000/api/reports/workbench \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "workbench_id": "workbench-123",
    "template_id": "financial_summary",
    "output_format": "pdf"
  }'
```

---

## 🚀 Frontend Integration

### React Hooks Available
```typescript
// Workbench management
const { createWorkbench, getWorkbenches, uploadFile } = useWorkbenches();

// Company management
const { createCompany, getCompanies, addMember } = useCompanies();

// Chat functionality
const { createSession, sendMessage, getMessages } = useChat();

// Agent interaction
const { createAgent, queryAgent, getTemplates } = useAgents();

// Report generation
const { generateWorkbenchReport, getWorkbenchReports } = useReports();
```

### API Client Usage
```typescript
import { workbenchesApi, agentsApi, chatApi } from '@/lib/api';

// Automatic JWT injection included
const workbenches = await workbenchesApi.getAll();
const response = await agentsApi.query(agentId, { message: "Analyze trends" });
const report = await reportsApi.generateWorkbenchReport(data);
```

---

## 🔒 Security & Permissions

### Authentication
- **Required**: All endpoints require valid Supabase JWT
- **Automatic**: Frontend automatically includes tokens

### Authorization
- **Row Level Security**: Database-level access control
- **Role-Based Access**: Owner/Editor/Viewer permissions
- **Company Inheritance**: Workbench access through company membership

### Data Protection
- **File Security**: Secure storage with access-controlled URLs
- **Input Validation**: Comprehensive request validation
- **Error Handling**: Safe error responses without data leaks

---

## 📈 Monitoring & Observability

### Health Checks
- **Liveness**: `/api/healthz` - Application running
- **Readiness**: `/api/readyz` - Dependencies available

### Logging
- **Structured Logs**: JSON format with correlation IDs
- **Request Tracking**: Full request/response logging
- **Error Monitoring**: Comprehensive error capture

### Performance
- **Response Times**: Monitored and logged
- **Database Queries**: Performance tracking
- **External APIs**: Groq/Supabase performance monitoring

---

## 🚀 Deployment & Scaling

### Production Ready
- **Docker**: Production container with health checks
- **Environment**: Secure configuration management
- **Monitoring**: Structured logging and metrics
- **Security**: HTTPS, CORS, authentication

### Scalability
- **Stateless**: Horizontal scaling ready
- **Background Jobs**: Async processing with Redis
- **Database**: Optimized queries with proper indexing
- **Caching**: Agent instance caching for performance
