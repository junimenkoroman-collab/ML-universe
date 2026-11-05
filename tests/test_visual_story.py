"""Semantics of the shared visual narrative, independent from Python math tests."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIS = (ROOT / 'ml_universe/static/visual_story.js').read_text(encoding='utf-8')
CSS = (ROOT / 'ml_universe/static/visual_story.css').read_text(encoding='utf-8')
HTML = (ROOT / 'ml_universe/static/index.html').read_text(encoding='utf-8')
APP = (ROOT / 'ml_universe/static/app.js').read_text(encoding='utf-8')


def test_visual_renderer_is_loaded_before_main_and_integrated():
    assert HTML.index('/visual_story.js') < HTML.index('/app.js')
    assert '/visual_story.css' in HTML
    assert 'window.MLStory.render' in APP
    assert 'displayModeBar:false' in VIS


def test_narrative_and_semantics_are_explicit():
    for name in ('regression', 'losses', 'classification', 'trees', 'clustering',
                 'attention', 'multihead', 'rag', 'bandits', 'information'):
        assert f'{name}:' in VIS
    assert 'visual-brief' in VIS
    assert 'visual-hero' in CSS
    assert "['contour','2D']" in VIS
    assert "['surface','3D']" in VIS
    assert 'Разобрать' not in HTML


def test_chart_controls_are_minimal():
    assert "['in','+','Приблизить']" in VIS
    assert "['out','−','Отдалить']" in VIS
    assert "['reset','↺','Вернуть исходный масштаб']" in VIS
    assert 'modeBarButtons' not in VIS
