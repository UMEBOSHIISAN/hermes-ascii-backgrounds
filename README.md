# hermes-ascii-aquarium

A skin for [Hermes Agent](https://github.com/NousResearch/hermes-agent) Desktop:
ASCII-art whales, jellyfish, an octopus, a turtle and little fish swimming
through a deep-sea backdrop, with matrix-style ASCII rain falling behind them.

Hermes Desktop のチャット画面の背景に、アスキーアートのクジラ・クラゲ・小魚が
泳ぐ海と、マトリックス風の文字の雨を表示するスキンです。

![preview](preview.png)

*(static preview — in the app everything swims, drifts and falls)*

## Install

Requires Python 3 (standard library only) and Hermes Desktop.

```sh
git clone https://github.com/UMEBOSHIISAN/hermes-ascii-aquarium.git
cd hermes-ascii-aquarium
python3 build_aquarium.py               # writes ~/.hermes/skins/ascii-aquarium.yaml
hermes config set display.skin ascii-aquarium
```

Then quit and relaunch Hermes Desktop (a restart is needed to pick up the skin).
If you use a custom `HERMES_HOME`, the script writes there instead.

## Customize

Edit `build_aquarium.py` and run it again:

- `ART` — the ASCII art for each creature
- `SCENE` — which creatures appear, their position, color, size, speed and direction
- `rain()` — number of rain columns and the characters that fall
- colors at the top of the file

Hermes caps `customCSS` at 32 KiB; the script stops with a message if the scene
gets too big (remove some creatures or rain columns).

## How it works

Hermes skins can carry a `customCSS` field, which Hermes Desktop injects as a
`<style>` tag. The script renders the aquarium as an animated SVG (SMIL) and
puts it behind the chat as a background image — no changes to Hermes itself.

The SVG is embedded as a URL-encoded `data:` URL. Note that a backslash inside a
CSS string is an escape character, so ASCII art containing `\` must be encoded
as `%5C` or the image silently fails to load. A copy is also written next to
the skin and referenced via `file://` as a fallback.

The creatures are drawn faintly and sit behind the messages, so chat text stays
readable. Clicks pass through to the app.

## Uninstall

```sh
hermes config set display.skin default
rm ~/.hermes/skins/ascii-aquarium.yaml
rm -r ~/.hermes/skins/assets/ascii-aquarium
```

## License

MIT
