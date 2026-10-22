# sddm — SITE-9 login screen (BUILD_SPEC.md §3 "Login screen")

`site-9/` is an SDDM 0.21 theme for the Qt6 greeter (`QtVersion=6` in
`metadata.desktop`). It isn't stowed: SDDM runs as its own user and reads
themes from `/usr/share/sddm/themes/`, so it's copied there with sudo.

The background isn't in the repo. Make it first (no placard, so no logo):

```sh
cd ~/Development/site-9
python3 wallpaper/tools/make-wallpaper.py --no-placard \
    --out ~/.local/share/site-9/login-background.png
```

Install (run in your own terminal; asks for your password):

```sh
sudo install -d -m 755 /usr/share/sddm/themes/site-9
sudo install -m 644 ~/Development/site-9/sddm/site-9/{Main.qml,metadata.desktop,theme.conf} /usr/share/sddm/themes/site-9/
sudo install -m 644 ~/.local/share/site-9/login-background.png /usr/share/sddm/themes/site-9/background.png
sudo install -d -m 755 /etc/sddm.conf.d
sudo install -m 644 ~/Development/site-9/sddm/site-9.conf /etc/sddm.conf.d/site-9.conf
```

Preview without logging out (a window, can't log in):

```sh
sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/site-9
```

**If the login screen ever breaks:** Ctrl+Alt+F2 → log in on the text
console → `sudo rm /etc/sddm.conf.d/site-9.conf` →
`sudo systemctl restart sddm` (SDDM's default theme comes back). If the
theme's QML fails to load, SDDM falls back to its built-in theme on its
own.
