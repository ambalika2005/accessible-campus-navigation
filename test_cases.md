# Test cases (run manually and record actual output)

| ID | Inputs | Expected behavior to verify |
|---|---|---|
| T1 | Main Gate → Auditorium; avoid stairs; lift available; no closure | A route should be found without using the Library–Academic Block stairs edge. |
| T2 | Main Gate → Auditorium; avoid stairs; lift unavailable; no closure | Lift edges are removed; route may still exist through ramps/paths. |
| T3 | Main Gate → Auditorium; avoid stairs; lift available; close Computer Lab–Auditorium | Route should avoid the closed edge if an alternate route exists. |
| T4 | Main Gate → Library; any valid settings | A route should be found; inspect BFS and A* paths/costs. |
| T5 | Same start and destination | Interface should display a validation message. |
| T6 | Try several different start/destination pairs and constraints | Record route found/not found, cost and expanded nodes. |

**Submission reminder:** Add screenshots and actual observations after running the prototype. Do not treat these expected outcomes as completed test evidence.
