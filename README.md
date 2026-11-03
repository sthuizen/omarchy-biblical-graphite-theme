# Biblical Graphite

A clone of the laptop's Starship theme with 20 grayscale biblical wallpapers from sthuizen's Quattro Sunset collection, source commit a0d5fd80bea51c11a9df70e02cb28c0ce3329608.

The Starship interface palette is preserved. The artwork uses Rec.709 luminance grayscale with gentle sigmoidal contrast (2.5x45%). No blur, rescaling or spatial filtering changes the original outlines. All wallpapers remain 1536 × 1024. The original colours and files remain in the source repository.

Omarchy 4.5.0rc3-1 and its contributors supplied the Starship theme; its MIT notice is preserved in licenses/Omarchy-MIT.txt. The original artwork licence is preserved in LICENSE. wallpapers.json records source and output SHA-256 checksums. previews/wallpaper-gallery.jpg shows the full collection.

Install with `omarchy theme install https://github.com/sthuizen/omarchy-biblical-graphite-theme.git`, then run `omarchy theme set biblical-graphite`. Use `omarchy theme bg next` to cycle the 20 wallpapers. Return with `omarchy theme set starship`.

tools/build-original.py reproduces the artwork using explicit source and output directories (`--source` and `--output`). It creates a fresh output directory and refuses to overwrite an existing one. Python 3, ImageMagick and Fontconfig are required.

## Automatic rotation

Run `bash scripts/install-rotation.sh` to install a user timer and theme-change hook. While Biblical Graphite is active, the wallpaper advances in catalogue order every 30 minutes and wraps after number 20. Activating the theme starts a fresh 30-minute interval; switching away stops the timer. The timer also starts with the graphical session after login. Each automatic change starts a fresh full interval.

To disable automatic changes, run `systemctl --user disable --now biblical-graphite-wallpaper-rotation.timer` and remove `~/.config/omarchy/hooks/theme-set.d/50-biblical-graphite-rotation`.


## Manual GitHub sync

The installed `~/.config/omarchy/themes/biblical-graphite` points to the working checkout, so theme files have one editable source. GitHub syncing is manual: there is no background sync timer or periodic network access. Sync changes when completing theme edits, and reapply the theme after editing settings to refresh the desktop's staged copy.

The manual helper fetches GitHub updates, fast-forwards a clean checkout, commits changes to already tracked files, pushes them and checks the remote commit. New files need `git add <file>` once before they can be included. It stops on conflicting local/remote changes instead of overwriting either copy. GitHub authentication must be available to the Git credential helper; the script contains no credentials.

For a manual sync, run `bash scripts/sync-github.sh` from the checkout. The source, all 20 wallpapers, previews, licences, rotation units and generation script are versioned. No release binaries are required.

![All 20 grayscale wallpapers](previews/wallpaper-gallery.jpg)
