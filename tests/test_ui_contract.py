"""Cheap offline UI contracts, in addition to the optional Chromium visual smoke."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent
JS=(ROOT/'ml_universe/static/app.js').read_text(encoding='utf-8')
HTML=(ROOT/'ml_universe/static/index.html').read_text(encoding='utf-8')
CSS=(ROOT/'ml_universe/static/app.css').read_text(encoding='utf-8')


def test_curriculum_nav_is_bounded_and_contains_only_seven_stages():
    block=JS.split('const NAV=[',1)[1].split('const allNav=',1)[0]
    assert len(re.findall(r"\['0[1-7] ·",block)) == 7
    for unwanted in ('pca','dbscan','gmm','diffusion','causal','timeseries','recommendations'):
        assert f"['{unwanted}'," not in block
    assert "['bandits'," in block
    assert "['multihead'," in block
    assert "['rag'," in block


def test_light_dark_themes_and_regression_controls():
    assert "id=\"themeButton\"" in HTML
    assert "id=\"timelineContainer\"" in HTML
    assert "id=\"navigation\"" in HTML
    assert "html.light" in CSS or ".light" in CSS
    assert 'ml-universe-theme' in JS
    assert 'SCHEMAS.trees=' in JS and 'SCHEMAS.ensembles=' in JS
