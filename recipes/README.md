# Production recipes

CLI scripts for common studio and marketing workflows. Choices track the
**most frequent Adobe Community / Reddit automation asks** (layers-to-files,
watermarks, sRGB delivery, padding, template text swap).

| Recipe | Script | Forum / studio use case |
|--------|--------|-------------------------|
| [Batch export](batch_export/) | `export_folder.py` | Deliver JPEG/PNG from a source folder |
| [Layer comps](layer_comps/) | `export_comps.py` | Design variant handoff |
| [Run action on folder](run_action/) | `run_action_folder.py` | Actions-panel macros at scale |
| [JSX from Python](jsx_bridge/) | `run_jsx.py` | Reuse existing ExtendScript |
| [Smart object replace](smart_object/) | `replace_smart_object.py` | Template / mockup pipelines |
| [**Export layers**](export_layers/) | `export_layers.py` | **#1 ask** — each layer → file |
| [**Watermark**](watermark/) | `watermark_folder.py` | Proofs, portfolios, client previews |
| [**Convert sRGB**](convert_srgb/) | `convert_srgb.py` | Web-safe color for browsers |
| [**Canvas border**](canvas_border/) | `add_border.py` | Padding / social safe margins |
| [**Text replace**](text_replace/) | `replace_text.py` | Localization & PSD templates |

Install helpers first:

```bash
pip install -e ".[windows]"
```

Examples:

```bash
python recipes/export_layers/export_layers.py ./out --format png
python recipes/watermark/watermark_folder.py ./in ./out --text "© Studio"
python recipes/convert_srgb/convert_srgb.py ./in ./out --format jpg
python recipes/canvas_border/add_border.py ./in ./out --padding 48
python recipes/text_replace/replace_text.py ./psds "DRAFT" "FINAL" --output ./out
```

GUI equivalents live in the [Photoshop Toolkit](../tools/photoshop_toolkit/).
