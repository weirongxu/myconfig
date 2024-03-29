local wezterm = require 'wezterm'

return {
  -- color_scheme = "",
  font = wezterm.font_with_fallback({
    "JetBrainsMono Nerd Font",
    -- "Noto Sans Mono CJK SC",
  }),
  hide_mouse_cursor_when_typing = false,
  warn_about_missing_glyphs=false,
  keys = {
    {key="1", mods="ALT", action={ActivateTab=0}},
    {key="2", mods="ALT", action={ActivateTab=1}},
    {key="3", mods="ALT", action={ActivateTab=2}},
    {key="4", mods="ALT", action={ActivateTab=3}},
    {key="5", mods="ALT", action={ActivateTab=4}},
    {key="6", mods="ALT", action={ActivateTab=5}},
    {key="7", mods="ALT", action={ActivateTab=6}},
    {key="8", mods="ALT", action={ActivateTab=7}},
    {key="9", mods="ALT", action={ActivateTab=8}},
    {key="0", mods="ALT", action="ShowTabNavigator"},
    {key="v", mods="SHIFT|CTRL", action=wezterm.action{PasteFrom="Clipboard"}},
    {key="*", mods="SHIFT|CTRL", action=wezterm.action{PasteFrom="PrimarySelection"}},
    {key="c", mods="SHIFT|CTRL", action=wezterm.action{CopyTo="ClipboardAndPrimarySelection"}},
  },
  font_size = 12,
  line_height = 0.9,
  audible_bell = 'Disabled',
  exit_behavior = 'Close',
  -- use_fancy_tab_bar = false,
  window_padding = {
    left = 0,
    right = 0,
    top = 0,
    bottom = 0,
  },
}
