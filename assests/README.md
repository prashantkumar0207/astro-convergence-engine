# assets/

Static media supporting documentation: diagrams, flowcharts, architecture images, exported
Mermaid renders, icons and other documentation graphics.

Rules:
- Diagram *sources* (Mermaid/PlantUML text) live with the documents that use them or here
  alongside the export; a binary image without committed source is not accepted.
- File naming: `<doc-or-topic>__<short-name>__vNN.<ext>` (double underscore separators).
- Optimise images for repository size; prefer SVG for line art.
- No licensed/third-party media without a recorded license note in this folder.
