# MES Production Scheduler - Technical Architecture

**Date:** July 17, 2025  
**Version:** 1.0.0-alpha  
**Architecture Status:** Foundation Complete

## 🏗️ System Architecture Overview

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        MES Production Scheduler                 │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (React)     │  Backend (FastAPI)    │  Database (PG)  │
│  ┌─────────────────┐  │  ┌─────────────────┐  │  ┌─────────────┐ │
│  │  Components     │  │  │  API Endpoints  │  │  │  Tables     │ │
│  │  ├─Dashboard    │  │  │  ├─Work Orders  │  │  │  ├─orgs     │ │
│  │  ├─WorkOrders   │  │  │  ├─Scheduling   │  │  │  ├─plants   │ │
│  │  ├─Scheduling   │  │  │  ├─Machines     │  │  │  ├─wc_cat   │ │
│  │  └─Machines     │  │  │  └─Operations   │  │  │  ├─work_ctr │ │
│  │                 │  │  │                 │  │  │  ├─products │ │
│  │  Hooks          │  │  │  Services       │  │  │  ├─prod_typ │ │
│  │  ├─useWorkOrders│  │  │  ├─Scheduling   │  │  │  ├─work_ord │ │
│  │  ├─useMachines  │  │  │  ├─Optimization │  │  │  └─operatns │ │
│  │  └─useScheduling│  │  │  └─Validation   │  │  │             │ │
│  └─────────────────┘  │  └─────────────────┘  │  └─────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 🗄️ Database Design

### Entity Relationship Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Organizations  │    │     Plants      │    │ Work Centers    │
│  ──────────────│    │  ──────────────│    │  ──────────────│
│  id (PK)        │    │  id (PK)        │    │  id (PK)        │
│  code           │◄──►│  organization_id│    │  plant_id       │
│  name           │    │  code           │    │  code           │
│  created_at     │    │  name           │    │  name           │
│  updated_at     │    │  location       │    │  description    │
└─────────────────┘    │  is_active      │    │  category_id    │
                       │  created_at     │    │  capacity_h_day │
                       └─────────────────┘    │  setup_time_min │
                                ▲             │  cost_per_hour  │
                                │             │  additional_data│
                                │             │  is_active      │
                                │             │  created_at     │
                                │             └─────────────────┘
                                │                      ▲
                                │                      │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Product Types  │    │    Products     │    │  Work Orders    │
│  ──────────────│    │  ──────────────│    │  ──────────────│
│  id (PK)        │    │  id (PK)        │    │  id (PK)        │
│  type_code      │◄──►│  type_id        │◄──►│  product_id     │
│  type_name      │    │  kpl            │    │  rn             │
│  description    │    │  name           │    │  quantity       │
│  can_have_child │    │  description    │    │  priority_level │
│  sort_order     │    │  priority_level │    │  datum_isporuke │
│  created_at     │    │  is_active      │    │  datum_sastavlj │
└─────────────────┘    │  created_at     │    │  datum_treci    │
                       │  updated_at     │    │  status         │
                       └─────────────────┘    │  created_at     │
                                              │  updated_at     │
                                              └─────────────────┘
                                                       ▲
                                                       │
                                              ┌─────────────────┐
                                              │   Operations    │
                                              │  ──────────────│
                                              │  id (PK)        │
                                              │  work_order_id  │
                                              │  work_center_id │
                                              │  operation_seq  │
                                              │  naziv          │
                                              │  norma          │
                                              │  quantity       │
                                              │  quantity_comp  │
                                              │  status         │
                                              │  est_start_time │
                                              │  est_comp_time  │
                                              │  actual_start   │
                                              │  actual_comp    │
                                              │  created_at     │
                                              │  updated_at     │
                                              └─────────────────┘
```

### Database Schema Details

#### Core Tables
```sql
-- Organizations: Multi-tenant structure
CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Plants: Manufacturing facilities
CREATE TABLE plants (
    id SERIAL PRIMARY KEY,
    organization_id INTEGER REFERENCES organizations(id),
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    location VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, code)
);

-- Work Centers: Production resources
CREATE TABLE work_centers (
    id SERIAL PRIMARY KEY,
    plant_id INTEGER REFERENCES plants(id),
    code VARCHAR(20) NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES work_center_categories(id),
    capacity_hours_per_day DECIMAL(4,2) DEFAULT 8.0,
    setup_time_minutes INTEGER DEFAULT 0,
    cost_per_hour DECIMAL(10,2),
    additional_data JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(plant_id, code)
);

-- Work Orders: Production orders
CREATE TABLE work_orders (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    rn VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    priority_level INTEGER DEFAULT 3,
    datum_isporuke DATE,
    datum_sastavljanja DATE,
    datum_treci DATE,
    status VARCHAR(20) DEFAULT 'pending',
    additional_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Operations: Manufacturing operations
CREATE TABLE operations (
    id SERIAL PRIMARY KEY,
    work_order_id INTEGER REFERENCES work_orders(id),
    work_center_id INTEGER REFERENCES work_centers(id),
    operation_sequence INTEGER NOT NULL,
    naziv VARCHAR(500) NOT NULL,
    norma DECIMAL(10,2),
    quantity INTEGER NOT NULL DEFAULT 1,
    quantity_completed INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    estimated_start_time TIMESTAMP,
    estimated_completion_time TIMESTAMP,
    actual_start_time TIMESTAMP,
    actual_completion_time TIMESTAMP,
    additional_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Indexes and Constraints
```sql
-- Performance indexes
CREATE INDEX idx_work_orders_status ON work_orders(status);
CREATE INDEX idx_work_orders_priority ON work_orders(priority_level);
CREATE INDEX idx_work_orders_dates ON work_orders(datum_isporuke, datum_sastavljanja);
CREATE INDEX idx_operations_work_center ON operations(work_center_id);
CREATE INDEX idx_operations_status ON operations(status);
CREATE INDEX idx_operations_sequence ON operations(work_order_id, operation_sequence);

-- Data constraints
ALTER TABLE work_orders ADD CONSTRAINT chk_priority_level 
    CHECK (priority_level IN (1, 2, 3));
ALTER TABLE work_orders ADD CONSTRAINT chk_status 
    CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled'));
ALTER TABLE operations ADD CONSTRAINT chk_operation_status 
    CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled'));
```

## 🔧 Backend Architecture

### FastAPI Application Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── work_orders.py      # Work order CRUD
│   │   ├── scheduling.py       # Scheduling operations
│   │   └── machines.py         # Work center management
│   ├── database/               # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py       # Database connection
│   │   └── models.py          # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   └── work_order.py      # Request/response models
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   └── scheduling_service.py
│   └── utils/                  # Utilities
│       ├── __init__.py
│       └── date_utils.py
├── alembic/                    # Database migrations
│   ├── env.py
│   ├── versions/
│   └── alembic.ini
├── migrate_legacy_data.py      # Data migration script
└── requirements.txt
```

### API Design Patterns

#### RESTful Endpoints
```python
# Work Orders API
GET    /api/work-orders              # List work orders
POST   /api/work-orders              # Create work order
GET    /api/work-orders/{id}         # Get specific work order
PUT    /api/work-orders/{id}         # Update work order
DELETE /api/work-orders/{id}         # Delete work order
PATCH  /api/work-orders/{id}/status  # Update status only

# Scheduling API
GET    /api/schedule/{work_center}   # Get schedule for work center
POST   /api/schedule/optimize        # Optimize schedule
PUT    /api/schedule/reorder         # Manual reorder operations

# Machines API
GET    /api/machines                 # List all work centers
GET    /api/machines/{id}            # Get specific work center
PUT    /api/machines/{id}/status     # Update work center status
GET    /api/machines/{id}/calendar   # Get work center calendar
```

#### Request/Response Models
```python
# Pydantic schemas for type safety
class WorkOrderCreate(BaseModel):
    product_id: int
    rn: str
    quantity: int = 1
    priority_level: int = 3
    datum_isporuke: Optional[date] = None
    datum_sastavljanja: Optional[date] = None

class WorkOrderResponse(BaseModel):
    id: int
    rn: str
    product_kpl: str
    product_name: str
    quantity: int
    priority_level: int
    datum_isporuke: Optional[date]
    datum_sastavljanja: Optional[date]
    status: str
    created_at: datetime
    updated_at: datetime
```

### Database Layer
```python
# Async SQLAlchemy configuration
engine = create_async_engine(
    "postgresql+asyncpg://postgres:password@192.168.1.25:5432/mes_production",
    echo=True,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency injection
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

## 🎨 Frontend Architecture

### React Application Structure
```
frontend/
├── src/
│   ├── components/             # Reusable components
│   │   ├── Layout/
│   │   │   ├── Layout.tsx      # Main layout component
│   │   │   └── Navigation.tsx  # Navigation sidebar
│   │   └── Common/             # Common UI components
│   ├── pages/                  # Page components
│   │   ├── Dashboard.tsx       # Overview dashboard
│   │   ├── WorkOrders.tsx      # Work order management
│   │   ├── Scheduling.tsx      # Drag-drop scheduling
│   │   └── Machines.tsx        # Work center management
│   ├── hooks/                  # Custom React hooks
│   │   ├── useWorkOrders.ts    # Work order operations
│   │   ├── useMachines.ts      # Machine operations
│   │   └── useScheduling.ts    # Scheduling operations
│   ├── lib/                    # Utilities and API client
│   │   ├── api.ts              # Axios configuration
│   │   └── utils.ts            # Helper functions
│   ├── types/                  # TypeScript type definitions
│   │   └── index.ts
│   ├── App.tsx                 # Main app component
│   ├── main.tsx                # Application entry point
│   └── index.css               # Global styles
├── public/                     # Static assets
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
└── vite.config.ts
```

### State Management Architecture
```typescript
// TanStack Query for server state
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30000,      // 30 seconds
      refetchInterval: 60000, // 1 minute
    },
  },
});

// Custom hooks for data fetching
export const useWorkOrders = (params?: WorkOrderFilters) => {
  return useQuery({
    queryKey: ['work-orders', params],
    queryFn: async () => {
      const response = await workOrdersApi.getAll(params);
      return response.data;
    },
    staleTime: 30000,
    refetchInterval: 60000,
  });
};

// Mutation hooks for updates
export const useUpdateWorkOrder = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ id, data }: { id: string; data: Partial<WorkOrder> }) => {
      const response = await workOrdersApi.update(id, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['work-orders'] });
    },
  });
};
```

### Component Architecture
```typescript
// Page component with hooks
export default function WorkOrders() {
  const { data: workOrdersData, isLoading, error } = useWorkOrders();
  const updateStatusMutation = useUpdateWorkOrderStatus();
  
  const handleStatusChange = async (id: string, status: string) => {
    try {
      await updateStatusMutation.mutateAsync({ id, status });
    } catch (error) {
      console.error('Failed to update status:', error);
    }
  };
  
  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  
  return (
    <div className="p-6">
      <WorkOrderTable 
        data={workOrdersData?.work_orders || []} 
        onStatusChange={handleStatusChange}
      />
    </div>
  );
}
```

## 🔌 API Integration

### HTTP Client Configuration
```typescript
// Axios setup with interceptors
const API_BASE_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for auth
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);
```

### Real-time Updates (Planned)
```typescript
// WebSocket integration for real-time updates
const useWebSocket = (url: string) => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  
  useEffect(() => {
    const ws = new WebSocket(url);
    
    ws.onopen = () => {
      console.log('WebSocket connected');
      setSocket(ws);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      // Handle real-time updates
      queryClient.invalidateQueries({ queryKey: [data.type] });
    };
    
    return () => {
      ws.close();
    };
  }, [url]);
  
  return socket;
};
```

## 🛠️ Development Tools

### MCP Server Integration
```json
{
  "mcpServers": {
    "postgresql": {
      "command": "mcp-server-postgresql",
      "args": ["--database", "mes_production", "--host", "192.168.1.25"]
    },
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["--path", "/project/root"]
    },
    "web-search": {
      "command": "mcp-server-web-search"
    },
    "git": {
      "command": "mcp-server-git"
    },
    "context7": {
      "command": "mcp-server-context7"
    }
  }
}
```

### Build Configuration
```typescript
// Vite configuration
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          tanstack: ['@tanstack/react-query'],
          dnd: ['@dnd-kit/core', '@dnd-kit/sortable'],
        },
      },
    },
  },
});
```

## 🔒 Security Considerations

### Database Security
- Parameterized queries prevent SQL injection
- Connection pooling with proper timeout settings
- Network-level database access control
- Role-based access control (planned)

### API Security
- CORS properly configured for frontend origin
- Request validation with Pydantic schemas
- Rate limiting (planned)
- Authentication middleware (planned)

### Frontend Security
- TypeScript for type safety
- XSS protection with proper data sanitization
- CSP headers (planned)
- Secure token storage (planned)

## 📈 Performance Optimization

### Database Performance
```sql
-- Optimized queries with proper indexing
EXPLAIN ANALYZE SELECT 
    wo.id, wo.rn, p.kpl, p.name, wo.status, wo.priority_level
FROM work_orders wo
JOIN products p ON wo.product_id = p.id
WHERE wo.status = 'pending'
ORDER BY wo.priority_level, wo.datum_isporuke;

-- Query uses index on (status, priority_level, datum_isporuke)
```

### Frontend Performance
```typescript
// Component lazy loading
const Dashboard = lazy(() => import('./pages/Dashboard'));
const WorkOrders = lazy(() => import('./pages/WorkOrders'));
const Scheduling = lazy(() => import('./pages/Scheduling'));

// Memoization for expensive calculations
const expensiveCalculation = useMemo(() => {
  return workOrders.reduce((acc, order) => {
    return acc + order.quantity * order.norma;
  }, 0);
}, [workOrders]);

// Virtual scrolling for large datasets (planned)
import { FixedSizeList as List } from 'react-window';
```

## 🧪 Testing Strategy (Planned)

### Backend Testing
```python
# FastAPI testing with pytest
@pytest.fixture
async def test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def test_create_work_order(test_db, client):
    work_order_data = {
        "product_id": 1,
        "rn": "WO-001",
        "quantity": 10,
        "priority_level": 1
    }
    response = await client.post("/api/work-orders", json=work_order_data)
    assert response.status_code == 201
```

### Frontend Testing
```typescript
// React Testing Library
import { render, screen, fireEvent } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

test('renders work order list', () => {
  const queryClient = new QueryClient();
  render(
    <QueryClientProvider client={queryClient}>
      <WorkOrders />
    </QueryClientProvider>
  );
  
  expect(screen.getByText('Work Orders')).toBeInTheDocument();
});
```

## 🚀 Deployment Architecture (Planned)

### Docker Configuration
```dockerfile
# Backend Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
```

### Infrastructure
```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
      
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: mes_production
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
      
volumes:
  postgres_data:
```

---

*This technical architecture document provides a comprehensive overview of the MES Production Scheduler system design and implementation details.*