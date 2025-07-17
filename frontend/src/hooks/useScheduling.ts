import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { schedulingApi } from '../lib/api';

export const useSchedule = (workCenter: string) => {
  return useQuery({
    queryKey: ['schedule', workCenter],
    queryFn: async () => {
      const response = await schedulingApi.getSchedule(workCenter);
      return response.data;
    },
    enabled: !!workCenter,
    staleTime: 30000, // 30 seconds
    refetchInterval: 60000, // 1 minute
  });
};

export const useOptimizeSchedule = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ 
      criteria, 
      workCenter 
    }: { 
      criteria: 'datum_isporuke' | 'datum_sastavljanja' | 'priority'; 
      workCenter?: string;
    }) => {
      const response = await schedulingApi.optimize(criteria, workCenter);
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['schedule', variables.workCenter] });
    },
  });
};

export const useReorderSchedule = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ 
      workCenter, 
      newOrder 
    }: { 
      workCenter: string; 
      newOrder: string[];
    }) => {
      const response = await schedulingApi.reorder(workCenter, newOrder);
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['schedule', variables.workCenter] });
    },
  });
};