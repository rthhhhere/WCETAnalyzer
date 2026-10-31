import os
import json
from models import ProcessorModel, OperationModel
import services

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(current_dir, '..', 'data', 'input.json')
    
    try:
        if not os.path.exists(input_path):
            print(f"Ошибка: файл данных не найден.\nОжидаемый путь: {input_path}")
            return

        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        proc_data = data["processor"]
        processor = ProcessorModel(
            baseOperationCost=proc_data["baseOperationCost"],
            cacheMissPenalty=proc_data["cacheMissPenalty"],
            branchMispredictionPenalty=proc_data["branchMispredictionPenalty"],
            deadlineCycles=proc_data["deadlineCycles"]
        )
        
        operations = [
            OperationModel(
                name=op["name"],
                type=op["type"],
                memoryAccesses=op["memoryAccesses"],
                branches=op["branches"]
            )
            for op in data["operations"]
        ]
        
        if processor.baseOperationCost <= 0 or processor.deadlineCycles <= 0:
            print("Ошибка: Некорректные базовые параметры процессора.")
            return
            
        for op in operations:
            if op.memoryAccesses < 0 or op.branches < 0:
                print(f"Ошибка: Некорректные параметры в операции {op.name}")
                return

        print("ОЦЕНКА ВРЕМЕНИ ВЫПОЛНЕНИЯ (WCET)")
        print("-" * 78)
        print(f"{'Операция':<24} {'Тип':<10} {'Обращения':<12} {'Ветвления':<11} {'Лучшее':<9} {'Худшее':<9}")
        print("-" * 78)
        
        for op in operations:
            best = services.best_case(op, processor)
            worst = services.worst_case(op, processor)
            print(f"{op.name:<24} {op.type:<10} {op.memoryAccesses:<12} {op.branches:<11} {best:<9} {worst:<9}")
            
        total_bcet = services.bcet(operations, processor)
        total_wcet = services.wcet(operations, processor)
        ratio = services.nondeterminism_ratio(operations, processor)
        breakdown = services.source_breakdown(operations, processor)
        
        print("-" * 78)
        print(f"BCET: {total_bcet} тактов")
        print(f"WCET: {total_wcet} тактов")
        print(f"Коэффициент недетерминизма: {ratio:.2f}")
        print(f"Вклад памяти (кэш-промахи): {breakdown.memoryPenalty} тактов")
        print(f"Вклад ветвлений (ошибки предсказания): {breakdown.branchPenalty} тактов")
        print(f"Общий штраф за недетерминизм: {breakdown.totalPenalty} тактов")
        print(f"Дедлайн: {processor.deadlineCycles} тактов")
        
        if total_wcet <= processor.deadlineCycles:
            print("Результат: фрагмент укладывается в дедлайн.")
        else:
            print("Результат: фрагмент НЕ укладывается в дедлайн.")
            
    except json.JSONDecodeError as ex:
        print(f"Ошибка чтения JSON: {ex}")
    except Exception as ex:
        print(f"Непредвиденная ошибка: {ex}")

if __name__ == "__main__":
    main()
