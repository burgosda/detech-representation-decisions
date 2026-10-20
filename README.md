# MDPI's Information biomedical terminology experiments: reproducibility materials

This repository accompanies the revised manuscript on term extraction, canonical-label prediction, and definition generation using internal DETECH 2026 holdouts. It contains experiment notebooks, locked split records, configurations, saved predictions and scores, prompt and generation records, and the post-review Task B audit.

## What can be checked immediately

Run `python verify_saved_results.py` from the repository root. This standard-library script checks core published numbers against the released CSV files without a GPU or an API key. The complete saved result tables and intervention-level predictions are under `journal_experiments/`.

| Manuscript analysis | Primary saved files |
| --- | --- |
| Task A five-seed decoding comparison | `taskA_holdout/results/pubmedbert_boundary_five_seed_all_variants_test_results.csv`, `pubmedbert_boundary_five_seed_paired_contrasts.csv`, and the 20 files in `taskA_holdout/predictions/` |
| Task A threshold and subgroup checks | `pubmedbert_boundary_five_seed_matched_threshold_summary.csv`, `pubmedbert_boundary_five_seed_test_subgroup_summary.csv` |
| Task A contextual intervention | `pubmedbert_boundary_seed42_development_collapse_diagnostic_summary.json`, `pubmedbert_boundary_five_seed_collapse_added_candidates.csv` |
| Task B linking and sensitivity | `taskB_holdout/results/taskB_test_compositional_results_locked.csv`, `taskB_test_compositional_change_audit.csv`, and `taskB_holdout/reviewer_audit/` |
| Task B definition generation | `taskB_holdout/predictions/*ISO*`, `taskB_holdout/results/taskB_definition_test_ISO_condition_metrics.csv`, `taskB_definition_test_ISO_detailed_metrics.csv`, `taskB_definition_collapse_active_intervention_audit.csv` |
| Revision audit | `notebooks/task_b_reviewer_audit.ipynb` and every file in `taskB_holdout/reviewer_audit/` |

The file `release_manifest.csv` records each released file's size and SHA-256 checksum.

## Source data

Get the original DETECH 2026 dataset from the organizers' repository: <https://github.com/gmdn/DETECH2026>. The source abstracts and original Task A/Task B training CSVs are not duplicated here. The notebooks expect them in the following local layout, where `DETECH_ROOT` is your own writable working folder:

```text
DETECH_ROOT/
  data/taskA/training/abstracts/{parkinson,mental_health}/
  data/taskA/training/csv/
  data/taskB/training/abstracts/{parkinson,mental_health}/
  data/taskB/training/csv/
  journal_experiments/{taskA_holdout,taskB_holdout}/
```

Copy the organizers' corresponding Task A and Task B source CSVs and abstract files into those `data/` folders. The notebooks' initial cells show the exact expected filenames. The internal holdouts are subsets of the challenge training resources; these are not scores on the organizers' hidden challenge test set. The released Task A document split and the separate Task B document and concept splits are in each task's `splits/` folder.

## Experiment code and computational requirements

- `notebooks/task_a.ipynb` is the original Colab workflow for Task A preprocessing, PubMedBERT boundary training, decoding, contextual clustering, evaluation, and five-seed checks.
- `notebooks/task_b.ipynb` is the original Colab workflow for Task B linking, contextual evidence ranking, prompt construction, generation, and evaluation.
- `notebooks/task_b_reviewer_audit.ipynb` computes partition composition, lookup routes, training familiarity, changed cases, repeated-prompt behavior, canonicalization sensitivity, and leave-one-group-out checks.

These notebooks were written as chronological research records, not as a one-click pipeline. They use a hard-coded Google Drive root (`/content/drive/MyDrive/MDPI Information/DETECH2026`) in several cells. To rerun them, first change all occurrences of that root to your local `DETECH_ROOT`, mount Drive if using Colab, and run the cells in their recorded order after installing the dependencies specified in their environment cells. Some cells inspect or update saved protocol files, and some superseded exploratory cells remain in the research record. Preserve the released locked splits and selected settings when reconstructing the reported experiment.

Task A uses `microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract`, five seeds (13, 21, 42, 77, 101), and the locked policies in `taskA_multiseed_robustness_protocol.json`. The seed-42 test was inspected before the additional four-seed robustness run; the protocol records this timing. GPU training checkpoints, optimizer states, logits, and embedding caches are omitted because of their size. The code and saved outputs document the analysis, but exact inference from an original trained checkpoint requires regenerating or obtaining that checkpoint.

Task B definition generation uses `gpt-4o-mini`, temperature 0, 120 maximum completion tokens, and up to three occurrence contexts. Prompts and both raw and canonicalized responses are included. The notebooks read `OPENAI_API_KEY` from a Colab secret; **no key is provided**. Identical prompts sometimes produced different API responses. The canonicalization rule retains the response from the earliest randomized API call for each exact prompt hash. Saved responses permit evaluation without new API calls, while a fresh API run may differ.

The semantic definition metric uses BERTScore with `microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext`. The combined score averages its 0–1 F1 with corpus SacreBLEU divided by 100. The original evaluation code in the Task B notebook specifies the tokenization, smoothing, and bootstrap procedure. API generation, model downloads, and GPU training require separate access and computational resources.

## Data and scope notes

The repository includes derived tables with mention labels, reference definitions, selected abstract passages in the definition prompts, and generated text. See the original DETECH repository for provenance of source material. The results are benchmark-relative and do not independently validate biomedical factual adequacy or ontology identity for open normalized labels. The reviewer audit uses the saved locked predictions and partitions; its leave-one-out checks do not retrain models or constitute new independent test partitions.

`results/` also contains metadata records with `${DETECH_ROOT}` as a placeholder for the original local Drive root. Some metadata entries name large intermediate files or checkpoints omitted from this compact release. The raw bootstrap replicate tables and split-search trial table are omitted; their summaries and the code to regenerate them are included.
