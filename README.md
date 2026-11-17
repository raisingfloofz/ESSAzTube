# ESSAzTube — Featured Edition

Free static GitHub Pages app featuring 12 approved ESSA YouTube channels. No YouTube API key or billing required.

## Upload to GitHub

1. Upload `index.html`, `videos.json`, `scripts/update_videos.py`, and `.github/workflows/update-videos.yml` **preserving the folder structure**. Put your existing `ESSAzTube.Icon.png` beside `index.html` (the icon is not included in this package).
2. In repository **Settings → Pages**, choose **Deploy from a branch**, your default branch, and **/(root)**.
3. Under **Actions**, select **Update Featured Videos**, then **Run workflow**. Wait for the workflow to finish and for GitHub Pages to deploy the updated `videos.json`.
4. The workflow checks every six hours (GitHub may delay or skip scheduled runs). You can manually run it at any time.
5. If the workflow can't commit, check **Settings → Actions → General → Workflow permissions** and allow read/write permissions, or use a repository policy that permits the workflow's `contents: write` permission.

## Important limitations

- Channel ID lookup parses public YouTube pages. YouTube can change page markup or block automated requests. Check the Actions logs for `UNRESOLVED channel` messages. Successfully resolved channels are saved for subsequent runs.
- The public RSS feed contains only a small number of recent uploads. Historical videos are retained as they're discovered, up to 500 total.
- YouTube feeds do not reliably label Shorts, provide video duration, or offer a dependable transcript search. This version deliberately has one mixed Featured feed, not an unreliable Shorts split.
- Videos must allow embedding. YouTube may show advertisements, and the embedded player retains its own controls. The app's Browse button resizes the surrounding player and shows a recommendation list; tapping inside the YouTube iframe itself cannot reliably trigger the app because of browser cross-origin restrictions.
- YouTube may change or discontinue public feeds; automatic updates are best effort, not guaranteed.
- Public GitHub Actions and GitHub Pages have usage limits and terms. The setup is designed to stay within typical free usage, not an unconditional guarantee of free service.

## Adding or removing creators

Edit the `HANDLES` lists in both `index.html` and `scripts/update_videos.py`. Only list creators who have agreed to be Featured.
