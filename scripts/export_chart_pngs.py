# /// script
# dependencies = ["plotly", "kaleido"]
# ///
"""Export static PNGs from the audit's saved Plotly HTML charts.

Usage: uv run export_chart_pngs.py <audit-output-dir> [glob]

Extracts the figure spec (data + layout) embedded in each chart's
Plotly.newPlot() call, so no analysis is re-run. PNGs land in
<audit-output-dir>/png/ at 1200x675 @2x — sized for full-width
embedding in an executive document.
"""
import json
import sys
from pathlib import Path

import plotly.io as pio


def extract_args(html: str):
    """Return (data, layout) args of the Plotly.newPlot call via bracket matching."""
    i = html.index("Plotly.newPlot(")
    i = html.index(",", i) + 1  # skip div-id arg
    args = []
    for _ in range(2):  # data array, layout object
        while html[i] in " \n\t\r,":
            i += 1
        open_ch = html[i]
        close_ch = {"[": "]", "{": "}"}[open_ch]
        depth, j, in_str, esc = 0, i, False, False
        while True:
            c = html[j]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True
                elif c == open_ch:
                    depth += 1
                elif c == close_ch:
                    depth -= 1
                    if depth == 0:
                        break
            j += 1
        args.append(json.loads(html[i : j + 1]))
        i = j + 1
    return args


def main():
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("audit_output")
    pattern = sys.argv[2] if len(sys.argv) > 2 else "*.html"
    png_dir = out_dir / "png"
    png_dir.mkdir(parents=True, exist_ok=True)

    failed = []
    charts = sorted(out_dir.glob(pattern))
    if not charts:
        sys.exit(f"no charts matching {pattern} in {out_dir}")
    for f in charts:
        try:
            data, layout = extract_args(f.read_text())
            fig = pio.from_json(json.dumps({"data": data, "layout": layout}))
            fig.update_layout(template="plotly_white")
            fig.write_image(png_dir / (f.stem + ".png"), width=1200, height=675, scale=2)
            print(f"ok  {f.stem}.png")
        except Exception as e:  # keep going; report at the end
            failed.append(f.name)
            print(f"FAIL {f.name}: {e}", file=sys.stderr)

    print(f"{len(charts) - len(failed)}/{len(charts)} charts exported to {png_dir}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
