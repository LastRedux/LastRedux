# LastRedux - A modern scrobbler for Last.fm on macOS

[![Screen-Shot-2020-12-26-at-1-15-36-AM.png](https://i.postimg.cc/C5gJ1FM8/Screen-Shot-2020-12-26-at-1-15-36-AM.png)](https://postimg.cc/TLtnNvD2)

# ⚠️ Disclaimer ⚠️ - LastRedux does not work on macOS 13+ and the project is not currently maintained

### Download ⚡️

Download the latest release from the [releases](https://github.com/LastRedux/LastRedux/releases) page

If you can figure out how to build from source, go for it, but you can ask for support in our [Discord server](https://discord.gg/DMCE4kV3kk)

### How to use LastRedux ✨🦄
- Run LastRedux in the background while listening to music
- Generally speaking, restart the app if anything goes wrong
- Tracks will be automatically scrobbled if you use Music.app (Apple Music or local files)
- Switch between media players by using the status bar icon menu
- You can put the app in Mini Mode which hides the sidebar and is optimized for small window sizes

### Keyboard Shortcuts ⌨️

- Cmd-1 focuses the history view
- Cmd-2 focuses the profile view
- Cmd-3 focuses the friends view
- Cmd-J selects the current scrobble in the details view
- Cmd-[ and Cmd-] select the previous and next scrobble
- Cmd-Shift-M toggles mini mode

### Known Issues 🚨

- At this moment, there is no caching of unsubmitted scrobbles if you lose connection or if Last.fm is down
- The app will cease to function if your internet connection is lost. Make sure to restart the app if this occurs
- There is currently no functionality to relaunch the app after shutdown, log out, or restart—you must launch the app manually.
- During setup, the LastRedux window may disappear behind the web browser. Minimize the web browser window or find LastRedux in Mission Control to bring the window back
- If the web browser doesn't open during setup, the URL text can only be copied with Cmd+C. At this moment, a bug prevents the context menu from appearing
- In rare cases, the app fails to launch due to a bug involving connection to Spotify. Simply relaunch the app if this occurs
- On macOS Big Sur, the app icon in the status bar is too small
- Quitting the app requires using the status bar menu

### Known Apple Music Issues 🍎

- Music.app will skip for a second when starting the app or switching the media player to Music.app in some cases
- Sometimes Apple Music send malformed data, which will result in the current song not loading. To fix this, play something in your library, then switch back
- Apple Music radio stations are currently unreliable, and may cause the app to crash
