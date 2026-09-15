"""Resolve relocated patches while preserving paths in captured evidence."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / 'docs/archive/agents-patches'


def resolve_patch_path(value):
    """Accept current paths and missing historical paths from any checkout."""
    path = Path(value)
    if path.is_file():
        return path
    index = json.loads((ARCHIVE / 'paths.json').read_text())
    locations = {entry['original_path']: entry['archived_path'] for entry in index['patches']}
    locations.update({old: index['current_patch'] for old in index.get('previous_current_paths', [])})
    for old, destination in locations.items():
        if path.as_posix() == old or path.as_posix().endswith('/' + old):
            return ROOT / destination
    if not path.is_absolute() and (ROOT / path).is_file():
        return ROOT / path
    return path


def recorded_patch_path(value):
    """Keep the original logical path when regenerating frozen manifests."""
    relative = Path(value).resolve().relative_to(ROOT).as_posix()
    entries = json.loads((ARCHIVE / 'paths.json').read_text())['patches']
    return next((entry['original_path'] for entry in entries
                 if entry['archived_path'] == relative), relative)
