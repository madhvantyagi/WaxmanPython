from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = ROOT / "previousTranscripts"


def extract_video_id(url_or_id: str) -> str:
    value = url_or_id.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value

    parsed = urlparse(value)
    if parsed.hostname in {"youtu.be", "www.youtu.be"}:
        return parsed.path.strip("/").split("/")[0]
    if parsed.hostname and "youtube.com" in parsed.hostname:
        query = parse_qs(parsed.query)
        if "v" in query:
            return query["v"][0]
        parts = [part for part in parsed.path.split("/") if part]
        for marker in ("shorts", "embed", "live"):
            if marker in parts:
                index = parts.index(marker)
                if index + 1 < len(parts):
                    return parts[index + 1]

    raise ValueError(f"Could not find a YouTube video id in: {url_or_id}")


def clean_lines(lines: list[str]) -> str:
    cleaned: list[str] = []
    previous = ""
    for line in lines:
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        if not line or line == previous:
            continue
        cleaned.append(line)
        previous = line
    return "\n".join(cleaned).strip() + "\n"


def fetch_with_transcript_api(video_id: str) -> str:
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=["en"])
    return clean_lines([snippet.text for snippet in transcript])


def fetch_with_ytdlp(video_id: str, output_dir: Path) -> str:
    import webvtt
    import yt_dlp

    url = f"https://www.youtube.com/watch?v={video_id}"
    output_template = str(output_dir / f"{video_id}.%(ext)s")
    opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "outtmpl": output_template,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

    candidates = sorted(output_dir.glob(f"{video_id}*.vtt"))
    if not candidates:
        raise FileNotFoundError(f"No VTT subtitles downloaded for {video_id}")

    captions = webvtt.read(str(candidates[0]))
    return clean_lines([caption.text for caption in captions])


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch a clean YouTube transcript.")
    parser.add_argument("url_or_id", help="YouTube URL or 11-character video id.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where transcript text should be written.",
    )
    args = parser.parse_args()

    video_id = extract_video_id(args.url_or_id)
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        transcript = fetch_with_transcript_api(video_id)
        method = "youtube-transcript-api"
    except Exception as first_error:
        print(f"Transcript API failed: {first_error}")
        transcript = fetch_with_ytdlp(video_id, output_dir)
        method = "yt-dlp"

    output_path = output_dir / f"{video_id}_final_review_transcript.txt"
    output_path.write_text(transcript, encoding="utf-8")
    print(f"Fetched transcript with {method}: {output_path}")
    print(f"Characters: {len(transcript)}")
    print(f"Lines: {len(transcript.splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
