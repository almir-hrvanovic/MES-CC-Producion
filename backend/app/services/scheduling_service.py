"""
Scheduling service for optimization algorithms
"""
from typing import List, Tuple, Any
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models import Operation, WorkOrder


class SchedulingService:
    """Service for scheduling operations and optimization"""
    
    async def optimize_by_criteria(
        self, 
        operations_data: List[Tuple[Operation, str]], 
        criteria: str
    ) -> List[Tuple[Operation, str]]:
        """
        Optimize operations based on specified criteria
        
        Args:
            operations_data: List of (Operation, work_order_rn) tuples
            criteria: Optimization criteria (datum_isporuke, datum_sastavljanja, etc.)
        
        Returns:
            Sorted list of operations
        """
        
        if criteria == "datum_isporuke":
            return await self._sort_by_delivery_date(operations_data)
        elif criteria == "datum_sastavljanja":
            return await self._sort_by_assembly_date(operations_data)
        elif criteria == "datum_treci":
            return await self._sort_by_third_date(operations_data)
        elif criteria == "hitno":
            return await self._sort_by_priority(operations_data)
        else:
            # Default: sort by delivery date
            return await self._sort_by_delivery_date(operations_data)
    
    async def _sort_by_delivery_date(
        self, 
        operations_data: List[Tuple[Operation, str]]
    ) -> List[Tuple[Operation, str]]:
        """Sort operations by delivery date (datum_isporuke)"""
        
        # We need to get work order data to access dates
        # For now, we'll sort by operation ID as placeholder
        # TODO: Join with WorkOrder to get actual dates
        
        def sort_key(item):
            operation, rn = item
            # Placeholder: sort by operation ID
            # In real implementation, sort by work_order.datum_isporuke
            return operation.id
        
        return sorted(operations_data, key=sort_key)
    
    async def _sort_by_assembly_date(
        self, 
        operations_data: List[Tuple[Operation, str]]
    ) -> List[Tuple[Operation, str]]:
        """Sort operations by assembly date (datum_sastavljanja)"""
        
        def sort_key(item):
            operation, rn = item
            # Placeholder: sort by operation sequence
            return operation.operation_sequence
        
        return sorted(operations_data, key=sort_key)
    
    async def _sort_by_third_date(
        self, 
        operations_data: List[Tuple[Operation, str]]
    ) -> List[Tuple[Operation, str]]:
        """Sort operations by third date (datum_treci)"""
        
        def sort_key(item):
            operation, rn = item
            # Placeholder: sort by naziv alphabetically
            return operation.naziv
        
        return sorted(operations_data, key=sort_key)
    
    async def _sort_by_priority(
        self, 
        operations_data: List[Tuple[Operation, str]]
    ) -> List[Tuple[Operation, str]]:
        """Sort operations by priority (HITNO field)"""
        
        def sort_key(item):
            operation, rn = item
            # Placeholder: sort by operation ID descending (urgent first)
            return -operation.id
        
        return sorted(operations_data, key=sort_key)
    
    async def calculate_completion_times(
        self, 
        operations: List[Operation],
        start_time: datetime = None
    ) -> List[dict]:
        """
        Calculate estimated completion times for operations
        
        Args:
            operations: List of operations in sequence
            start_time: Starting time (defaults to now)
        
        Returns:
            List of dictionaries with timing information
        """
        
        if start_time is None:
            start_time = datetime.now()
        
        results = []
        current_time = start_time
        
        for operation in operations:
            # Calculate duration from norma (standard time in hours)
            duration_hours = float(operation.norma) if operation.norma else 1.0
            duration = timedelta(hours=duration_hours)
            
            end_time = current_time + duration
            
            results.append({
                "operation_id": operation.id,
                "estimated_start": current_time,
                "estimated_end": end_time,
                "duration_hours": duration_hours
            })
            
            # Next operation starts when current one ends
            current_time = end_time
        
        return results
    
    async def detect_conflicts(
        self, 
        operations: List[Operation]
    ) -> List[dict]:
        """
        Detect scheduling conflicts
        
        Args:
            operations: List of operations to check
        
        Returns:
            List of conflict descriptions
        """
        
        conflicts = []
        
        # Check for capacity conflicts (placeholder)
        total_hours = sum(float(op.norma) if op.norma else 0 for op in operations)
        if total_hours > 40:  # More than 40 hours of work
            conflicts.append({
                "type": "capacity_exceeded",
                "description": f"Total work time ({total_hours:.1f}h) exceeds weekly capacity",
                "severity": "warning"
            })
        
        # Check for missing dependencies (placeholder)
        for operation in operations:
            if operation.dependencies:
                conflicts.append({
                    "type": "dependency_check",
                    "description": f"Operation {operation.id} has dependencies that need verification",
                    "severity": "info"
                })
        
        return conflicts