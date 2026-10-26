# Contributing a theme 🐾

Thanks for wanting to add something cute! A theme is a single file in `themes/`.

## Steps

1. **Copy the template**
   ```sh
   cp themes/_template.py themes/my_theme.py
   ```
   Set `NAME` (the skin name, e.g. `"my-theme"`) and `DESCRIPTION`.

2. **Draw and place things** — edit `ART` and `SCENE`. Comments in the template explain every field.

3. **Try it in Hermes**
   ```sh
   python3 build.py my-theme
   hermes config set display.skin my-theme
   ```
   Restart Hermes Desktop and look at it with a real conversation on screen.

4. **Make a GIF** for the gallery (needs Google Chrome and ffmpeg):
   ```sh
   python3 tools/make_gif.py my-theme      # -> previews/my-theme.gif
   ```

5. **Open a pull request** with `themes/my_theme.py`, `previews/my-theme.gif`, and a new gallery cell in `README.md`.

## Checklist

- [ ] Only plain ASCII characters in the art (no emoji, no full-width characters)
- [ ] Chat text is still easy to read — keep creature opacity around 0.2–0.5
- [ ] `python3 build.py my-theme` succeeds (it stops if `customCSS` goes over the 32 KiB cap)
- [ ] Your own original art, or art you're allowed to share
- [ ] Cute 🐱

## Tips

- In `ART`, backslashes must be doubled: `"/\\_/\\"` draws `/\_/\`.
- To glue several pieces together (e.g. a rainbow trail behind a cat), give them the same motion, speed and delay, and use `x` to offset them. See the nyan cat in `themes/nyan.py`.
- Too big? Lower `TWINKLES` / `PARTICLES` counts or `RAIN` columns first — they cost the most bytes.
