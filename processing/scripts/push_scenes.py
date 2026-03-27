#!/usr/bin/env python3
"""
Narrowlitics: Push Scenes to Server (Run on M5 Mac)

After Gemini indexing, push the scene JSON to the Narrowlitics API on Hetzner.

Usage:
    python push_scenes.py scenes_gemini.json --episode-id 1

What it does:
    1. Reads the Gemini-generated scene JSON file
    2. Sends it to the Narrowlitics API on your Hetzner server
    3. The API stores it in PostgreSQL with vector embeddings
"""
import json
import sys
import argparse
import urllib.request


def push_scenes(json_path: str, episode_id: int, api_url: str) -> None:
    with open(json_path) as f:
        scenes = json.load(f)

    print(f"Pushing {len(scenes)} scenes to {api_url}/api/scenes/episode/{episode_id}/bulk")

    payload = json.dumps({"scenes": scenes}).encode("utf-8")
    req = urllib.request.Request(
        f"{api_url}/api/scenes/episode/{episode_id}/bulk",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print(f"Success! Created {result.get('created', '?')} scenes.")
    except urllib.error.HTTPError as e:
        print(f"API error {e.code}: {e.read().decode()}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        print("Is the Narrowlitics backend running on the server?")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Push Gemini scene data to Narrowlitics API")
    parser.add_argument("json_path", help="Path to Gemini scene JSON file")
    parser.add_argument("--episode-id", type=int, default=1, help="Episode ID in the database")
    parser.add_argument("--api-url", default="https://narrowlitics.capainofindustries.com",
                        help="Narrowlitics API URL")
    args = parser.parse_args()

    push_scenes(args.json_path, args.episode_id, args.api_url)
