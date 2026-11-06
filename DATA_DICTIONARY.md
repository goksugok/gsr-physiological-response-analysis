# Data dictionary (archived pipeline)

| Field | Meaning |
|---|---|
| `participant` | Pseudonymous participant number; do not publish actual participant records |
| `trial` | Trial identifier from OpenSesame (`trial_id`) |
| `image_name` | Stimulus filename (not included in public archive) |
| `type` | Inferred `ai`/`real` using substring matching of stimulus name |
| `familiarity` | OpenSesame condition metadata |
| `opensesame_start_time` | Experiment image onset timestamp in milliseconds |
| `gsr_trial_start_time` | Aligned GSR image-onset timestamp in seconds |
| `response` | Recorded response |
| `correct` | Experiment correctness flag |
| `rt` | Response time as reported by OpenSesame (milliseconds) |
| `baseline_gsr` | First raw ADC count within the 4-second trial window |
| `peak_gsr` | Maximum raw ADC count within the trial window |
| `scr` | `peak_gsr - baseline_gsr` in raw ADC counts, *not* calibrated µS |
