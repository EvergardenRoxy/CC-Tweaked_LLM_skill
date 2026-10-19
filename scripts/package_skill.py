#!/usr/bin/env python3
"""Build and verify the portable active skill pack; no archives or audit inputs."""
import hashlib
import pathlib
import zipfile
from validate_skill import ROOT, check_structure


def main():
    if not check_structure():
        raise SystemExit('Invalid active skill structure')
    root = ROOT / 'skills/minecraft-cc-tweaked'
    files = [root / 'SKILL.md', *sorted((root / 'references').glob('*.md'))]
    target = ROOT / 'CCT_prompt_pack.zip'
    staged = target.with_suffix('.zip.tmp')
    try:
        with zipfile.ZipFile(staged, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                archive.writestr(str(path.relative_to(root)), path.read_bytes())
        with zipfile.ZipFile(staged) as archive:
            expected = {str(path.relative_to(root)): path.read_bytes() for path in files}
            assert set(archive.namelist()) == set(expected)
            assert len(archive.namelist()) == len(expected)
            assert archive.testzip() is None
            for name, content in expected.items():
                assert not pathlib.PurePosixPath(name).is_absolute()
                assert '..' not in pathlib.PurePosixPath(name).parts
                assert archive.read(name) == content
        staged.replace(target)
    finally:
        if staged.exists():
            staged.unlink()
    print(f'PASS: {target.name}: {len(files)} files; source bytes and CRC verified')
    print('SHA-256:', hashlib.sha256(target.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
