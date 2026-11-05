"""Contracts for the visual learning layer; graphs must remain computed by backend."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent.parent
JS=(ROOT/'ml_universe/static/visual_story.js').read_text(encoding='utf-8')
CSS=(ROOT/'ml_universe/static/visual_story.css').read_text(encoding='utf-8')
APP=(ROOT/'ml_universe/static/app.js').read_text(encoding='utf-8')
HTML=(ROOT/'ml_universe/static/index.html').read_text(encoding='utf-8')

TOPICS=[
'regression','losses','regularization_path','optimizer_gallery','schedulers','sweep',
'classification','trees','ensembles','clustering','neuron','activation','neural',
'neural_dynamics','cnn','rnn','nlp','bpe','text_classification','embeddings',
'attention','multihead','decoding','rag','bandits','math','algebra','norms','information'
]

def test_visual_guides_cover_all_curriculum_topics():
    lesson_block=JS.split('const lessons = {',1)[1].split('\n  };',1)[0]
    for topic in TOPICS:
        assert re.search(r'\b'+re.escape(topic)+r': \[',lesson_block), topic

def test_scientific_charts_stay_backend_driven():
    assert 'MLStory.render({charts,page,reg' in APP
    assert 'window.MLStory={render' in JS
    assert "fetch('/api/'" in APP
    assert 'visual_story.js' in HTML and 'visual_story.css' in HTML
    assert "Plotly.react(target,traces,layout,config)" in JS

def test_chart_accessibility_and_contextual_explanation():
    assert "aria-label" in JS
    assert 'visual-brief-title' in JS
    assert "Каждая клетка" in JS
    assert ".visual-hero" in CSS
    assert 'displayModeBar:false' in JS
    assert 'function renderCharts(charts)' in APP  # single authoritative renderer
    assert "view==='surface'" in JS

def test_visualizations_are_meaningful_not_random():
    assert 'classColors' in JS
    assert "layout.yaxis.autorange='reversed'" in JS
    assert 'trace.colorscale=sequential' in JS
    assert 'layout.yaxis.scaleanchor=' in JS
    assert 'const needs3d=traces.some(isSurface)' in JS


def test_optimizer_arena_uses_one_switchable_2d_3d_trajectory_view():
    assert "page==='optimizer_gallery' && charts.length>=3" in JS
    assert "index:chosen,kind:'hero',note:0,toggle:true" in JS
