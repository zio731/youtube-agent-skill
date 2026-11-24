---
name: optimus-youtube
description: Support Optimus Grid long-form YouTube production with script hooks, title-thumbnail checks, edit suggestions, retention CSV analysis, chapters and weekly planning. Use when Fabio requests these editorial workflows or explicitly invokes the adapted YouTube Agent skill.
license: MIT
---

# Optimus Grid YouTube editorial tools

Adapted from Jakeschincariol/youtube-agent-skill; MIT notice retained in LICENSE.
Resolve SKILL_DIR as the folder containing this file. Use an available Python interpreter; on Fabio's PC Python 3.12 is available. Tools use only the standard library and print results; they do not edit media or publish.

## Project context

- Drafts and discussion in Italian. Final channel language is American English for a US audience.
- Neutral reporting on AI, robotics, work and government choices. Trace factual claims to original sources; distinguish announcements, demonstrations, forecasts and measured deployment.
- Read the relevant existing pilot/project files before starting a new draft. News archive notes are leads, not verified sources.
- Fabio schedules and publishes manually in YouTube Studio. The daily Shorts automation is outside this project. Only prepare Shorts if explicitly requested; never add them by default to a long-video plan.
- Use session context as the voice brief. Do not require three videos or create an unrelated global voice profile before working.
- Use available vidIQ skills/tools for live analytics, packaging and search demand where applicable. These local scripts supplement those tools; their scores do not predict views, CTR or retention.

## Select the requested mode

Read only the relevant reference. References contain upstream editorial heuristics, which the qualifications below take precedence over. Script commands in a reference run against SKILL_DIR/tools/<mode>/, not the current directory.

| Mode | Reference | Tool |
| --- | --- | --- |
| script/hooks | references/yt-script.md | tools/yt-script/hookscore.py and hooks.json |
| title + thumbnail pairing | references/yt-package.md | tools/yt-package/title.py |
| transcript edit suggestions | references/yt-edit.md | tools/yt-edit/deadair.py |
| retention | references/yt-retention.md | tools/yt-retention/retention.py |
| chapters | references/yt-chapters.md | tools/yt-chapters/chapters.py |
| public-video outliers | references/yt-viral.md | tools/yt-viral/swipe.py |
| descriptions/tags | references/yt-seo.md | no executable |
| weekly plan | references/yt-plan.md | no executable |
| channel audit | references/yt-audit.md | supplement verified channel evidence |
| comment drafts | references/yt-comment.md | drafts only, no sending |
| optional Shorts | references/yt-shorts.md | only when explicitly requested |

## Interpretation and execution

Hook and title tools are English lexical heuristics. Use on the final English text, or label an Italian result uncalibrated. Favor accurate, engaging openings over fear, sensational claims or a higher heuristic score. Timings such as 15 seconds and 150 words/minute are editing starting points; use the actual voice file for final duration.

The retention tool requires explicit --axis seconds|percent|fraction; add --duration for relative axes. It reports descriptive changes in percentage points, not causes. Compare the channel's videos at similar length/age and audience; a 25-point opening loss is not a universal threshold, and a flat curve cannot prove a packaging problem. Review transcript and sampled scenes before suggesting an explanation.

Transcript cuts are suggestions. Keep meaningful pauses, on-screen demonstrations and original media. Compare proposed cut intervals to footage before applying any actual edit. Chapters need semantic retitling and timing checks on the final export. Outlier comparisons need observed views, comparable publication ages/formats and a disclosed baseline sample; missing figures are not zeros.

A weekly plan should fit the requested long-form episode and available work already established in chat; do not mandate an extra video or Shorts. Finish with the concrete requested deliverable, limitations and an actionable next step. Do not append a generic permission question to every output.

For video evidence use optimus-watch; for a requested finished explanatory video use create-video-essay and the selected installed renderer. This skill itself does not render a video or access YouTube Studio.
