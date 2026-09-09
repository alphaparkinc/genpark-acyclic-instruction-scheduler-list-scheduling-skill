from client import InstructionScheduler

def main():
    print("=== Testing List Instruction Scheduler ===")
    insts = [
        ('load_x', []),
        ('load_y', []),
        ('compute', ['load_x', 'load_y']),
        ('write_back', ['compute'])
    ]
    latencies = {'load_x': 2, 'load_y': 2, 'compute': 1, 'write_back': 1}
    scheduler = InstructionScheduler(insts, latencies, resource_units=2)
    plan = scheduler.schedule()
    print("Scheduled timeline:", plan)
    assert len(plan['schedule']) == 4
    assert plan['total_cycles'] <= 5

    print("Instruction Scheduler verified successfully!")

if __name__ == '__main__':
    main()
