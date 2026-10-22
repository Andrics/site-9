# firefox — SITE-9 userChrome.css (BUILD_SPEC.md §3 "Firefox")

Firefox's profile folder has a random name, so stow targets the profile
directly instead of `~`:

```sh
# the profile Firefox uses (Default= under [Install…] in profiles.ini)
grep -A2 '^\[Install' ~/.config/mozilla/firefox/profiles.ini
cd ~/Development/site-9
stow -t ~/.config/mozilla/firefox/<profile> firefox
```

That links `chrome/` (userChrome.css, userContent.css) and `user.js`
into the profile. Restart Firefox to load them. Stow skips this README.

Written against Firefox 158.0.1 (Nova design). It styles Firefox's
internal markup, so recheck after every Firefox update.
