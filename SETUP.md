# Jatinn07 — GitHub profile README

This package recreates the supplied dashboard composition: split hero, three-column profile panel, activity strip and footer. Visual assets are local to this repository, so the README does not rely on external card images or icon-CDN availability.

## Install

Extract the ZIP into your existing clone:

```bash
cd ~/Code/Jatinn07
unzip -o ~/Downloads/Jatinn07.zip
git add -A
git commit -m "Rebuild GitHub profile dashboard"
git push origin main
```

The archive contains files at its root, not inside an extra nested folder.

## Refresh the contribution calendar

1. Push the package to the `main` branch. The workflow starts automatically because the README, generator and workflow file changed.
2. Open `https://github.com/Jatinn07/Jatinn07/actions`.
3. Select **Refresh profile activity** and check that the run succeeds.
4. Refresh your profile after the action commits the generated SVG.

You can also trigger it manually using **Run workflow**. The workflow updates `assets/activity.svg` using:
- GitHub's public REST profile endpoint for follower/following counts.
- GitHub Contributions API for daily contribution levels.

It runs once daily at 01:23 UTC. The workflow uses `GITHUB_TOKEN` with repository content write permission; no personal access token or secret needs to be created.

If the contribution data provider is temporarily unavailable, the workflow fails rather than generating fake activity. Rerun it later.

## Contact links

Only verified destinations are included: GitHub profile, repositories and the activity section. No email or LinkedIn address has been invented. Provide those exact public URLs later to add them.
