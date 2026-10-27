from flask import Flask, render_template, request
from collections import deque
import heapq

app = Flask(__name__)

# Synthetic campus map. Each edge is bidirectional unless stated otherwise.
# cost represents estimated travel units (not real metres or minutes).
EDGES = [
    ("Main Gate", "Admin Block", 2, "ramp"),
    ("Main Gate", "Library", 3, "path"),
    ("Admin Block", "Library", 2, "path"),
    ("Admin Block", "Academic Block", 3, "lift"),
    ("Library", "Academic Block", 2, "stairs"),
    ("Library", "Canteen", 3, "ramp"),
    ("Academic Block", "Canteen", 4, "path"),
    ("Academic Block", "Computer Lab", 2, "lift"),
    ("Canteen", "Computer Lab", 3, "path"),
    ("Computer Lab", "Auditorium", 3, "ramp"),
    ("Canteen", "Auditorium", 5, "path"),
]
LOCATIONS = sorted({x for e in EDGES for x in e[:2]})
HEURISTIC = {
    "Main Gate": 0, "Admin Block": 2, "Library": 3,
    "Academic Block": 4, "Canteen": 5, "Computer Lab": 6,
    "Auditorium": 8
}

def build_graph(allow_stairs=True, lift_available=True, closed_edge=None):
    graph = {name: [] for name in LOCATIONS}
    for a, b, cost, feature in EDGES:
        if feature == "stairs" and not allow_stairs:
            continue
        if feature == "lift" and not lift_available:
            continue
        if closed_edge and {a, b} == set(closed_edge):
            continue
        graph[a].append((b, cost, feature))
        graph[b].append((a, cost, feature))
    return graph

def bfs(graph, start, goal):
    queue = deque([(start, [start], 0)])
    seen = {start}
    expanded = 0
    while queue:
        node, path, cost = queue.popleft()
        expanded += 1
        if node == goal:
            return {"path": path, "cost": cost, "expanded": expanded}
        for nxt, edge_cost, _ in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, path + [nxt], cost + edge_cost))
    return {"path": [], "cost": None, "expanded": expanded}

def astar(graph, start, goal):
    # For this small synthetic map, heuristic values are illustrative estimates.
    # A* optimality depends on a suitable admissible heuristic for the selected goal.
    heap = [(HEURISTIC.get(start, 0), 0, start, [start])]
    best = {start: 0}
    expanded = 0
    while heap:
        _, cost, node, path = heapq.heappop(heap)
        if cost != best.get(node):
            continue
        expanded += 1
        if node == goal:
            return {"path": path, "cost": cost, "expanded": expanded}
        for nxt, edge_cost, _ in graph.get(node, []):
            new_cost = cost + edge_cost
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                # Goal-specific zero heuristic is safe fallback if the supplied
                # illustrative heuristic is not calibrated for the selected goal.
                h = 0 if goal != "Auditorium" else HEURISTIC.get(nxt, 0)
                heapq.heappush(heap, (new_cost + h, new_cost, nxt, path + [nxt]))
    return {"path": [], "cost": None, "expanded": expanded}

def csp_assignments():
    """Backtracking CSP with forward checking for simulated support requests."""
    requests_data = {
        "Request A": {"needs": "mobility", "slot": "Morning"},
        "Request B": {"needs": "visual", "slot": "Morning"},
        "Request C": {"needs": "mobility", "slot": "Afternoon"},
    }
    staff = {
        "Anu": {"skills": {"mobility"}, "slots": {"Morning", "Afternoon"}},
        "Ravi": {"skills": {"visual", "mobility"}, "slots": {"Morning"}},
        "Maya": {"skills": {"visual"}, "slots": {"Afternoon"}},
    }
    domains = {}
    for req, details in requests_data.items():
        domains[req] = [
            person for person, info in staff.items()
            if details["needs"] in info["skills"] and details["slot"] in info["slots"]
        ]
    assignment = {}
    nodes = 0
    def backtrack(unassigned, current_domains):
        nonlocal nodes
        nodes += 1
        if not unassigned:
            return True
        req = min(unassigned, key=lambda r: len(current_domains[r]))
        for person in current_domains[req]:
            # Constraint: a staff member can handle at most one request per slot.
            conflict = any(
                assigned_person == person and
                requests_data[assigned_req]["slot"] == requests_data[req]["slot"]
                for assigned_req, assigned_person in assignment.items()
            )
            if conflict:
                continue
            assignment[req] = person
            new_unassigned = [r for r in unassigned if r != req]
            new_domains = {r: list(current_domains[r]) for r in new_unassigned}
            # Forward checking: remove this person from same-slot domains.
            for other in new_unassigned:
                if requests_data[other]["slot"] == requests_data[req]["slot"]:
                    new_domains[other] = [p for p in new_domains[other] if p != person]
            if all(new_domains[r] for r in new_unassigned) and backtrack(new_unassigned, new_domains):
                return True
            del assignment[req]
        return False
    solved = backtrack(list(requests_data), domains)
    return {"assignment": assignment if solved else {}, "nodes": nodes, "requests": requests_data}

def infer_facts(lift_available, closed_edge, mobility_need):
    facts = []
    rules = []
    if mobility_need:
        facts.append("mobility_support_required")
        rules.append("IF mobility_support_required THEN avoid_stairs")
    if not lift_available:
        facts.append("lift_unavailable")
        rules.append("IF lift_unavailable THEN lift_edges_blocked")
    if closed_edge:
        facts.append("path_closure_reported")
        rules.append("IF path_closure_reported THEN exclude_closed_edge")
    conclusions = []
    if "mobility_support_required" in facts:
        conclusions.append("avoid_stairs")
    if "lift_unavailable" in facts:
        conclusions.append("lift_edges_blocked")
    if "path_closure_reported" in facts:
        conclusions.append("exclude_closed_edge")
    return facts, rules, conclusions

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    start = "Main Gate"
    goal = "Auditorium"
    mobility = True
    lift_available = True
    closure = ""
    if request.method == "POST":
        start = request.form.get("start", start)
        goal = request.form.get("goal", goal)
        mobility = request.form.get("mobility") == "yes"
        lift_available = request.form.get("lift") == "yes"
        closure = request.form.get("closure", "").strip()
        closed_edge = closure.split("|") if "|" in closure else None
        if start == goal:
            error = "Choose two different locations."
            result = {"error": error}
        elif start not in LOCATIONS or goal not in LOCATIONS:
            result = {"error": "Please select valid campus locations."}
        else:
            graph = build_graph(allow_stairs=not mobility, lift_available=lift_available,
                                closed_edge=closed_edge)
            b = bfs(graph, start, goal)
            a = astar(graph, start, goal)
            facts, rules, conclusions = infer_facts(lift_available, closed_edge, mobility)
            csp = csp_assignments()
            result = {"bfs": b, "astar": a, "facts": facts, "rules": rules,
                      "conclusions": conclusions, "csp": csp,
                      "mobility": mobility, "lift_available": lift_available,
                      "closure": closure}
    return render_template("index.html", locations=LOCATIONS, start=start, goal=goal,
                           mobility=mobility, lift_available=lift_available,
                           closure=closure, result=result)

if __name__ == "__main__":
    app.run(debug=True)
