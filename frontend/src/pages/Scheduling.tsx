import { useState, useEffect } from 'react';
import { Calendar, Clock, RefreshCw, Loader2, AlertCircle } from 'lucide-react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  type DragEndEvent,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import {
  useSortable,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { useSchedule, useOptimizeSchedule, useReorderSchedule } from '../hooks/useScheduling';

interface ScheduleItem {
  id: string;
  workOrderRn: string;
  productKpl: string;
  productName: string;
  operation: string;
  estimatedTime: number;
  priority: number;
  deliveryDate: string;
  assemblyDate: string;
  position: number;
}

interface SortableItemProps {
  item: ScheduleItem;
}

function SortableItem({ item }: SortableItemProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id: item.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      className="flex items-center p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow cursor-move"
    >
      <div className="flex-1">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-gray-900">{item.workOrderRn}</h3>
            <p className="text-sm text-gray-600">{item.productKpl}</p>
            <p className="text-sm text-gray-500">{item.productName}</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">
                <Clock size={14} className="inline mr-1" />
                {item.estimatedTime} min
              </p>
              <p className="text-sm text-gray-600">
                <Calendar size={14} className="inline mr-1" />
                Due: {new Date(item.deliveryDate).toLocaleDateString()}
              </p>
            </div>
            <div className="text-right">
              <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                item.priority === 1 ? 'bg-red-100 text-red-800' :
                item.priority === 2 ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {item.priority === 1 ? 'High' : item.priority === 2 ? 'Medium' : 'Low'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Scheduling() {
  const [selectedWorkCenter, setSelectedWorkCenter] = useState('SAV100');
  const [optimizeBy, setOptimizeBy] = useState<'datum_isporuke' | 'datum_sastavljanja' | 'priority'>('datum_isporuke');

  const { data: scheduleData, isLoading, error } = useSchedule(selectedWorkCenter);
  const optimizeMutation = useOptimizeSchedule();
  const reorderMutation = useReorderSchedule();

  // Convert schedule data to sortable items
  const scheduleItems: ScheduleItem[] = (scheduleData?.operations || []).map((op: any) => ({
    id: op.id.toString(),
    workOrderRn: op.work_order.rn,
    productKpl: op.work_order.product_kpl,
    productName: op.work_order.product_name,
    operation: op.naziv,
    estimatedTime: op.norma || 0,
    priority: op.work_order.priority_level,
    deliveryDate: op.work_order.datum_isporuke,
    assemblyDate: op.work_order.datum_sastavljanja,
    position: op.position || 0,
  }));

  const [items, setItems] = useState<ScheduleItem[]>(scheduleItems);

  // Update items when schedule data changes
  useEffect(() => {
    setItems(scheduleItems);
  }, [scheduleData]);

  const workCenters = ['SAV100', 'G1000'];

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;

    if (active.id !== over?.id) {
      const oldIndex = items.findIndex(item => item.id === active.id);
      const newIndex = items.findIndex(item => item.id === over?.id);

      const newItems = arrayMove(items, oldIndex, newIndex);
      setItems(newItems);

      // Send reorder request to API
      try {
        await reorderMutation.mutateAsync({
          workCenter: selectedWorkCenter,
          newOrder: newItems.map(item => item.id),
        });
      } catch (error) {
        console.error('Error reordering schedule:', error);
        // Revert changes on error
        setItems(items);
        alert('Failed to reorder schedule. Please try again.');
      }
    }
  };

  const handleOptimize = async () => {
    try {
      await optimizeMutation.mutateAsync({
        criteria: optimizeBy,
        workCenter: selectedWorkCenter,
      });
    } catch (error) {
      console.error('Error optimizing schedule:', error);
      alert('Failed to optimize schedule. Please try again.');
    }
  };

  if (isLoading) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-64">
          <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
          <span className="ml-2 text-gray-600">Loading schedule...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="flex items-center justify-center h-64">
          <AlertCircle className="h-8 w-8 text-red-600" />
          <span className="ml-2 text-red-600">Error loading schedule. Please try again.</span>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Production Scheduling</h1>
        <p className="text-gray-600">Optimize and manage production schedules</p>
      </div>

      {/* Controls */}
      <div className="mb-6 flex flex-col sm:flex-row gap-4">
        <div className="flex gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Work Center
            </label>
            <select
              value={selectedWorkCenter}
              onChange={(e) => setSelectedWorkCenter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {workCenters.map((center) => (
                <option key={center} value={center}>
                  {center}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Optimize By
            </label>
            <select
              value={optimizeBy}
              onChange={(e) => setOptimizeBy(e.target.value as 'datum_isporuke' | 'datum_sastavljanja' | 'priority')}
              className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="datum_isporuke">Delivery Date</option>
              <option value="datum_sastavljanja">Assembly Date</option>
              <option value="priority">Priority</option>
            </select>
          </div>
        </div>
        <div className="flex items-end">
          <button
            onClick={handleOptimize}
            disabled={optimizeMutation.isPending}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {optimizeMutation.isPending ? (
              <Loader2 className="h-4 w-4 animate-spin mr-2" />
            ) : (
              <RefreshCw size={20} className="mr-2" />
            )}
            Optimize Schedule
          </button>
        </div>
      </div>

      {/* Schedule */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">
            Schedule for {selectedWorkCenter}
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            Drag and drop items to reorder the schedule
          </p>
        </div>
        <div className="p-6">
          {items.length > 0 ? (
            <DndContext
              sensors={sensors}
              collisionDetection={closestCenter}
              onDragEnd={handleDragEnd}
            >
              <SortableContext items={items.map(item => item.id)} strategy={verticalListSortingStrategy}>
                <div className="space-y-4">
                  {items.map((item) => (
                    <SortableItem key={item.id} item={item} />
                  ))}
                </div>
              </SortableContext>
            </DndContext>
          ) : (
            <div className="text-center py-8 text-gray-500">
              No operations scheduled for this work center
            </div>
          )}
        </div>
      </div>

      {reorderMutation.isPending && (
        <div className="fixed top-4 right-4 bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg">
          Saving order...
        </div>
      )}
    </div>
  );
}