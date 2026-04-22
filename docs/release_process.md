# Release Process

1. Refresh `data/current/` from the validated public collector output.
2. Snapshot the release into `data/releases/<version>/`.
3. Run `python scripts/build_release_metadata.py`.
4. Run `python scripts/validate_release.py --check`.
5. Update `CHANGELOG.md` and tag the release.
