import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { workOrdersApi, type WorkOrder } from '../lib/api';

export const useWorkOrders = (params?: { work_center?: string; status?: string; urgent_only?: boolean }) => {
  return useQuery({
    queryKey: ['work-orders', params],
    queryFn: async () => {
      const response = await workOrdersApi.getAll(params);
      return response.data;
    },
    staleTime: 30000, // 30 seconds
    refetchInterval: 60000, // 1 minute
  });
};

export const useWorkOrder = (id: string) => {
  return useQuery({
    queryKey: ['work-order', id],
    queryFn: async () => {
      const response = await workOrdersApi.getById(id);
      return response.data;
    },
    enabled: !!id,
  });
};

export const useCreateWorkOrder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (workOrderData: Partial<WorkOrder>) => {
      const response = await workOrdersApi.create(workOrderData);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['work-orders'] });
    },
  });
};

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

export const useUpdateWorkOrderStatus = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ id, status }: { id: string; status: string }) => {
      const response = await workOrdersApi.updateStatus(id, status);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['work-orders'] });
    },
  });
};

export const useDeleteWorkOrder = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (id: string) => {
      const response = await workOrdersApi.delete(id);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['work-orders'] });
    },
  });
};