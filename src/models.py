from dataclasses import dataclass, field
from typing import List

@dataclass
class ProcessorModel:
    baseOperationCost: int
    cacheMissPenalty: int
    branchMispredictionPenalty: int
    deadlineCycles: int

@dataclass
class OperationModel:
    name: str
    type: str
    memoryAccesses: int
    branches: int

@dataclass
class SourceBreakdownResult:
    memoryPenalty: int
    branchPenalty: int
    
    @property
    def totalPenalty(self) -> int:
        return self.memoryPenalty + self.branchPenalty

@dataclass
class InputDataModel:
    processor: ProcessorModel
    operations: List[OperationModel] = field(default_factory=list)
