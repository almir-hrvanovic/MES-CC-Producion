import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import Login from './pages/Login';
import MainDashboard from './pages/MainDashboard';
import Dashboard from './pages/Dashboard';
import WorkOrders from './pages/WorkOrders';
import Scheduling from './pages/Scheduling';
import Machines from './pages/Machines';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<Login />} />
          
          {/* Protected routes */}
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <MainDashboard />
            </ProtectedRoute>
          } />
          
          <Route path="/" element={
            <ProtectedRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/work-orders" element={
            <ProtectedRoute>
              <Layout>
                <WorkOrders />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/scheduling" element={
            <ProtectedRoute>
              <Layout>
                <Scheduling />
              </Layout>
            </ProtectedRoute>
          } />
          
          <Route path="/machines" element={
            <ProtectedRoute>
              <Layout>
                <Machines />
              </Layout>
            </ProtectedRoute>
          } />
          
          {/* Redirect to login if no route matches */}
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;