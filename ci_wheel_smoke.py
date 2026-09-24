from __future__ import annotations

import argparse
import importlib
import importlib.machinery
import importlib.metadata
import sys
import sysconfig


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("expected_version")
    parser.add_argument(
        "--require-free-threaded",
        action="store_true",
    )
    args = parser.parse_args()

    if args.require_free_threaded:
        if sysconfig.get_config_var("Py_GIL_DISABLED") != 1:
            raise AssertionError(
                "Expected a CPython free-threaded build"
            )

    if importlib.metadata.version("pyalsaaudio") != args.expected_version:
        raise AssertionError(
            "Installed distribution version mismatch"
        )

    import alsaaudio

    native = importlib.import_module("alsaaudio._alsaaudio")

    native_path = str(native.__file__)

    if not any(
        native_path.endswith(suffix)
        for suffix in importlib.machinery.EXTENSION_SUFFIXES
    ):
        raise AssertionError(
            f"Native extension path has unexpected suffix: {native_path}"
        )

    if not isinstance(alsaaudio.PCM_PLAYBACK, int):
        raise AssertionError("PCM_PLAYBACK is not an int")

    if not isinstance(alsaaudio.PCM_CAPTURE, int):
        raise AssertionError("PCM_CAPTURE is not an int")

    alsa_version = alsaaudio.asoundlib_version()

    if not isinstance(alsa_version, str) or not alsa_version:
        raise AssertionError(
            f"Unexpected ALSA library version: {alsa_version!r}"
        )

    card_indexes = alsaaudio.card_indexes()

    if not isinstance(card_indexes, list):
        raise AssertionError(
            f"card_indexes() did not return a list: {card_indexes!r}"
        )

    print("pyalsaaudio installed native-wheel smoke-test OK")
    print("Installed from:", alsaaudio.__file__)
    print("Native extension:", native_path)
    print("Distribution version:", args.expected_version)
    print("ALSA library version:", alsa_version)
    print("Python:", sys.version)
    print("Platform:", sys.platform)


if __name__ == "__main__":
    main()
