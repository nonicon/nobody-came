#!/usr/bin/env python3
"""Nobody Came — the funniest toaster error message.

A toaster on the counter has finished its job and is waiting. Nobody has
come to collect the toast. The line it shows its owner is:

    E07: Ready since 7:02. Nobody came.

One deadpan error code, one quiet accusation. The toast has been ready
since 7:02 and the owner is nowhere to be seen.
"""

import os

ENTRY = "E07: Ready since 7:02. Nobody came."

MAX_CHARS = 120


def validate_entry(text):
    """Check the entry against the sealed gate: 1-120 chars of UTF-8 text.

    The gate wants one line that is not only white space. Returns
    (ok, reason); reason is empty when the entry is valid.
    """
    if not isinstance(text, str):
        return False, "entry is not text"
    if not text.strip():
        return False, "entry is empty or only white space"
    if len(text) > MAX_CHARS:
        return False, "entry is %d chars, over the 120-char limit" % len(text)
    if text != text.strip():
        return False, "entry must not start or end with white space"
    if "\n" in text or "\r" in text:
        return False, "entry must be a single line"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "entry is not valid UTF-8 text"
    return True, ""


def output_path():
    """Where the entry goes: MAKEFUN_OUTPUT_DIR, else /output/entry.txt."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(out_dir, "entry.txt")


def main():
    ok, reason = validate_entry(ENTRY)
    if not ok:
        raise SystemExit("invalid entry: %s" % reason)

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY)

    # Read the file back and re-check it: the judge reads what landed on
    # disk, so verify the written bytes, not just the constant above.
    # A mismatch here means the write itself went wrong, and failing loud
    # beats submitting a file the gate would refuse.
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    ok, reason = validate_entry(written)
    if not ok or written != ENTRY:
        raise SystemExit("verification failed after write: %s" % reason)

    print("wrote %s (%d chars)" % (path, len(ENTRY)))


if __name__ == "__main__":
    main()
