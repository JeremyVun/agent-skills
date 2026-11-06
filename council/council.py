#!/usr/bin/env python3
"""One council round: tiles a game's frames into timestamped contact sheets and has Opus and Sol each review them
blind, as players who know only the game's name.

Usage: council.py <frames-dir> <out-dir> --game NAME [--fps 1] [--note TEXT] [--previous FILE] [--only opus|sol]
Frames are the images in <frames-dir> in name order, taken at a constant --fps of game time.
"""
import argparse
import concurrent.futures
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
OPUS, SOL, EFFORT = 'claude-opus-5-5', 'gpt-6.1-sol', 'high'

args = argparse.ArgumentParser()
args.add_argument('frames')
args.add_argument('out')
args.add_argument('--game', required=True)
args.add_argument('--fps', type=float, default=1)
args.add_argument('--note', default='')
args.add_argument('--previous')
args.add_argument('--only', choices=['opus', 'sol'])
a = args.parse_args()

frames = sorted(p for p in pathlib.Path(a.frames).iterdir() if p.suffix.lower() in ('.jpg', '.jpeg', '.png'))
if not frames:
    sys.exit(f'No frames in {a.frames}')
out = pathlib.Path(a.out).resolve()
(out / 'sheets').mkdir(parents=True, exist_ok=True)


def clock(index):
    seconds = index / a.fps
    whole = int(seconds)
    text = f'{whole // 60}:{whole % 60:02d}'
    return text if a.fps <= 1 else f'{text}.{int((seconds - whole) * 10)}'


with Image.open(frames[0]) as first:
    portrait = first.height > first.width
columns, rows = (6, 2) if portrait else (4, 3)
tile_w, tile_h = (320, 480) if portrait else (480, 300)
font = ImageFont.load_default(size=16)
sheets = []
for start in range(0, len(frames), columns * rows):
    sheet = Image.new('RGB', (columns * tile_w, rows * tile_h))
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(frames[start:start + columns * rows]):
        x, y = i % columns * tile_w, i // columns * tile_h
        with Image.open(path) as frame:
            frame = frame.convert('RGB')
            scale = max(tile_w / frame.width, tile_h / frame.height)
            frame = frame.resize((round(frame.width * scale), round(frame.height * scale)), Image.LANCZOS)
            left, top = (frame.width - tile_w) // 2, (frame.height - tile_h) // 2
            sheet.paste(frame.crop((left, top, left + tile_w, top + tile_h)), (x, y))
        label = clock(start + i)
        box = draw.textbbox((x + 10, y + 8), label, font=font)
        draw.rounded_rectangle((box[0] - 5, box[1] - 3, box[2] + 5, box[3] + 3), 3, fill=(0, 0, 0))
        draw.text((x + 10, y + 8), label, font=font, fill=(255, 255, 255))
        draw.rectangle((x, y, x + tile_w - 1, y + tile_h - 1), outline=(0, 0, 0))
    name = f'sheet-{len(sheets) + 1:02d}.jpg'
    sheet.save(out / 'sheets' / name, quality=88)
    sheets.append(name)
print(f'{len(frames)} frames on {len(sheets)} sheets in {out / "sheets"}')

every = 'one frame for every second' if a.fps == 1 else f'{a.fps:g} frames for every second'
brief = (HERE / 'brief.md').read_text().format(game=a.game, every=every, note=a.note.strip())
if a.previous:
    brief = (f'Before this you played an earlier part of {a.game}. Your own account of it:\n\n'
             f'<earlier>\n{pathlib.Path(a.previous).read_text().strip()}\n</earlier>\n\n{brief}')
listing = f'The contact sheets, in order: {", ".join(sheets)}.'
player = (HERE / 'player.md').read_text()

# An empty folder outside any project, holding only the sheets, so no project instructions or memory reach them.
blind = pathlib.Path(tempfile.mkdtemp(prefix='council-'))
for name in sheets:
    shutil.copy(out / 'sheets' / name, blind / name)
(blind / '.player.md').write_text(player)


def run(command):
    done = subprocess.run(command, cwd=blind, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(f'{command[0]} exited {done.returncode}\n{done.stderr[-4000:]}')
    return done.stdout


def opus():
    return run(['claude', '-p', '--model', OPUS, '--effort', EFFORT, '--system-prompt', player,
                '--setting-sources', 'project', '--tools', 'Read', '--allowedTools', 'Read', '--output-format', 'text',
                f'{brief}\n{listing} They are image files in the current folder; read each one.'])


def sol():
    answer = blind / '.answer.md'
    run(['codex', 'exec', '--skip-git-repo-check', '--ephemeral', '-m', SOL, '-c', f'model_reasoning_effort={EFFORT}',
         '-c', f'model_instructions_file={blind / ".player.md"}', '-s', 'read-only', '-C', str(blind),
         *[f'--image={blind / name}' for name in sheets], '--output-last-message', str(answer),
         '--', f'{brief}\n{listing} They are attached as images in that order.'])
    return answer.read_text()


reviewers = {'opus': opus, 'sol': sol}
names = [a.only] if a.only else list(reviewers)
failed = False
try:
    with concurrent.futures.ThreadPoolExecutor() as pool:
        for name, future in [(n, pool.submit(reviewers[n])) for n in names]:
            try:
                (out / f'{name}.md').write_text(future.result())
                print(f'{name}: {out / f"{name}.md"}')
            except Exception as error:
                failed = True
                print(f'{name} failed: {error}', file=sys.stderr)
finally:
    shutil.rmtree(blind, ignore_errors=True)
sys.exit(1 if failed else 0)
