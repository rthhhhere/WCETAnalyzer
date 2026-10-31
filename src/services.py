from typing import List
from models import OperationModel, ProcessorModel, SourceBreakdownResult

def best_case(op: OperationModel, model: ProcessorModel) -> int:
    return model.baseOperationCost

def worst_case(op: OperationModel, model: ProcessorModel) -> int:
    return (model.baseOperationCost + 
            (op.memoryAccesses * model.cacheMissPenalty) + 
            (op.branches * model.branchMispredictionPenalty))

def bcet(fragment: List[OperationModel], model: ProcessorModel) -> int:
    return sum(best_case(op, model) for op in fragment)

def wcet(fragment: List[OperationModel], model: ProcessorModel) -> int:
    return sum(worst_case(op, model) for op in fragment)

def nondeterminism_ratio(fragment: List[OperationModel], model: ProcessorModel) -> float:
    best = bcet(fragment, model)
    if best <= 0:
        raise ValueError("BCET должен быть больше нуля.")
    return wcet(fragment, model) / best

def source_breakdown(fragment: List[OperationModel], model: ProcessorModel) -> SourceBreakdownResult:
    mem_penalty = sum(op.memoryAccesses * model.cacheMissPenalty for op in fragment)
    branch_penalty = sum(op.branches * model.branchMispredictionPenalty for op in fragment)
    return SourceBreakdownResult(memoryPenalty=mem_penalty, branchPenalty=branch_penalty)
