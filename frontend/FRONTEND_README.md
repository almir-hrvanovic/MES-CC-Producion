# MES Production Scheduler Frontend

React TypeScript frontend for the Manufacturing Execution System (MES) Production Scheduler.

## Features

- **Dashboard**: Overview of production status with key metrics
- **Work Orders**: Manage and track production work orders
- **Scheduling**: Optimize and reorder production schedules
- **Machines**: Monitor work center status and utilization

## Technology Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **React Router** for navigation
- **TanStack Query** for API state management
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **Axios** for API communication

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout/
│   │       └── Layout.tsx          # Main layout with navigation
│   ├── pages/
│   │   ├── Dashboard.tsx           # Dashboard overview
│   │   ├── WorkOrders.tsx          # Work orders management
│   │   ├── Scheduling.tsx          # Production scheduling
│   │   └── Machines.tsx            # Work center monitoring
│   ├── lib/
│   │   └── api.ts                  # API client and types
│   ├── App.tsx                     # Main app component
│   └── index.css                   # Tailwind CSS imports
├── tailwind.config.js              # Tailwind configuration
├── postcss.config.js               # PostCSS configuration
└── package.json                    # Dependencies
```

## Getting Started

### Prerequisites

- Node.js (v20.19.0 or higher)
- npm or yarn

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

## API Integration

The frontend communicates with the FastAPI backend running at `http://localhost:8000/api`. 

Key API endpoints:
- `/work-orders` - Work order management
- `/schedule` - Production scheduling
- `/machines` - Work center monitoring

## Components

### Layout
- Responsive sidebar navigation
- Mobile-friendly hamburger menu
- Active route highlighting

### Dashboard
- Key metrics cards
- Recent work orders
- Work center status overview

### Work Orders
- Searchable and filterable table
- Status and priority indicators
- CRUD operations (planned)

### Scheduling
- Work center selection
- Optimization by delivery date, assembly date, or priority
- Drag-and-drop reordering (planned)

### Machines
- Work center status monitoring
- Utilization rate visualization
- Capacity and performance metrics

## Development Notes

- Uses descriptive variable names as per project standards
- Connects to network database at `192.168.1.25:5432`
- Mock data is used for development until API integration is complete
- Built with responsive design for desktop and mobile

## Next Steps

1. Implement drag-and-drop scheduling functionality
2. Add real-time data updates
3. Integrate with actual backend API
4. Add user authentication
5. Implement data validation and error handling
6. Add unit tests