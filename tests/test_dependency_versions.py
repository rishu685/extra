from __future__ import annotations

import tomllib
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_POETRY_LOCK = _REPO_ROOT / "poetry.lock"

# pyasn1 is pulled in transitively (google-auth -> pyasn1-modules -> pyasn1).
# Versions below 0.6.5 are affected by GHSA-mm57-4v3p-rchx,
# GHSA-9m75-vc3g-4x39, GHSA-fm9c-5rcf-2q5p, and GHSA-2qm8-x737-gmw5, so the
# resolved lockfile version must be at least the fixed release.
_PYASN1_FIXED_VERSION = (0, 6, 5)


def _version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split("."))


def _locked_version(package_name: str) -> tuple[int, ...]:
    with _POETRY_LOCK.open("rb") as fh:
        lock = tomllib.load(fh)
    for package in lock["package"]:
        if package["name"] == package_name:
            return _version_tuple(package["version"])
    raise AssertionError(f"{package_name} not present in poetry.lock")


def test_pyasn1_locked_at_cve_fixed_version() -> None:
    assert _locked_version("pyasn1") >= _PYASN1_FIXED_VERSION
