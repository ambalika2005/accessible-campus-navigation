Airin jerry,Ajil Denny,Alan James,ALdrin Andrus,Allen p Jison,Ambalika ES
# Group 3 — Accessible Campus Navigation
**Course:** CST401 Artificial Intelligence (S7, 2019 Scheme)  
**SDGs:** 4, 10 and 11

## Overview
A small teaching prototype that finds routes between fictional campus locations while considering stairs, lift availability and a closed path. It demonstrates an intelligent agent (CO1), uninformed and informed search (CO2), a constraint satisfaction problem (CO3), and rule-based knowledge representation/inference (CO4).

## Requirements
- Python 3.10 or newer
- Flask (installed from `requirements.txt`)

## Run
1. Extract the ZIP.
2. Open a terminal in this project folder.
3. Create/activate a virtual environment if desired.
4. Install dependencies: `python -m pip install -r requirements.txt`
5. Start: `python app.py`
6. Open `http://127.0.0.1:5000` in a browser.

## Project structure
- `app.py` — synthetic map, BFS, A*, CSP/backtracking + forward checking, rule inference, Flask route.
- `templates/index.html` — web interface.
- `requirements.txt` — Python dependency.
- `PROJECT_DOCUMENTATION.docx` — report with CO mapping, PEAS, algorithms, test plan, limitations and AI-use disclosure.
- `test_cases.md` — manual test plan.

## CO mapping
- **CO1:** agent/environment and PEAS.
- **CO2:** BFS and A* comparison.
- **CO3:** staff-to-request CSP using backtracking and forward checking.
- **CO4:** facts/rules and forward inference.

## Important assumptions and limitations
- Campus locations, connections and costs are synthetic.
- Costs are abstract units, not verified distances or travel times.
- This is a classroom prototype, not a production navigation or safety tool.
- The A* heuristic is illustrative and only used for the Auditorium goal; use a goal-specific admissible heuristic for a rigorous optimality guarantee.
- BFS minimises edge count, not weighted path cost.
- Only one selected closure can be tested at a time in the interface.
- The inference component demonstrates simple rules rather than a full logic engine.
- No personal or real student data is included.

## Verification
Run through at least the cases in `test_cases.md`. Check that each selected constraint is reflected in the generated graph and that displayed paths use only available edges. Record screenshots and actual outputs from your own run before submission.

## AI-use record
This starter project was drafted with assistance from ChatGPT for structure, code and documentation. The team must inspect, run and test the code, correct any issues, record what it changed, and be ready to explain every component. Do not claim tests were passed unless your team has actually run them.
