#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
import shlex
from shutil import which

def executable(*commands):
    """Return the first command that exists on the system."""
    for cmd in commands:
        if which(cmd.split()[0]):
            return cmd
    return None

def halt(message: str):
    """Display a message in tmux and exit."""
    subprocess.run(["tmux", "display-message", message])
    sys.exit(0)

def extract_urls(text: str):
    """Extract URLs (http, https, file) from a string."""
    import re
    pattern = re.compile(
        r"(?:https?|file)://[-a-zA-Z0-9@:%_+.~#?&/=]*[-a-zA-Z0-9@%_+.~#?&/=!]"
    )
    return pattern.findall(text)

def with_fzf(options, lines):
    """Run fzf with the given options and feed it lines."""
    proc = subprocess.Popen(
        ["fzf"] + options,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    stdout, _ = proc.communicate(input="\n".join(lines))
    return stdout.splitlines()

# --- Main Script ---

# Capture tmux pane
try:
    pane_content = subprocess.check_output(
        ["tmux", "capture-pane", "-J", "-p", "-S", "-99999"],
        text=True
    )
except subprocess.CalledProcessError:
    halt("Failed to capture tmux pane")

# Extract URLs
urls = []
for line in pane_content.splitlines():
    line = line.strip()
    if line:
        urls.extend(extract_urls(line))
urls = list(dict.fromkeys(reversed(urls)))  # reverse & remove duplicates

if not urls:
    halt("No URLs found")

header = "Press CTRL-Y to copy URL to clipboard"

# Get tmux client size
dims = subprocess.check_output(
    ["tmux", "display-message", "-p", "#{client_width} #{client_height}"],
    text=True
).split()
width, height = map(int, dims)

# Compute fzf size
max_len = max(len(header), *(len(u) for u in urls)) + 8
rows = len(urls) + 7
cols = min(max_len, width)
rows = min(rows, height)
size_option = f"{cols},{rows}"

fzf_options = [
    "--tmux", size_option,
    "--multi", "--no-margin", "--no-padding", "--wrap",
    "--expect", "ctrl-y",
    "--style", "default",
    "--header", header,
    "--header-border", "top",
    "--highlight-line", "--header-first",
    "--info", "inline-right",
    "--padding", "1,1,0,1",
    "--border-label", " URLs "
]

selected = with_fzf(fzf_options, urls)
if not selected:
    sys.exit(0)

if selected[0] == "ctrl-y":
    # Copy to clipboard using xclip
    copier = executable("xclip -selection clipboard")
    if not copier:
        halt("xclip not found")
    subprocess.run(shlex.split(copier), input="\n".join(selected[1:]), text=True)
    halt("Copied to clipboard")

# Open URLs
opener = executable("xdg-open", "open")
if not opener:
    halt("No command to open URL")
for url in selected[1:]:
    subprocess.Popen(shlex.split(opener) + [url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

