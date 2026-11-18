"""Small contract tests for the template.

These tests intentionally cover only the template's public starting points.
Add plugin-specific tests beside this file as the implementation grows.
"""

import json
from pathlib import Path
from types import SimpleNamespace

import OlivOSPluginTemplate.main as template


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / 'OlivOSPluginTemplate'
NAMESPACE = 'OlivOSPluginTemplate'


class FakeEvent:
    def __init__(self):
        self.base_info = {'self_id': 10001}
        self.data = SimpleNamespace(
            message='/bot',
            sender={'name': 'tester'},
            target_id=10001,
            user_id=20002,
            group_id=-1,
        )
        self.replies = []
        self.sent = []

    def reply(self, text):
        self.replies.append(text)

    def send(self, send_type, target_id, payload):
        self.sent.append((send_type, target_id, payload))


def test_manifest_exposes_namespace_and_single_webui_page():
    manifest = json.loads((PLUGIN_ROOT / 'app.json').read_text(encoding='utf-8'))
    assert manifest['namespace'] == NAMESPACE
    assert manifest['message_mode'] == 'olivos_string'
    assert manifest['support']
    pages = manifest['webui_config']
    assert len(pages) == 1
    assert pages[0]['type'] == 'iframe'
    assert pages[0]['path'] == 'webui/index.html'
    assert manifest['menu_config']
    assert {path.name for path in (PLUGIN_ROOT / 'webui').iterdir()} == {'index.html'}


def test_event_contract_exposes_common_callbacks():
    for name in ('init', 'init_after', 'private_message', 'group_message', 'poke', 'save', 'menu'):
        assert callable(getattr(template.Event, name, None))


def test_unity_reply_example_answers_bot_command():
    event = FakeEvent()
    template.Event.group_message(event, None)
    assert event.replies == [NAMESPACE]


def test_webui_bridge_example_round_trips_text():
    event = FakeEvent()
    event.data.namespace = NAMESPACE
    event.data.event = f'{NAMESPACE}_WebUI_Echo'
    event.data.payload = {'text': 'hello'}
    event.data.webui = {'request_id': 'request-1'}

    template.Event.menu(event, None)

    assert event.sent == [
        ('webui', 'request-1', {'ok': True, 'text': 'hello', 'plugin': template.gPluginName})
    ]


def test_webui_page_is_self_contained():
    page = (PLUGIN_ROOT / 'webui' / 'index.html').read_text(encoding='utf-8')
    assert 'olivos:plugin_event' in page
    assert 'window.parent.postMessage' in page
    for forbidden in ('fetch(', 'WebSocket', 'localStorage'):
        assert forbidden not in page
