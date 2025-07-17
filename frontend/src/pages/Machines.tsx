import { Activity, Clock, AlertTriangle, CheckCircle, Loader2, AlertCircle } from 'lucide-react';
import { useMachines, useUpdateMachineStatus } from '../hooks/useMachines';
import { type WorkCenter } from '../lib/api';

export default function Machines() {
  const { data: machinesData, isLoading, error } = useMachines();
  const updateStatusMutation = useUpdateMachineStatus();

  const machines = machinesData || [];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'idle':
        return 'bg-yellow-100 text-yellow-800';
      case 'maintenance':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'idle':
        return <Clock className="h-5 w-5 text-yellow-600" />;
      case 'maintenance':
        return <AlertTriangle className="h-5 w-5 text-red-600" />;
      default:
        return <Activity className="h-5 w-5 text-gray-600" />;
    }
  };

  const getUtilizationColor = (rate: number) => {
    if (rate >= 80) return 'bg-green-500';
    if (rate >= 60) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getUtilizationRate = (_machine: WorkCenter) => {
    // Calculate utilization rate based on machine data
    // For now, return a mock value since we don't have real utilization data
    return Math.floor(Math.random() * 40) + 60; // Random between 60-100%
  };

  const handleStatusChange = async (workCenterCode: string, newStatus: string) => {
    try {
      await updateStatusMutation.mutateAsync({ workCenterCode, status: newStatus });
    } catch (error) {
      console.error('Error updating machine status:', error);
      alert('Failed to update machine status. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-64">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          <span className="ml-2 text-gray-600">Loading work centers...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-64">
          <AlertCircle className="h-8 w-8 text-red-600" />
          <span className="ml-2 text-red-600">Error loading work centers. Please try again.</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Work Centers</h1>
        <p className="text-gray-600">Monitor and manage work center status</p>
      </div>

      {/* Work Centers Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {machines.map((machine: WorkCenter) => {
          const utilizationRate = getUtilizationRate(machine);
          const operationsCount = Math.floor(Math.random() * 20) + 5; // Mock operations count
          const avgSetupTime = machine.setup_time_minutes;
          const machineStatus = machine.is_active ? 'active' : 'idle';

          return (
            <div key={machine.id} className="bg-white rounded-lg shadow">
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {machine.code} - {machine.name}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {machine.description || 'No description'}
                    </p>
                  </div>
                  <div className="flex items-center">
                    {getStatusIcon(machineStatus)}
                    <select
                      value={machineStatus}
                      onChange={(e) => handleStatusChange(machine.code, e.target.value)}
                      className={`ml-2 text-xs font-semibold rounded-full px-2 py-1 border-0 ${getStatusColor(machineStatus)}`}
                      disabled={updateStatusMutation.isPending}
                    >
                      <option value="active">Active</option>
                      <option value="idle">Idle</option>
                      <option value="maintenance">Maintenance</option>
                    </select>
                  </div>
                </div>

                {/* Utilization Rate */}
                <div className="mb-4">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">Utilization Rate</span>
                    <span className="font-medium">{utilizationRate}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${getUtilizationColor(utilizationRate)}`}
                      style={{ width: `${utilizationRate}%` }}
                    ></div>
                  </div>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <Activity className="h-5 w-5 text-blue-600 mr-2" />
                      <div>
                        <p className="text-sm text-gray-600">Operations</p>
                        <p className="text-lg font-semibold">{operationsCount}</p>
                      </div>
                    </div>
                  </div>
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center">
                      <Clock className="h-5 w-5 text-yellow-600 mr-2" />
                      <div>
                        <p className="text-sm text-gray-600">Setup Time</p>
                        <p className="text-lg font-semibold">{avgSetupTime}min</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Capacity */}
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-blue-700">Daily Capacity</span>
                    <span className="font-semibold text-blue-900">{machine.capacity_hours_per_day} hours</span>
                  </div>
                  {machine.cost_per_hour && (
                    <div className="flex items-center justify-between mt-1">
                      <span className="text-sm text-blue-700">Cost per Hour</span>
                      <span className="font-semibold text-blue-900">${machine.cost_per_hour}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Summary Stats */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <CheckCircle className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Centers</p>
              <p className="text-2xl font-bold text-gray-900">
                {machines.filter((m: WorkCenter) => m.is_active).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Activity className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Centers</p>
              <p className="text-2xl font-bold text-gray-900">
                {machines.length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-2 bg-yellow-100 rounded-lg">
              <Clock className="h-6 w-6 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Avg Capacity</p>
              <p className="text-2xl font-bold text-gray-900">
                {machines.length > 0 
                  ? Math.round(machines.reduce((sum: number, m: WorkCenter) => sum + m.capacity_hours_per_day, 0) / machines.length)
                  : 0}h
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}