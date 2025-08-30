# tmux-fzf-url

tmux plugin for opening urls

### 📥 Installation

Prerequisites:
* [`fzf`](https://github.com/junegunn/fzf)
* [`python3`](https://www.python.org/downloads/)

**Install using [TPM](https://github.com/tmux-plugins/tpm)**

Add this line to your tmux config file, then hit `prefix + I`:

``` tmux
set -g @plugin 'aruruu-chan/fzf-urlpy.tmux'
```

**Install manually**

Clone this repo somewhere and source `fzf-urlpy.tmux` at the config file.

### 📝 Usage

The default key-binding is `u`(of course prefix hit is needed), it can be modified by
setting value to `@fzf-url-bind` at the tmux config like this:

``` tmux
set -g @fzf-url-bind 'x'
```

You can also extend the capture groups by defining `@fzf-url-extra-filter`:

``` tmux
# simple example for capturing files like 'abc.txt'
set -g @fzf-url-extra-filter 'grep -oE "\b[a-zA-Z]+\.txt\b"'
```

The plugin default captures the current screen. You can set `history_limit` to capture
the scrollback history:

```tmux
set -g @fzf-url-history-limit '2000'
```

You can use custom fzf options by defining `@fzf-url-fzf-options`.

```
# open tmux-fzf-url in a tmux v3.2+ popup
set -g @fzf-url-fzf-options '-w 50% -h 50% --multi -0 --no-preview --no-border'
```

By default, `tmux-fzf-url` will use `xdg-open`, `open`, or the `BROWSER`
environment variable to open the url, respectively. If you want to use a
different command, you can set `@fzf-url-open` to the command you want to use.

```tmux
set -g @fzf-url-open "firefox"
```

### 💡 Tips

- You can mark multiple urls and open them at once.
