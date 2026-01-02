# Firecrawl Repository Cleanup Plan

## Goal
Refactor the entire project to focus on the standalone Python implementation, removing non-core code and excessive documentation.

## Current State
- **Repository Size**: ~50MB (mostly in apps/ and examples/)
- **Core Implementation**: ✅ Complete in `firecrawl-standalone/`
- **Legacy Code**: Original Node.js/TypeScript API server and all SDKs
- **Examples**: 18MB of example applications and blog posts

## Classification: Core vs Non-Core

### ✅ CORE (Keep - Essential for Project)

#### 1. Standalone Python Package
```
firecrawl-standalone/
├── firecrawl/          # Core scraping logic
├── examples/           # Usage examples (3 core examples)
├── tests/              # Test suite
├── README.md           # Package documentation
└── pyproject.toml      # Package config
```
**Status**: ✅ Complete - This IS the refactored project

#### 2. Essential Repository Files
```
LICENSE                 # Legal requirement
.gitignore             # Git configuration
README.md              # Main project README (needs update)
CLAUDE.md              # AI assistant instructions
docker-compose.yaml    # May be needed for some services
```

#### 3. Reference Implementation (Optional - May Keep)
```
apps/api/src/scraper/  # Original scraping logic (reference only)
```
**Decision**: Keep for now as reference, can remove later if needed

### ❌ NON-CORE (Remove - Not Essential)

#### 1. SDK Implementations (Redundant - Standalone is Self-Contained)
```
apps/python-sdk/       # 1.2MB - Client SDK (requires API server)
apps/js-sdk/           # 852KB - Node.js SDK (requires API server)
apps/rust-sdk/         # 276KB - Rust SDK (requires API server)
```
**Reason**: The standalone Python package doesn't need client SDKs that call an API server

#### 2. API Server Infrastructure (Not Needed for Standalone)
```
apps/api/              # 12MB - Full API server (except scraper code for reference)
apps/ui/               # 340KB - Web UI for API
apps/redis/            # 40KB - Redis config for queue
apps/nuq-postgres/     # 16KB - Database config
```
**Reason**: Standalone version doesn't use the API server, queues, or database

#### 3. Services (Can Run Independently if Needed)
```
apps/go-html-to-md-service/    # 68KB - Go markdown service
apps/playwright-service-ts/    # 76KB - Playwright service
```
**Decision**: These are optional for standalone. Keep if referenced, otherwise remove.
**Note**: Standalone uses Python libraries (markdownify, playwright) instead

#### 4. Testing Infrastructure
```
apps/test-site/        # 13MB - Test website for CI/CD
apps/test-suite/       # 2MB - Integration test suite
```
**Reason**: Not needed for standalone package (has its own tests)

#### 5. Examples (Excessive - 18MB)
```
examples/              # 60 example apps + blog posts
├── aginews-ai-newsletter/
├── ai-podcast-generator/
├── claude_stock_analyzer/
├── blog-articles/     # Multiple blog posts
├── ... (50+ more example apps)
```
**Reason**:
- Most examples are for the API server (not standalone)
- Blog articles are outdated documentation
- Standalone already has 3 core examples

#### 6. Documentation (Redundant or Outdated)
```
SELF_HOST.md           # 12KB - Self-hosting guide (for API server)
CONTRIBUTING.md        # 8KB - Contributing guide (for API server)
NEXT_ITERATION_PLAN.md # 12KB - Planning doc (completed)
REFACTORING_SUMMARY.md # 8KB - Progress doc (completed)
```
**Reason**: These documents describe the old API server architecture

#### 7. Images (Not Essential)
```
img/                   # 2.9MB - Logos and screenshots
```
**Reason**: Branding materials not needed for library

## Cleanup Strategy

### Phase 1: Documentation Cleanup (Safe, Reversible)
**Files to Delete**:
- SELF_HOST.md
- CONTRIBUTING.md
- NEXT_ITERATION_PLAN.md
- REFACTORING_SUMMARY.md
- img/

**Rationale**: These are documentation files that describe the old architecture. Can be recovered from git history if needed.

### Phase 2: Examples Cleanup (High Impact)
**Files to Delete**:
- examples/ (keep only standalone's own examples)

**Rationale**: 18MB of examples that don't work with standalone package.

**What to Keep**:
- `firecrawl-standalone/examples/` (3 core examples already created)

### Phase 3: SDKs and Infrastructure (Major Cleanup)
**Directories to Delete**:
- apps/python-sdk/
- apps/js-sdk/
- apps/rust-sdk/
- apps/ui/
- apps/redis/
- apps/nuq-postgres/
- apps/test-site/
- apps/test-suite/

**Rationale**: These are all infrastructure for running the API server, which the standalone version doesn't need.

**What to Keep**:
- apps/api/src/scraper/ (for reference only, optional)
- apps/go-html-to-md-service/ (optional, can be removed)
- apps/playwright-service-ts/ (optional, can be removed)

### Phase 4: Update Main README
**Changes Needed**:
1. Rewrite README.md to focus on standalone Python package
2. Remove references to API server
3. Update installation instructions
4. Point to firecrawl-standalone/ for documentation

## Alternative Approach: Archive Strategy

Instead of deleting, we can move non-core code to an archive branch:

```bash
git checkout -b archive/original-api-implementation
git push origin archive/original-api-implementation
git checkout main

# Then remove from main
git rm -r apps/python-sdk apps/js-sdk apps/rust-sdk
# ... etc
```

**Benefits**:
- Nothing is permanently lost
- Can reference if needed
- Clean main branch

## Estimated Impact

### Before Cleanup
- **Repository Size**: ~50MB
- **Directories**: ~80 major directories
- **Focus**: Scattered between API server and standalone

### After Cleanup
- **Repository Size**: ~5-10MB (estimated)
- **Directories**: ~5-10 directories
- **Focus**: Clear - standalone Python package

### Lines of Code Reduction
- **Remove**: ~100K+ lines of TypeScript/Node.js code
- **Keep**: ~3K lines of Python code (standalone package)

## Recommended Action Plan

### Option 1: Aggressive Cleanup (Recommended)
Remove everything non-core, focus entirely on standalone Python package.

**Pros**:
- Clean repository
- Clear focus
- Easy to understand
- Smaller clone size

**Cons**:
- Can't reference old implementation
- Loses historical context (recoverable via git)

### Option 2: Conservative Cleanup
Keep apps/ for reference, only remove examples and redundant docs.

**Pros**:
- Keep reference implementation
- Can port features if needed

**Cons**:
- Repository still large
- Confusing (two implementations)
- Not aligned with goal

### Option 3: Archive Branch (Balanced)
Move non-core to archive branch, delete from main.

**Pros**:
- Clean main branch
- History preserved in archive
- Best of both worlds

**Cons**:
- More git operations
- Archive branch needs maintenance

## My Recommendation

**Option 3: Archive Branch + Aggressive Cleanup on Main**

This approach:
1. Creates an archive branch preserving everything
2. Cleans main branch to focus on standalone Python
3. Allows recovery if needed
4. Aligns with project goal
5. Maintains git history

## Next Steps

1. **Create Archive Branch**: Preserve current state
2. **Remove Examples**: Delete 18MB of examples/
3. **Remove SDKs**: Delete all SDK directories
4. **Remove Infrastructure**: Delete API server, UI, databases
5. **Remove Documentation**: Delete outdated docs
6. **Remove Images**: Delete img/ directory
7. **Update README**: Rewrite to focus on standalone
8. **Update SHARED_TASK_NOTES.md**: Document completed work

## Questions for Next Iteration

1. **Should we keep any reference to the API server?**
   - Option A: Remove entirely (clean break)
   - Option B: Keep README note about alternative architecture
   - Option C: Keep in archive branch only

2. **Should we keep the Go/Playwright services?**
   - Standalone uses Python equivalents
   - These services are only needed for API server
   - Recommendation: Remove from main, keep in archive

3. **What about the scraper reference code?**
   - apps/api/src/scraper/ has the original implementation
   - Could be useful for porting features
   - Recommendation: Move to firecrawl-standalone/reference/ or remove

4. **How should we handle this cleanup?**
   - All in one iteration (aggressive)
   - Incremental over multiple iterations (conservative)
   - Create archive branch first (safe)

## Success Criteria

✅ **Repository Focused on Python Standalone**:
- [ ] Main README describes standalone Python package
- [ ] No SDK directories (python-sdk, js-sdk, rust-sdk)
- [ ] No API server infrastructure
- [ ] No examples/ directory (or minimal)
- [ ] Repository size < 10MB
- [ ] Clear project structure
- [ ] All docs point to standalone implementation
