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


ACCENT = "#2C5282"  # single data hue used across the whole report
GRAY = "#A0AEC0"    # reference/context lines only


def ramp(n):
    """n shades light->dark of the accent hue, for multi-series charts."""
    lo, hi = (178, 194, 219), (31, 58, 95)
    if n == 1:
        return [ACCENT]
    return ["#%02x%02x%02x" % tuple(int(lo[k] + (hi[k] - lo[k]) * i / (n - 1)) for k in range(3)) for i in range(n)]


def recolor(fig):
    """Collapse every trace to one hue so exhibits share a single palette.

    Executive documents read as one system when data carries exactly one
    color: single series get the accent, multi-series get sequential shades
    of it, dashed reference lines stay gray, heatmaps get a monochrome scale.
    """
    mono_scale = [[0, "#EDF2F7"], [1, "#1F3A5F"]]
    is_ref = lambda t: getattr(getattr(t, "line", None), "dash", None) in ("dash", "dot", "dashdot")
    shades = ramp(len([t for t in fig.data if not is_ref(t)]))
    i = 0
    for t in fig.data:
        if t.type == "heatmap":
            t.colorscale = mono_scale
            continue
        if is_ref(t):
            t.line.color = GRAY
            continue
        c = shades[i]; i += 1
        if hasattr(t, "marker") and t.marker is not None:
            t.marker.color = c  # also overrides per-point palette arrays
            if getattr(t.marker, "line", None) is not None and t.marker.line.color is not None:
                t.marker.line.color = c
        if hasattr(t, "line") and t.line is not None:
            t.line.color = c
    fig.update_layout(colorway=[ACCENT])


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
            recolor(fig)
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
