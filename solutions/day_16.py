import time
from copy import copy
from typing import List, Dict, Tuple
from itertools import permutations
import asyncio as aio

# how many timesteps did the action take, what was the value of the action (unmodified by time value),
# tuple of workers acting and valves opened by each
Action = Tuple[int, int, List[Tuple[int, str]]]


class Valve:
    def __init__(self, valve_id: str, others: List[str], flow_rate: int):
        self.valves_to_connect_to: List[str] = others
        self.id: str = valve_id
        self.flow_rate: int = flow_rate
        self.links = []  # Valves
        self.map_to_valves: Dict = {}  # str to Valve
        all_valves[self.id] = self

    def __repr__(self):
        return self.id


class Worker:
    def __init__(self, current_valve: Valve, worker_id: int):
        self.current_valve: Valve = current_valve
        self.target: str = ""  # note that bool("") == False
        self.id: int = worker_id

    def dist_to_target(self):
        return len(self.current_valve.map_to_valves[self.target]) + 1

    def provide_copy(self):
        other = Worker(current_valve=self.current_valve, worker_id=self.id)
        other.target = self.target
        return other

    def __repr__(self):
        s = f"{self.current_valve.id} -> {self.target}"
        if self.target:
            s += f" ({self.dist_to_target()})"
        return s


def bfs_find_distances(focused_valve: Valve):
    queue = []
    parentage: Dict[str, List[str]] = {focused_valve.id: []}
    queue.append((focused_valve, []))
    while queue:
        current_valve, parent = queue.pop(0)
        for neighbor in current_valve.links:
            if neighbor.id not in parentage:
                parentage[neighbor.id] = copy(
                    parentage[current_valve.id] + [neighbor.id]
                )
                queue.append((neighbor, current_valve.id))
    focused_valve.map_to_valves = parentage


def connect_valves():
    for valve in all_valves.values():
        for other_id in valve.valves_to_connect_to:
            other = all_valves[other_id]
            valve.links.append(other)
    for valve in all_valves.values():
        bfs_find_distances(valve)


def get_value_skipping_alone(
        current: Valve, to_visit: List[str], time_remaining: int
) -> int:
    if not to_visit:
        return 0
    values = [0]
    for vid in to_visit:
        next_to_visit = copy(to_visit)
        next_to_visit.remove(vid)
        time_to_open = len(current.map_to_valves[vid]) + 1
        if time_remaining - time_to_open < 0:
            continue
        value_of_vid = (time_remaining - time_to_open) * all_valves[vid].flow_rate
        value_of_others = get_value_skipping_alone(
            all_valves[vid], next_to_visit, time_remaining - time_to_open
        )
        values.append(value_of_vid + value_of_others)
    return max(values)


def get_target_sets(lst: List, num_workers: int):
    return list(permutations(lst, num_workers))


async def pair_get_value(
        workers: List[Worker],
        to_visit: List[str],
        time_remaining: int,
        targets_to_assign: List[Tuple[str, int]],
        already_opened: List[str],
        depth: int,
) -> Tuple[int, List[Action]]:
    # copy of the workers (copied to not interfere with previous worker objects in recursion)
    next_workers = [worker.provide_copy() for worker in workers]
    # same, but for unvisited valves
    next_to_visit = copy(to_visit)
    # same, but for opened valves
    next_already_opened = copy(already_opened)

    # assign workers to targets
    for target, worker_id in targets_to_assign:
        # remove targets from pool of unvisited valves (only if in pool)
        # possible to target a valve not in the pool if one worker is targeting the other's target
        if target in next_to_visit:
            next_to_visit.remove(target)
        next(
            (worker for worker in next_workers if worker.id == worker_id)
        ).target = target

    # create unique key based on locations, targets, unvisited valves
    # value stored is expected reward times time diff? something like "value 6 times your timestep minus 4"?
    first_worker = min(next_workers, key=lambda x: x.current_valve.id + x.target)
    second_worker = max(next_workers, key=lambda x: x.current_valve.id + x.target)
    unique_key = (
            first_worker.current_valve.id
            + ":"
            + first_worker.target
            + ":"
            + second_worker.current_valve.id
            + ":"
            + second_worker.target
            + ":"
            + str(next_to_visit)
    )
    # if key exists in memoized paths, then this path has already been investigated
    # so we can just return that
    global lock
    async with lock:
        if unique_key in memoized_paths:
            global times_consulted
            times_consulted += 1
            memoized_result = memoized_paths[unique_key]
            val = 0
            time_ahead = 0
            for action in memoized_result:
                time_ahead += action[0]
                if time_remaining - time_ahead >= 0:
                    val += action[1] * (time_remaining - time_ahead)
            paths = memoized_paths[unique_key]
            return val, paths

    # how long it takes workers to open their target valves - we skip valves which don't have flow rates > 0
    times_to_opening = [worker.dist_to_target() for worker in next_workers]
    time_to_next_opening = min(times_to_opening)
    next_timestamp: int = time_remaining - time_to_next_opening

    # return no value and no action if no action could be completed before running out of time
    if next_timestamp < 0:
        return 0, []

    # values from valves being opened this action
    value_of_valves_opening_now = []
    # description of this action, list of workers and the valves they're opening
    # does not necessarily include all workers if arrivals are staggered
    this_action_items: List[Tuple[int, str]] = []

    # the actual doing part of the function
    # each worker evaluates if they're going to make it to their target this action
    # if they are, then we check that nobody else is already there (should be the only case in which valves can
    # be opened multiple times). if someone's already there, stop targeting there
    # if it's clear, add that you went there as an action, get the value for it, go there, await new target
    # if you can't get there in time, move as close as you can while the other guy moves to its
    for worker in next_workers:
        if worker.target in next_already_opened:
            worker.target = ""
            continue
        if worker.dist_to_target() == time_to_next_opening:
            # only open a valve if it hasn't yet been opened (i.e. the other guy has already gotten there)
            if worker.target not in next_already_opened:
                next_already_opened.append(worker.target)
                this_action_items.append((worker.id, worker.target))
                value_for_opening = all_valves[worker.target].flow_rate
                value_of_valves_opening_now.append(value_for_opening)
                worker.current_valve = all_valves[worker.target]
                worker.target = ""
            else:
                worker.target = ""
                continue
        else:
            worker.current_valve = all_valves[
                worker.current_valve.map_to_valves[worker.target][
                    time_to_next_opening - 1
                    ]
            ]

    # recurse
    value_of_subsequent, continued_paths = await pair_do_targeting(
        next_workers,
        next_to_visit,
        time_remaining - time_to_next_opening,
        next_already_opened,
        depth,
    )
    # record full details of this action, adding future results, memoize that
    value_of_this_action = sum(value_of_valves_opening_now) * next_timestamp
    this_action: Action = (time_to_next_opening, sum(value_of_valves_opening_now), this_action_items)
    future_history: List[Action] = [this_action, *continued_paths]
    async with lock:
        if (x := len(memoized_paths)) % 100 == 0:
            if x > 0:
                print(x)
        memoized_paths[unique_key] = future_history
    answer: Tuple[int, List[Action]] = (
        value_of_this_action + value_of_subsequent,
        future_history,
    )

    return answer


async def pair_do_targeting(
        workers: List[Worker],
        to_visit: List[str],
        time_remaining: int,
        already_opened: List[str],
        depth: int = 0,
) -> Tuple[int, List[Action]]:
    # if no worker has a target and no targets remain, all value has been extracted from this branch
    if not to_visit and not [w for w in workers if w.target]:
        return 0, []

    values = []  # values of subpaths taken

    # global start_time
    # print("\t" * depth + f"{depth}, t: {round(time.time() - start_time, 3)}, p: {len(memoized_paths)}, c: {times_consulted}")
    if not workers[0].target and not workers[1].target:
        if len(to_visit) >= 2:
            tasks = []
            for target_1 in to_visit:
                for target_2 in to_visit:
                    if not target_1 == target_2:
                        tasks.append(aio.create_task(pair_get_value(
                            copy(workers),
                            copy(to_visit),
                            time_remaining,
                            [(target_1, workers[0].id), (target_2, workers[1].id)],
                            copy(already_opened),
                            depth + 1,
                        )))
            results = await aio.gather(*tasks)
            values.extend(results)

        else:
            target = to_visit[0]
            value = await pair_get_value(
                workers,
                to_visit,
                time_remaining,
                [(target, workers[0].id), (target, workers[1].id)],
                already_opened,
                depth + 1,
            )
            values.append(value)
    else:
        if to_visit:
            tasks = []
            for target in to_visit:
                values.append(await pair_get_value(
                    workers,
                    to_visit,
                    time_remaining,
                    [(target, next(w for w in workers if not w.target).id)],
                    already_opened,
                    depth + 1
                ))
            #     tasks.append(aio.create_task(pair_get_value(
            #         copy(workers),
            #         copy(to_visit),
            #         time_remaining,
            #         [(target, next(w for w in workers if not w.target).id)],
            #         copy(already_opened),
            #         depth + 1,
            #     )))
            # results = await aio.gather(*tasks)
            # values.extend(results)
        else:
            value = await pair_get_value(
                workers,
                to_visit,
                time_remaining,
                [
                    (
                        next(w for w in workers if w.target).target,
                        next(w for w in workers if not w.target).id,
                    )
                ],
                already_opened,
                depth + 1,
            )
            values.append(value)

    return max(values, key=lambda x: x[0])


def set_up_valves():
    with open(f"../inputs/day_16.txt", "r") as input_file:
        for line in input_file.readlines():
            line = line.strip()
            valve_id = line.split("Valve ")[1].split(" ")[0]
            flow_rate = line.split("rate=")[1].split(";")[0]
            if "leads to valve " in line:
                others = [other for other in line.split("valve ")[1].split(", ")]
            else:
                others = [other for other in line.split("valves ")[1].split(", ")]
            Valve(valve_id, others, int(flow_rate))
    connect_valves()


def part_1():
    set_up_valves()
    start = all_valves["AA"]
    to_visit = [vid for vid, valve in all_valves.items() if valve.flow_rate > 0]
    time_remaining = 30
    print(get_value_skipping_alone(start, to_visit, time_remaining))


# unsure if part 2 works, takes a while to run
def part_2():
    set_up_valves()
    start = all_valves["AA"]
    workers = [Worker(start, 0), Worker(start, 1)]
    to_visit = [vid for vid, valve in all_valves.items() if valve.flow_rate > 0]
    already_opened = []
    time_remaining = 26
    value, action_history = aio.run(pair_do_targeting(
        workers, to_visit, time_remaining, already_opened
    ))
    print(value)
    print(f"Memoized {len(memoized_paths)} paths.")
    print(f"Consulted {times_consulted} times.")
    for i in range(1, time_remaining + 1):
        print(f"== Minute {i} ==")
        for action in action_history:
            if action[0] == i:
                if action[2]:
                    for worker, valve in action[2]:
                        print(
                            f"Worker {worker} opens valve {valve} (value {all_valves[valve].flow_rate * (time_remaining - i)})"
                        )
                    print(f"Value {action[1]}")
    print()


all_valves: Dict[str, Valve] = {}
memoized_paths: Dict[str, List[Action]] = {}
times_consulted: int = 0
lock = aio.Lock()
# start_time = time.time()

if __name__ == "__main__":
    # part_1()
    part_2()
