import { Activity, TrendingUp, Clock, AlertCircle, Loader2 } from 'lucide-react';
import { useWorkOrders } from '../hooks/useWorkOrders';
import { useMachines } from '../hooks/useMachines';

export default function Dashboard() {
  const { data: workOrdersData, isLoading: workOrdersLoading } = useWorkOrders();
  const { data: machinesData, isLoading: machinesLoading } = useMachines();

  const workOrders = workOrdersData?.work_orders || [];
  const machines = machinesData || [];

  // Calculate statistics
  const activeWorkOrders = workOrders.filter(wo => wo.status === 'in_progress').length;
  const completedToday = workOrders.filter(wo => {
    const today = new Date().toISOString().split('T')[0];
    return wo.status === 'completed' && wo.updated_at.startsWith(today);
  }).length;
  const pendingWorkOrders = workOrders.filter(wo => wo.status === 'pending').length;
  const urgentWorkOrders = workOrders.filter(wo => wo.priority_level === 1).length;

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const recentWorkOrders = workOrders
    .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
    .slice(0, 5);

  if (workOrdersLoading || machinesLoading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-64">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          <span className="ml-2 text-gray-600">Loading dashboard...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Manufacturing Execution System Overview</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Activity className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Work Orders</p>
              <p className="text-2xl font-bold text-gray-900">{activeWorkOrders}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Completed Today</p>
              <p className="text-2xl font-bold text-gray-900">{completedToday}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Clock className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Pending</p>
              <p className="text-2xl font-bold text-gray-900">{pendingWorkOrders}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-red-100 rounded-lg">
              <AlertCircle className="h-6 w-6 text-red-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Urgent</p>
              <p className="text-2xl font-bold text-gray-900">{urgentWorkOrders}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Recent Work Orders</h2>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {recentWorkOrders.length > 0 ? (
                recentWorkOrders.map((order) => (
                  <div key={order.id} className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900">{order.rn}</p>
                      <p className="text-sm text-gray-600">{order.product_kpl}</p>
                      <p className="text-xs text-gray-500">{order.product_name}</p>
                    </div>
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(order.status)}`}>
                      {order.status.replace('_', ' ')}
                    </span>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-center py-4">No work orders found</p>
              )}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Work Center Status</h2>
          </div>
          <div className="p-6">
            <div className="space-y-4">
              {machines.length > 0 ? (
                machines.map((machine) => (
                  <div key={machine.id} className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-gray-900">{machine.code} - {machine.name}</p>
                      <p className="text-sm text-gray-600">
                        Capacity: {machine.capacity_hours_per_day}h/day
                      </p>
                      <p className="text-xs text-gray-500">
                        Setup: {machine.setup_time_minutes}min
                      </p>
                    </div>
                    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                      machine.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {machine.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-center py-4">No work centers found</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}