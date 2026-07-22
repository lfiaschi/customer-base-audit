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
FONT = "Helvetica Neue, Arial, sans-serif"
INK = "#1A2332"     # primary text
MUTED = "#4A5568"   # secondary text (axis titles, ticks, legend, chart title)
GRID = "#E8EDF3"
AXIS = "#CBD5E0"


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
    Color follows the entity: series repeated across subplot panels keep one
    shade per name; one-trace-per-panel small multiples are a single entity,
    so every panel wears the accent.
    """
    mono_scale = [[0, "#EDF2F7"], [1, "#1F3A5F"]]
    is_ref = lambda t: getattr(getattr(t, "line", None), "dash", None) in ("dash", "dot", "dashdot")
    main = [t for t in fig.data if not is_ref(t) and t.type != "heatmap"]

    names = list(dict.fromkeys(t.name for t in main if t.name))
    panels = {(t.xaxis or "x", t.yaxis or "y") for t in main}
    if 2 <= len(names) < len(main):
        by_name = dict(zip(names, ramp(len(names))))
        color_of = lambda t, i: by_name.get(t.name, ACCENT)
    elif len(panels) == len(main):
        color_of = lambda t, i: ACCENT
    else:
        shades = ramp(len(main))
        color_of = lambda t, i: shades[i]

    i = 0
    for t in fig.data:
        if t.type == "heatmap":
            t.colorscale = mono_scale
            continue
        if is_ref(t):
            t.line.color = GRAY
            continue
        c = color_of(t, i); i += 1
        if hasattr(t, "marker") and t.marker is not None:
            t.marker.color = c  # also overrides per-point palette arrays
            if t.type == "bar":
                t.marker.line = dict(color="white", width=1)  # surface gap between fills
            elif getattr(t.marker, "line", None) is not None and t.marker.line.color is not None:
                t.marker.line.color = c
        if hasattr(t, "line") and t.line is not None:
            t.line.color = c
    fig.update_layout(colorway=[ACCENT])


def style(fig):
    """Publication typography and recessive scaffolding, sized for 1200px width.

    Lens agents chart with library defaults (12px text, prominent grids);
    an executive exhibit needs consistent, larger type and a grid that
    recedes behind the data. Text wears ink/gray, never series colors.
    The chart's own title stays descriptive and secondary — the action
    title in the document carries the message.
    """
    fig.update_layout(
        font=dict(family=FONT, size=17, color=INK),
        title=dict(font=dict(family=FONT, size=20, color=MUTED)),
        legend=dict(font=dict(size=15, color=MUTED), borderwidth=0, bgcolor="rgba(0,0,0,0)",
                    title_font=dict(size=15, color=MUTED)),
        margin=dict(l=80, r=40, t=100, b=70),
        paper_bgcolor="white", plot_bgcolor="white",
    )
    axis_kw = dict(gridcolor=GRID, zeroline=False, linecolor=AXIS, showline=True,
                   ticks="outside", tickcolor=AXIS,
                   title_font=dict(size=16, color=MUTED), tickfont=dict(size=15, color=MUTED))
    fig.update_xaxes(**axis_kw)
    fig.update_yaxes(**axis_kw)
    for a in fig.layout.annotations or ():  # panel titles, callouts
        size = (a.font.size if a.font and a.font.size else 13)
        a.font = dict(family=FONT, size=max(size, 16), color=a.font.color if a.font and a.font.color else MUTED)
    for t in fig.data:
        if t.type == "scatter" and getattr(t, "line", None) is not None:
            t.line.width = max(t.line.width or 2, 3)
        if t.type == "scatter" and getattr(t, "marker", None) is not None and t.marker.size is not None:
            t.marker.size = max(t.marker.size, 8)
        if getattr(t, "textposition", None) is not None and t.type == "bar":
            t.textfont = dict(size=14, color=MUTED)


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
            style(fig)
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
