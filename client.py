class InstructionScheduler:
    """Critical-Path List Instruction Scheduler."""
    def __init__(self, instructions, latencies, resource_units=2):
        self.instructions = instructions
        self.latencies = latencies
        self.resource_units = resource_units

    def schedule(self):
        succs = {i[0]: [] for i in self.instructions}
        preds = {i[0]: [] for i in self.instructions}
        for i_id, dep_list in self.instructions:
            preds[i_id] = list(dep_list)
            for d in dep_list:
                succs[d].append(i_id)

        def get_priority(node):
            if not succs[node]:
                return self.latencies.get(node, 1)
            return self.latencies.get(node, 1) + max(get_priority(s) for s in succs[node])

        priorities = {i[0]: get_priority(i[0]) for i in self.instructions}
        ready = [i[0] for i in self.instructions if not preds[i[0]]]
        ready.sort(key=lambda n: priorities[n], reverse=True)

        schedule_order = []
        cycle = 0
        in_flight = {}
        completed = set()

        while len(completed) < len(self.instructions):
            finished = [inst for inst, fin_time in in_flight.items() if fin_time <= cycle]
            for f in finished:
                del in_flight[f]
                completed.add(f)
                for s in succs[f]:
                    if all(p in completed for p in preds[s]) and s not in ready and s not in in_flight:
                        ready.append(s)
            ready.sort(key=lambda n: priorities[n], reverse=True)

            issued = 0
            while ready and issued < self.resource_units:
                nxt = ready.pop(0)
                schedule_order.append((nxt, cycle))
                in_flight[nxt] = cycle + self.latencies.get(nxt, 1)
                issued += 1

            cycle += 1

        return {
            'schedule': schedule_order,
            'total_cycles': cycle - 1
        }
