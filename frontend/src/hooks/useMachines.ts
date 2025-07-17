import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { machinesApi } from '../lib/api';

export const useMachines = () => {
  return useQuery({
    queryKey: ['machines'],
    queryFn: async () => {
      const response = await machinesApi.getAll();
      return response.data;
    },
    staleTime: 60000, // 1 minute
    refetchInterval: 120000, // 2 minutes
  });
};

export const useMachine = (workCenterCode: string) => {
  return useQuery({
    queryKey: ['machine', workCenterCode],
    queryFn: async () => {
      const response = await machinesApi.getById(workCenterCode);
      return response.data;
    },
    enabled: !!workCenterCode,
  });
};

export const useUpdateMachineStatus = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ workCenterCode, status }: { workCenterCode: string; status: string }) => {
      const response = await machinesApi.updateStatus(workCenterCode, status);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['machines'] });
    },
  });
};

export const useMachineCalendar = (workCenterCode: string) => {
  return useQuery({
    queryKey: ['machine-calendar', workCenterCode],
    queryFn: async () => {
      const response = await machinesApi.getCalendar(workCenterCode);
      return response.data;
    },
    enabled: !!workCenterCode,
  });
};