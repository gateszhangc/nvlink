#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
  if len(sys.argv) != 4:
    raise SystemExit("usage: sync_kustomize_image_tag.py <kustomization> <image_name> <new_tag>")

  kustomization_path = Path(sys.argv[1])
  image_name = sys.argv[2]
  new_tag = sys.argv[3]

  lines = kustomization_path.read_text().splitlines()
  rendered: list[str] = []
  in_images = False
  matched_name = False
  updated = False

  for line in lines:
    stripped = line.strip()
    if stripped == "images:":
      in_images = True
    elif in_images and stripped.startswith("- name:"):
      matched_name = stripped.split(":", 1)[1].strip() == image_name
    elif in_images and matched_name and stripped.startswith("newTag:"):
      indent = line[: len(line) - len(line.lstrip())]
      rendered.append(f"{indent}newTag: {new_tag}")
      updated = True
      matched_name = False
      continue
    elif in_images and stripped and not line.startswith(" "):
      in_images = False
      matched_name = False

    rendered.append(line)

  if not updated:
    raise SystemExit(f"Could not find a newTag entry for image '{image_name}' in {kustomization_path}")

  kustomization_path.write_text("\n".join(rendered) + "\n")


if __name__ == "__main__":
  main()

