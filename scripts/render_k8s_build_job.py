#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser(description="Render the K8s image build job manifest.")
  parser.add_argument("--template", required=True)
  parser.add_argument("--output", required=True)
  parser.add_argument("--job-name", required=True)
  parser.add_argument("--namespace", required=True)
  parser.add_argument("--app-name", required=True)
  parser.add_argument("--git-secret-name", required=True)
  parser.add_argument("--registry-secret-name", required=True)
  parser.add_argument("--github-repository", required=True)
  parser.add_argument("--git-ref", required=True)
  parser.add_argument("--git-sha", required=True)
  parser.add_argument("--image-repository", required=True)
  parser.add_argument("--image-tag", required=True)
  parser.add_argument("--dockerfile-path", required=True)
  return parser.parse_args()


def main() -> None:
  args = parse_args()
  rendered = Path(args.template).read_text()
  replacements = {
    "JOB_NAME": args.job_name,
    "BUILD_NAMESPACE": args.namespace,
    "APP_NAME": args.app_name,
    "GIT_SECRET_NAME": args.git_secret_name,
    "REGISTRY_SECRET_NAME": args.registry_secret_name,
    "GITHUB_REPOSITORY": args.github_repository,
    "GIT_REF": args.git_ref,
    "GIT_SHA": args.git_sha,
    "IMAGE_REPOSITORY": args.image_repository,
    "IMAGE_TAG": args.image_tag,
    "DOCKERFILE_PATH": args.dockerfile_path
  }

  for key, value in replacements.items():
    rendered = rendered.replace(f"{{{{{key}}}}}", value)

  unresolved = sorted(set(re.findall(r"{{([A-Z0-9_]+)}}", rendered)))
  if unresolved:
    raise SystemExit(f"Unresolved placeholders: {', '.join(unresolved)}")

  Path(args.output).write_text(rendered)


if __name__ == "__main__":
  main()

