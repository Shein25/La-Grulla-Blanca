# Kaggle techniques heavy v0.4 — Git-backed entrypoint

Use `notebooks/KAGGLE_TECH_BALANCE_ALL_ROOTS_HEAVY_V01_2_GIT.ipynb`.

This entrypoint needs no Kaggle Dataset for campaign inputs. It clones the official repository, checks out the pinned asset commit `ac184bf496277eda78493262a1255f245d5c1d97`, reconstructs the input ZIP from five versioned base64 parts, verifies SHA-256 `dd4032c12a574d071411a505565f970473baaa84c17d4302435a9a206938d63b`, verifies the internal manifest, and only then starts the campaign.

Kaggle Internet must be enabled.

For a full run set:

```python
RESUME = True
RUN_MODE = "FULL_CAMPAIGN"
```

A Kaggle Input is only needed later if you want to restore a downloaded `TECHNIQUES_HEAVY_CHECKPOINT.zip`.
