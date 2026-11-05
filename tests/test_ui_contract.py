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


def test_distraction_free_ui_has_no_file_controls_or_decorative_modebar():
    # File import/export lives in the backwards-compatible Python API, not the learning UI.
    for unwanted in ('id="csvButton"', 'id="csvInput"', 'id="loadInput"', 'id="saveButton"', 'id="loadButton"'):
        assert unwanted not in HTML
    assert '<input type="file"' not in HTML
    assert 'saveFile(' not in JS and 'loadCsv(' not in JS
    assert 'toImageButtonOptions' not in JS
    assert 'modeBarButtons:[buttons]' in JS
    assert "['zoomIn2d','zoomOut2d','resetScale2d']" in JS
    assert "['zoom3d','resetCameraDefault3d']" in JS
    assert 'id="renderTime"' not in HTML


def test_parameters_are_opt_in_modules_in_every_topic():
    assert 'id="inspectorPanel"' in HTML
    assert 'id="addModuleButton"' in HTML
    assert 'id="modulePicker"' in HTML
    assert 'const PARAM_LAYOUT=' in JS
    assert 'validateParameterLayouts();' in JS
    assert "activeModules=new Map()" in JS
    assert 'function removeModule(id)' in JS
    assert 'function relevantField(key)' in JS
    assert "['w','b','lr']" in JS
    assert "['optimizer','Оптимизатор'" in JS
    assert "['regularization','Регуляризация'" in JS
    assert "['attention'" in JS
    assert "['multihead'" in JS
    assert "['rag'" in JS
    assert "showControls();if(page==='regression')resetRegression(true);else runLab();" in JS
    # One workspace per topic, step-through inside the lab, arena only for comparisons.
    assert 'id="modeBar"' not in HTML
    assert 'data-mode=' not in HTML
    assert 'id="runMainButton"' not in HTML
    assert 'id="applyButton"' not in HTML
    assert 'id="paramsFooter"' not in HTML
    assert 'compareRegression(' not in JS
    assert 'changeMode(' not in JS
    assert "['optimizer_gallery'," in JS
    assert 'id="timelineContainer"' in HTML


def test_comparison_endpoint_is_not_duplicated():
    server=(ROOT/'ml_universe/server.py').read_text(encoding='utf-8')
    assert "'/api/compare'" not in server
    assert "from .core.regression import RegressionExperiment,compare" not in server
