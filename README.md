tmux-fzf-url
============

Open URLs in the current pane with fzf.

Prerequisites
-------------

- [tmux][tmux] 3.3+ for popup support
- [fzf][fzf] 0.53.0+ for `--tmux` option

[tmux]: https://github.com/tmux/tmux
[fzf]: https://github.com/junegunn/fzf

Installation
------------

### Using [TPM](https://github.com/tmux-plugins/tpm)

Add this line to your tmux config file, then hit `prefix + I`:

```sh
set -g @plugin 'aruruu-chan/fzf-urlpy'
```

Usage
-----

Press `PREFIX` + `u`.

Customization
-------------

```sh
# Bind-key (default: 'u')
set -g @fzf-urlpy-bind 'u'
```
