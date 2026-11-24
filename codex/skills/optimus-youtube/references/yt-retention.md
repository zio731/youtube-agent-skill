# Retention mode

Run the adapted tool with explicit units:

```powershell
python "SKILL_DIR/tools/yt-retention/retention.py" retention.csv --axis seconds --json
python "SKILL_DIR/tools/yt-retention/retention.py" retention.csv --axis percent --duration 600 --transcript transcript.srt --json
```

Use --axis fraction only for positions from 0 to 1. Values are percentages by default; use --values fraction for retention from 0 to 1. Semicolon-separated decimal-comma CSV is supported. Keep zeros; reject unordered or nonfinite observations.

The report describes opening loss in percentage points, observed drop intervals and a net middle slope. Sparse samples do not locate the exact instant of departure. Compare meaningful peers and read the corresponding scenes and transcript before forming hypotheses. Neither a 25-point loss nor a particular slope is a universal quality verdict. A correlation with spoken words does not prove why people left.

Return the most consequential observation, the supporting times/data, uncertainties, and a concrete edit experiment. If there are no real retention data, do not manufacture them from views or a script score.
