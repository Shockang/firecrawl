# Quick Start: Repository Cleanup

This is a quick reference for executing the repository cleanup. For detailed context, see:
- `CLEANUP_PLAN.md` - Full cleanup strategy
- `FINAL_STRUCTURE.md` - Target structure
- `ITERATION_2026-01-02_SUMMARY.md` - What was planned

## Goal
Remove 45MB of non-core code, focus repository on standalone Python package.

## Pre-Cleanup Checklist ✅
- [x] Standalone package working (firecrawl-standalone/)
- [x] Cleanup plan created (CLEANUP_PLAN.md)
- [x] Final structure designed (FINAL_STRUCTURE.md)
- [x] Documentation updated (SHARED_TASK_NOTES.md)

## Cleanup Steps (Estimated Time: 15-30 minutes)

### Step 1: Create Archive Branch (5 minutes)
```bash
# Create archive branch with current state
git checkout -b archive/original-api-implementation
git push origin archive/original-api-implementation

# Return to main branch
git checkout main

# Verify we're on main
git branch
```

### Step 2: Remove Documentation Files (2 minutes)
```bash
# Remove outdated documentation
git rm SELF_HOST.md
git rm CONTRIBUTING.md
git rm NEXT_ITERATION_PLAN.md
git rm REFACTORING_SUMMARY.md

# Remove images directory
git rm -r img/
```

### Step 3: Remove Examples (2 minutes)
```bash
# Remove all examples (standalone has its own)
git rm -r examples/
```

### Step 4: Remove SDKs (2 minutes)
```bash
# Remove all SDK directories
git rm -r apps/python-sdk
git rm -r apps/js-sdk
git rm -r apps/rust-sdk
```

### Step 5: Remove Infrastructure (5 minutes)
```bash
# Remove API server and infrastructure
git rm -r apps/api
git rm -r apps/ui
git rm -r apps/redis
git rm -r apps/nuq-postgres
```

### Step 6: Remove Testing Infrastructure (2 minutes)
```bash
# Remove test site and suite
git rm -r apps/test-site
git rm -r apps/test-suite
```

### Step 7: Remove Optional Services (2 minutes)
```bash
# Remove Go and Playwright services (standalone uses Python libs)
git rm -r apps/go-html-to-md-service
git rm -r apps/playwright-service-ts
```

### Step 8: Update README.md (5 minutes)
Create a new README.md focused on standalone package:

```markdown
# Firecrawl - Standalone Python Web Scraper

A standalone Python web scraper for easy integration into existing projects.

## Quick Start

```bash
# Install
cd firecrawl-standalone
pip install -e .

# Scrape a URL
python -c "import asyncio; from firecrawl import FirecrawlScraper; \
  asyncio.run(FirecrawlScraper().scrape('https://example.com'))"
```

## Documentation

See [firecrawl-standalone/README.md](firecrawl-standalone/README.md) for full documentation.

## License

Apache License 2.0
```

### Step 9: Verify Changes (2 minutes)
```bash
# Check what will be removed
git status

# Review file count (should be much smaller)
find . -type f | wc -l

# Check repository size
du -sh .

# Verify standalone package is intact
ls -la firecrawl-standalone/
```

### Step 10: Test Standalone Package (5 minutes)
```bash
# Test import
cd firecrawl-standalone
python -c "import firecrawl; print('✓ Import works')"

# Run basic example (if network available)
python examples/basic_scrape.py
```

### Step 11: Commit Changes (2 minutes)
```bash
# Add all changes
git add -A

# Commit
git commit -m "Refactor: Remove non-core code, focus on standalone Python package

- Remove SDKs (python-sdk, js-sdk, rust-sdk) - 2.3MB
- Remove API server infrastructure - 12MB
- Remove testing infrastructure - 15MB
- Remove examples - 18MB
- Remove outdated documentation - 40KB
- Remove images - 2.9MB

Total reduction: 90% (50MB → 5MB)

Repository now focuses on standalone Python package in firecrawl-standalone/

See CLEANUP_PLAN.md for details.
Original code preserved in archive/original-api-implementation branch"
```

### Step 12: Push Changes (2 minutes)
```bash
# Push to remote
git push origin main
```

## Post-Cleanup Verification ✅

After cleanup, verify:

- [ ] Repository size < 10MB (`du -sh .`)
- [ ] Only core files remain (`ls -la`)
- [ ] firecrawl-standalone/ is intact
- [ ] README.md updated
- [ ] Package imports work (`python -c "import firecrawl"`)
- [ ] Archive branch exists (`git branch -a | grep archive`)

## Rollback Plan (If Needed)

If anything goes wrong:

```bash
# Reset to before cleanup
git reflog

# Find the commit before cleanup
git reset --hard <commit-hash>

# Or checkout archive branch
git checkout archive/original-api-implementation
```

## What You Should See After Cleanup

```
firecrawl/
├── firecrawl-standalone/    # Core package (1MB)
├── README.md                 # Updated (5KB)
├── LICENSE                   # Legal (36KB)
├── CLAUDE.md                 # AI context (4KB)
├── SHARED_TASK_NOTES.md      # Notes (8KB)
├── .gitignore               # Git config
└── .git/                    # History (preserved)
```

Total: ~5MB (down from 50MB)

## Tips

1. **Go slow**: Check each step with `git status`
2. **Verify often**: Test standalone package after major deletions
3. **Commit frequently**: Create checkpoints if needed
4. **Stay calm**: Everything is recoverable via git

## Expected Results

- ✅ Clean, focused repository
- ✅ 90% size reduction
- ✅ Clear project structure
- ✅ Easy to understand
- ✅ Aligned with project goal

## Next Steps After Cleanup

1. Update SHARED_TASK_NOTES.md (mark Phase 2 complete)
2. Test standalone package thoroughly
3. Consider if any additional polish needed
4. **Done!** Project refactoring complete

## Questions?

See detailed documentation:
- `CLEANUP_PLAN.md` - Why we're removing what we're removing
- `FINAL_STRUCTURE.md` - What the final structure looks like
- `ITERATION_2026-01-02_SUMMARY.md` - How we got here

---

**Ready to clean up!** Follow the steps above and you'll have a clean, focused repository in 30 minutes.
