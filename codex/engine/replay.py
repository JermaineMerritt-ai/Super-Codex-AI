"""
Codex Replay System
Query replay functionality for debugging, testing, and reproducibility.
Supports capturing query state, replaying queries, and analyzing differences.
"""

import os
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timezone, timedelta
import logging
import json
import hashlib
import pickle
from dataclasses import dataclass, asdict
from enum import Enum
import copy

logger = logging.getLogger(__name__)


class ReplayStatus(Enum):
    """Status of replay operations"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ComparisonResult(Enum):
    """Result of replay comparison"""
    IDENTICAL = "identical"
    SIMILAR = "similar"
    DIFFERENT = "different"
    ERROR = "error"


@dataclass
class QuerySnapshot:
    """Snapshot of query state for replay"""
    snapshot_id: str
    query_id: str
    query_text: str
    timestamp: str
    context: Dict[str, Any]
    vector_state: Optional[Dict[str, Any]] = None
    rag_config: Optional[Dict[str, Any]] = None
    system_state: Optional[Dict[str, Any]] = None
    result_summary: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QuerySnapshot":
        """Create from dictionary"""
        return cls(**data)


@dataclass
class ReplayResult:
    """Result of a replay operation"""
    replay_id: str
    original_snapshot: QuerySnapshot
    replay_timestamp: str
    status: ReplayStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    performance_data: Optional[Dict[str, Any]] = None
    comparison: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['status'] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReplayResult":
        """Create from dictionary"""
        data['status'] = ReplayStatus(data['status'])
        data['original_snapshot'] = QuerySnapshot.from_dict(data['original_snapshot'])
        return cls(**data)


class QueryCapturer:
    """Capture query state for replay"""
    
    def __init__(self, config):
        self.config = config
        self.enabled = config.replay_capture_enabled
        self.snapshots_path = config.replay_snapshots_path
        self.max_snapshots = config.replay_max_snapshots
        
        # Ensure snapshots directory exists
        if self.enabled:
            self.snapshots_path.mkdir(parents=True, exist_ok=True)
    
    async def capture_query_state(self, query_id: str, query_text: str, 
                                 context: Dict[str, Any],
                                 rag_system = None) -> Optional[str]:
        """Capture current state for replay"""
        if not self.enabled:
            return None
        
        try:
            # Generate snapshot ID
            snapshot_id = self._generate_snapshot_id(query_id)
            
            # Capture vector store state
            vector_state = await self._capture_vector_state(rag_system) if rag_system else None
            
            # Capture RAG configuration
            rag_config = self._capture_rag_config(rag_system) if rag_system else None
            
            # Capture system state
            system_state = self._capture_system_state()
            
            # Create snapshot
            snapshot = QuerySnapshot(
                snapshot_id=snapshot_id,
                query_id=query_id,
                query_text=query_text,
                timestamp=datetime.now(timezone.utc).isoformat(),
                context=context,
                vector_state=vector_state,
                rag_config=rag_config,
                system_state=system_state
            )
            
            # Save snapshot
            await self._save_snapshot(snapshot)
            
            # Clean up old snapshots
            await self._cleanup_old_snapshots()
            
            logger.debug(f"Captured query snapshot {snapshot_id} for query {query_id}")
            return snapshot_id
            
        except Exception as e:
            logger.error(f"Failed to capture query state for {query_id}: {e}")
            return None
    
    async def update_snapshot_result(self, snapshot_id: str, result: Dict[str, Any]):
        """Update snapshot with query result"""
        if not self.enabled:
            return
        
        try:
            snapshot = await self._load_snapshot(snapshot_id)
            if snapshot:
                # Create result summary (not full result to save space)
                snapshot.result_summary = {
                    "success": result.get("success", False),
                    "scroll_type": result.get("scroll_type"),
                    "content_length": len(result.get("content", "")),
                    "source_count": len(result.get("sources", [])),
                    "processing_time": result.get("processing_time"),
                    "confidence_score": result.get("confidence_score")
                }
                
                await self._save_snapshot(snapshot)
                logger.debug(f"Updated snapshot {snapshot_id} with result summary")
                
        except Exception as e:
            logger.error(f"Failed to update snapshot {snapshot_id} with result: {e}")
    
    async def get_snapshot(self, snapshot_id: str) -> Optional[QuerySnapshot]:
        """Get snapshot by ID"""
        return await self._load_snapshot(snapshot_id)
    
    async def list_snapshots(self, limit: int = 50, 
                           query_filter: Optional[str] = None) -> List[QuerySnapshot]:
        """List available snapshots"""
        if not self.enabled:
            return []
        
        try:
            snapshots = []
            
            # Load all snapshot files
            for snapshot_file in self.snapshots_path.glob("*.json"):
                try:
                    snapshot = await self._load_snapshot_from_file(snapshot_file)
                    
                    # Apply filter if specified
                    if query_filter:
                        if query_filter.lower() not in snapshot.query_text.lower():
                            continue
                    
                    snapshots.append(snapshot)
                    
                except Exception as e:
                    logger.warning(f"Failed to load snapshot from {snapshot_file}: {e}")
            
            # Sort by timestamp (newest first)
            snapshots.sort(key=lambda s: s.timestamp, reverse=True)
            
            return snapshots[:limit]
            
        except Exception as e:
            logger.error(f"Failed to list snapshots: {e}")
            return []
    
    def _generate_snapshot_id(self, query_id: str) -> str:
        """Generate unique snapshot ID"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        query_hash = hashlib.md5(query_id.encode()).hexdigest()[:8]
        return f"snap_{timestamp}_{query_hash}"
    
    async def _capture_vector_state(self, rag_system) -> Optional[Dict[str, Any]]:
        """Capture relevant vector store state"""
        try:
            if hasattr(rag_system, 'vector_store') and rag_system.vector_store:
                return {
                    "total_documents": len(rag_system.vector_store.documents),
                    "vector_dimension": len(rag_system.vector_store.embeddings[0]) if rag_system.vector_store.embeddings else 0,
                    "last_update": getattr(rag_system.vector_store, 'last_update', None)
                }
        except Exception as e:
            logger.warning(f"Failed to capture vector state: {e}")
        return None
    
    def _capture_rag_config(self, rag_system) -> Optional[Dict[str, Any]]:
        """Capture RAG system configuration"""
        try:
            if hasattr(rag_system, 'config'):
                return {
                    "chunk_size": getattr(rag_system.config, 'chunk_size', None),
                    "chunk_overlap": getattr(rag_system.config, 'chunk_overlap', None),
                    "similarity_threshold": getattr(rag_system.config, 'similarity_threshold', None),
                    "max_results": getattr(rag_system.config, 'max_search_results', None)
                }
        except Exception as e:
            logger.warning(f"Failed to capture RAG config: {e}")
        return None
    
    def _capture_system_state(self) -> Dict[str, Any]:
        """Capture relevant system state"""
        return {
            "python_version": f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": os.environ.get("ENVIRONMENT", "unknown")
        }
    
    async def _save_snapshot(self, snapshot: QuerySnapshot):
        """Save snapshot to disk"""
        snapshot_file = self.snapshots_path / f"{snapshot.snapshot_id}.json"
        
        with open(snapshot_file, 'w') as f:
            json.dump(snapshot.to_dict(), f, indent=2)
    
    async def _load_snapshot(self, snapshot_id: str) -> Optional[QuerySnapshot]:
        """Load snapshot from disk"""
        snapshot_file = self.snapshots_path / f"{snapshot_id}.json"
        return await self._load_snapshot_from_file(snapshot_file)
    
    async def _load_snapshot_from_file(self, snapshot_file: Path) -> Optional[QuerySnapshot]:
        """Load snapshot from file"""
        if not snapshot_file.exists():
            return None
        
        try:
            with open(snapshot_file, 'r') as f:
                data = json.load(f)
            return QuerySnapshot.from_dict(data)
        except Exception as e:
            logger.warning(f"Failed to load snapshot from {snapshot_file}: {e}")
            return None
    
    async def _cleanup_old_snapshots(self):
        """Remove old snapshots beyond max limit"""
        try:
            snapshot_files = list(self.snapshots_path.glob("*.json"))
            
            if len(snapshot_files) <= self.max_snapshots:
                return
            
            # Sort by modification time (oldest first)
            snapshot_files.sort(key=lambda f: f.stat().st_mtime)
            
            # Remove oldest files
            files_to_remove = snapshot_files[:-self.max_snapshots]
            
            for file_path in files_to_remove:
                try:
                    file_path.unlink()
                    logger.debug(f"Removed old snapshot {file_path.name}")
                except Exception as e:
                    logger.warning(f"Failed to remove old snapshot {file_path}: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to cleanup old snapshots: {e}")


class QueryReplayer:
    """Replay queries from snapshots"""
    
    def __init__(self, config, rag_system):
        self.config = config
        self.rag_system = rag_system
        self.capturer = QueryCapturer(config)
        self.replay_results: Dict[str, ReplayResult] = {}
    
    async def replay_query(self, snapshot_id: str, 
                          compare_with_original: bool = True) -> ReplayResult:
        """Replay a query from snapshot"""
        try:
            # Load snapshot
            snapshot = await self.capturer.get_snapshot(snapshot_id)
            if not snapshot:
                raise ValueError(f"Snapshot {snapshot_id} not found")
            
            # Generate replay ID
            replay_id = self._generate_replay_id(snapshot_id)
            
            # Create initial result
            replay_result = ReplayResult(
                replay_id=replay_id,
                original_snapshot=snapshot,
                replay_timestamp=datetime.now(timezone.utc).isoformat(),
                status=ReplayStatus.PENDING
            )
            
            self.replay_results[replay_id] = replay_result
            
            # Start replay
            replay_result.status = ReplayStatus.IN_PROGRESS
            
            logger.info(f"Starting replay {replay_id} for snapshot {snapshot_id}")
            
            # Capture performance data
            start_time = datetime.now(timezone.utc)
            
            try:
                # Execute query with captured context
                result = await self.rag_system.query(
                    query=snapshot.query_text,
                    context=snapshot.context
                )
                
                end_time = datetime.now(timezone.utc)
                
                # Record performance
                replay_result.performance_data = {
                    "execution_time": (end_time - start_time).total_seconds(),
                    "timestamp": end_time.isoformat()
                }
                
                replay_result.result = result
                replay_result.status = ReplayStatus.COMPLETED
                
                # Compare with original if requested
                if compare_with_original and snapshot.result_summary:
                    replay_result.comparison = await self._compare_results(
                        snapshot.result_summary, 
                        result
                    )
                
                logger.info(f"Replay {replay_id} completed successfully")
                
            except Exception as e:
                replay_result.status = ReplayStatus.FAILED
                replay_result.error = str(e)
                logger.error(f"Replay {replay_id} failed: {e}")
            
            return replay_result
            
        except Exception as e:
            logger.error(f"Failed to setup replay for snapshot {snapshot_id}: {e}")
            raise
    
    async def replay_batch(self, snapshot_ids: List[str], 
                          max_concurrent: int = 3) -> List[ReplayResult]:
        """Replay multiple queries in batch"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def bounded_replay(snapshot_id: str) -> ReplayResult:
            async with semaphore:
                return await self.replay_query(snapshot_id)
        
        tasks = [bounded_replay(sid) for sid in snapshot_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions in results
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch replay failed for {snapshot_ids[i]}: {result}")
                # Create error result
                error_result = ReplayResult(
                    replay_id=f"error_{i}",
                    original_snapshot=None,
                    replay_timestamp=datetime.now(timezone.utc).isoformat(),
                    status=ReplayStatus.FAILED,
                    error=str(result)
                )
                final_results.append(error_result)
            else:
                final_results.append(result)
        
        return final_results
    
    async def get_replay_result(self, replay_id: str) -> Optional[ReplayResult]:
        """Get replay result by ID"""
        return self.replay_results.get(replay_id)
    
    async def list_replay_results(self, limit: int = 50) -> List[ReplayResult]:
        """List recent replay results"""
        results = list(self.replay_results.values())
        results.sort(key=lambda r: r.replay_timestamp, reverse=True)
        return results[:limit]
    
    async def analyze_replay_patterns(self, days: int = 7) -> Dict[str, Any]:
        """Analyze replay patterns and results"""
        try:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            
            # Filter recent results
            recent_results = [
                r for r in self.replay_results.values()
                if datetime.fromisoformat(r.replay_timestamp.replace('Z', '+00:00')) >= cutoff_date
            ]
            
            if not recent_results:
                return {"message": "No recent replay results to analyze"}
            
            # Analyze patterns
            total_replays = len(recent_results)
            successful_replays = len([r for r in recent_results if r.status == ReplayStatus.COMPLETED])
            failed_replays = len([r for r in recent_results if r.status == ReplayStatus.FAILED])
            
            # Performance analysis
            execution_times = [
                r.performance_data.get("execution_time", 0) 
                for r in recent_results 
                if r.performance_data
            ]
            
            avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
            
            # Comparison analysis
            comparisons = [r.comparison for r in recent_results if r.comparison]
            
            comparison_results = {
                ComparisonResult.IDENTICAL.value: 0,
                ComparisonResult.SIMILAR.value: 0,
                ComparisonResult.DIFFERENT.value: 0,
                ComparisonResult.ERROR.value: 0
            }
            
            for comp in comparisons:
                result_type = comp.get("overall_result", ComparisonResult.ERROR.value)
                comparison_results[result_type] += 1
            
            # Error analysis
            error_patterns = {}
            for result in recent_results:
                if result.error:
                    error_type = type(result.error).__name__ if hasattr(result.error, '__name__') else "Unknown"
                    error_patterns[error_type] = error_patterns.get(error_type, 0) + 1
            
            return {
                "analysis_period_days": days,
                "total_replays": total_replays,
                "success_rate": successful_replays / total_replays if total_replays > 0 else 0,
                "failure_rate": failed_replays / total_replays if total_replays > 0 else 0,
                "performance": {
                    "average_execution_time": avg_execution_time,
                    "min_execution_time": min(execution_times) if execution_times else 0,
                    "max_execution_time": max(execution_times) if execution_times else 0
                },
                "comparison_results": comparison_results,
                "error_patterns": error_patterns,
                "recommendations": self._get_analysis_recommendations(
                    successful_replays / total_replays if total_replays > 0 else 1,
                    comparison_results,
                    error_patterns
                )
            }
            
        except Exception as e:
            logger.error(f"Failed to analyze replay patterns: {e}")
            return {"error": str(e)}
    
    async def _compare_results(self, original_summary: Dict[str, Any], 
                              replay_result: Dict[str, Any]) -> Dict[str, Any]:
        """Compare original and replay results"""
        try:
            comparison = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "original_summary": original_summary,
                "replay_summary": {
                    "success": replay_result.get("success", False),
                    "scroll_type": replay_result.get("scroll_type"),
                    "content_length": len(replay_result.get("content", "")),
                    "source_count": len(replay_result.get("sources", [])),
                    "processing_time": replay_result.get("processing_time"),
                    "confidence_score": replay_result.get("confidence_score")
                },
                "differences": {},
                "similarity_score": 0.0
            }
            
            # Compare key metrics
            orig = original_summary
            replay = comparison["replay_summary"]
            
            differences = {}
            similarity_factors = []
            
            # Success comparison
            if orig.get("success") != replay.get("success"):
                differences["success"] = {
                    "original": orig.get("success"),
                    "replay": replay.get("success")
                }
            else:
                similarity_factors.append(1.0)
            
            # Content length comparison (with tolerance)
            orig_length = orig.get("content_length", 0)
            replay_length = replay.get("content_length", 0)
            
            if orig_length > 0:
                length_diff = abs(orig_length - replay_length) / orig_length
                if length_diff > 0.1:  # More than 10% difference
                    differences["content_length"] = {
                        "original": orig_length,
                        "replay": replay_length,
                        "difference_pct": length_diff * 100
                    }
                similarity_factors.append(max(0, 1.0 - length_diff))
            
            # Source count comparison
            orig_sources = orig.get("source_count", 0)
            replay_sources = replay.get("source_count", 0)
            
            if orig_sources != replay_sources:
                differences["source_count"] = {
                    "original": orig_sources,
                    "replay": replay_sources
                }
            else:
                similarity_factors.append(1.0)
            
            # Processing time comparison (informational, not part of similarity)
            orig_time = orig.get("processing_time", 0)
            replay_time = replay.get("processing_time", 0)
            
            if orig_time > 0 and replay_time > 0:
                time_factor = replay_time / orig_time
                differences["processing_time"] = {
                    "original": orig_time,
                    "replay": replay_time,
                    "factor": time_factor
                }
            
            # Calculate overall similarity
            similarity_score = sum(similarity_factors) / len(similarity_factors) if similarity_factors else 0.0
            comparison["similarity_score"] = similarity_score
            comparison["differences"] = differences
            
            # Determine overall result
            if not differences:
                comparison["overall_result"] = ComparisonResult.IDENTICAL.value
            elif similarity_score > 0.8:
                comparison["overall_result"] = ComparisonResult.SIMILAR.value
            else:
                comparison["overall_result"] = ComparisonResult.DIFFERENT.value
            
            return comparison
            
        except Exception as e:
            logger.error(f"Failed to compare results: {e}")
            return {
                "overall_result": ComparisonResult.ERROR.value,
                "error": str(e)
            }
    
    def _generate_replay_id(self, snapshot_id: str) -> str:
        """Generate replay ID"""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        return f"replay_{timestamp}_{snapshot_id[-8:]}"
    
    def _get_analysis_recommendations(self, success_rate: float, 
                                    comparison_results: Dict[str, int],
                                    error_patterns: Dict[str, int]) -> List[str]:
        """Get recommendations based on analysis"""
        recommendations = []
        
        if success_rate < 0.8:
            recommendations.append("Low replay success rate - investigate common failure patterns")
        
        total_comparisons = sum(comparison_results.values())
        if total_comparisons > 0:
            different_rate = comparison_results.get(ComparisonResult.DIFFERENT.value, 0) / total_comparisons
            if different_rate > 0.3:
                recommendations.append("High result variance in replays - check for non-deterministic behavior")
        
        if error_patterns:
            most_common_error = max(error_patterns.items(), key=lambda x: x[1])
            recommendations.append(f"Most common error: {most_common_error[0]} - investigate root cause")
        
        if not recommendations:
            recommendations.append("Replay results look healthy - continue monitoring")
        
        return recommendations


# Example usage
if __name__ == "__main__":
    async def test_replay():
        from config import CodexConfig
        from rag import CodexRAG
        
        config = CodexConfig()
        rag = CodexRAG(config)
        await rag.initialize()
        
        capturer = QueryCapturer(config)
        replayer = QueryReplayer(config, rag)
        
        # Test snapshot capture
        snapshot_id = await capturer.capture_query_state(
            "test_query_001",
            "What is the honor system?",
            {"scroll_type": "general"},
            rag
        )
        
        if snapshot_id:
            print(f"Captured snapshot: {snapshot_id}")
            
            # Test replay
            replay_result = await replayer.replay_query(snapshot_id)
            print(f"Replay result: {replay_result.status}")
        
        await rag.cleanup()
    
    asyncio.run(test_replay())