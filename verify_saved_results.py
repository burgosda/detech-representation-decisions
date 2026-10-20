"""Check core reported values against the released saved result tables.

Run: python verify_saved_results.py
Uses only Python's standard library; does not retrain or call an API.
"""
import csv
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent
A = ROOT / 'journal_experiments/taskA_holdout'
B = ROOT / 'journal_experiments/taskB_holdout'

def read(path):
    with path.open(newline='', encoding='utf-8-sig') as handle:
        return list(csv.DictReader(handle))

def near(actual, expected, tolerance=5e-5):
    assert abs(actual - expected) < tolerance, (actual, expected)

seeds = read(A/'results/pubmedbert_boundary_five_seed_all_variants_test_results.csv')
assert len(seeds) == 20
assert {int(row['seed']) for row in seeds} == {13, 21, 42, 77, 101}
for variant, expected in [('NESTED_NEURAL', 0.3275307435910329),
                          ('NONOVERLAP_NEURAL', 0.5592225779729555)]:
    subset = [row for row in seeds if row['variant'] == variant]
    assert len(subset) == 5
    near(mean(float(row['avg_micro_f1']) for row in subset), expected, 1e-10)

linking = read(B/'results/taskB_test_compositional_results_locked.csv')
for system, score in [('MORPHOLOGICAL_OPEN', 0.8110),
                      ('COMPOSITIONAL_MINCHAR_5', 0.7829)]:
    row, = (r for r in linking if r['system'] == system and r['domain'] == 'ALL')
    assert int(row['mention_inputs']) == 122
    assert int(row['gold_links']) == 131
    near(float(row['micro_f1']), score)

scores = read(B/'reviewer_audit/linking_training_familiarity_link_level_scores.csv')
assert len(scores) == 4
assert {int(r['gold_links']) for r in scores} == {100, 31}
changes = read(B/'reviewer_audit/linking_changed_cases.csv')
assert len(changes) == 13

definitions = read(B/'results/taskB_definition_test_ISO_condition_metrics.csv')
assert len(definitions) == 3
assert {int(row['n_concepts']) for row in definitions} == {48}
by_condition = {row['condition']: row for row in definitions}
assert set(by_condition) == {'CONCEPT_ONLY','UNRANKED_CONTEXTS','COLLAPSE_K50'}
delta = (float(by_condition['COLLAPSE_K50']['descriptive_combined_score'])
         - float(by_condition['UNRANKED_CONTEXTS']['descriptive_combined_score']))
near(delta, -0.000776, 5e-7)
print('Saved result checks passed.')
print('Task A: five seeds and main decoding means match the saved tables.')
print('Task B linking: 122 inputs, 131 links, 13 changed inputs; reported F1 values match.')
print('Task B definitions: 48 concepts and collapse-minus-unranked combined score match.')
