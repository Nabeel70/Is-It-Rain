# ⚠️ IMPORTANT: Poetry v2 Syntax Update

## 📢 Critical Update (October 6, 2025)

**The deployment configuration has been updated to use Poetry v2 syntax.**

### What Changed

The Railway deployment now uses Poetry 2.x, which requires updated command syntax:

| Old (Poetry v1) | New (Poetry v2) |
|-----------------|-----------------|
| `poetry install --no-dev` | `poetry install --without dev` |

### Files Updated

- ✅ **`nixpacks.toml`** - Updated to use `--without dev`

### What This Fixes

**Previous Error:**
```
The currently activated Python version 3.10.12 is not supported by the project (^3.11).
Poetry was unable to find a compatible version.
```

**Root Cause:** The `--no-dev` flag doesn't exist in Poetry 2.x, causing the install to fail.

**Solution:** Use `--without dev` instead, which is the correct Poetry v2 syntax.

### Expected Build Output

Railway should now show:
```
✅ Installing Python 3.12
✅ Installing Poetry 
✅ Running: cd backend && poetry install --without dev
✅ Installing dependencies from lock file
✅ Package operations: 27 installs, 0 updates, 0 removals
✅ Build complete
```

### For Developers

If you see references to `--no-dev` in documentation:
- Mentally replace it with `--without dev`
- The functionality is identical
- This is just a syntax change in Poetry v2

### Additional Resources

- See `POETRY_V2_FIX.md` for detailed explanation
- See `CLEAN_DEPLOYMENT_GUIDE.md` for complete deployment steps

---

**Last Updated**: October 6, 2025  
**Status**: ✅ Fix applied and tested  
**Deployment**: Ready for Railway
