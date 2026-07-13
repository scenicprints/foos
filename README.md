# Octo

A clean, full-screen **Android WebView for GitHub** — like a dedicated GitHub
app, but it's just the mobile site wrapped nicely, with the same in-app OTA
updater as BodyComp and Pantry.

- Opens straight to `github.com`; you sign in once and it stays signed in.
- Chromeless — no app bar, GitHub's own UI fills the screen.
- Android **back button** navigates the WebView back.
- **Pull down** to refresh.
- `mailto:` / `tel:` links and file downloads (release assets, `.zip`, `.apk`,
  …) hand off to your real browser / mail app so they behave correctly.
- **File uploads work** — GitHub attachment forms (issue/PR attachments, avatar,
  gist files) open the system file picker; images-only forms filter to images.
- **Updates:** on launch it quietly checks the latest GitHub Release. If a newer
  build exists, a slim banner slides in at the top — tap it to install.
  No banner = no chrome. To check manually anytime, **long-press the very top
  edge** of the screen to open the update sheet.

Package `com.scenicprints.octo` · Flutter 3.44.2 · Android only.

## First-time setup (once)

1. **Create the GitHub repo** `scenicprints/octo` (public, so the updater can
   read Releases without a token), then point this folder at it:
   ```powershell
   git init
   git add -A
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/scenicprints/octo.git
   git push -u origin main
   ```

2. **Generate the signing key** (fresh keystore, dedicated to Octo):
   ```powershell
   .\scripts\setup-signing.ps1
   ```
   It creates `android/app/upload-keystore.jks`, writes `android/key.properties`
   for local signed builds, and prints the four secrets to add to the repo.
   **Back up the `.jks` and its password** — it's irreplaceable.

3. **Add the four secrets** to `scenicprints/octo` →
   *Settings → Secrets and variables → Actions*:
   `KEYSTORE_BASE64`, `STORE_PASSWORD`, `KEY_PASSWORD`, `KEY_ALIAS`
   (the setup script prints all four). Then delete
   `scripts/keystore.base64.txt`.

## Releasing an update

```powershell
.\publish.ps1               # prompts for version + "what's new"
```

This bumps `pubspec.yaml`, tags `v<version>`, and pushes — GitHub Actions builds
the signed APK and publishes it as a Release. Your phone picks it up on next
launch (banner) or via long-press → **Check**.

## Regenerating the launcher icon

```powershell
python scratchpad/gen_icon.py
dart run flutter_launcher_icons
```
