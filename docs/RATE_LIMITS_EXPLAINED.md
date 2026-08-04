# GitHub API Rate Limits Explained

## Quick Answer

**YES! The 5,000 requests/hour is PER PERSON who signs in with GitHub.**

Each authenticated user gets their own separate rate limit quota that is NOT shared with other users.

---

## Visual Breakdown

### Scenario 1: Nobody Signs In (Anonymous)

```
┌─────────────────────────────────────┐
│  Office Network (Same IP Address)  │
│                                     │
│  👤 User A ──┐                      │
│  👤 User B ──┤ Share 60 req/hour   │
│  👤 User C ──┤ = 20 each if fair   │
│  👤 User D ──┘                      │
│                                     │
└─────────────────────────────────────┘
```

**Problem**: Multiple users from the same IP (office, school, home) share the 60/hour limit. Runs out quickly!

---

### Scenario 2: Everyone Signs In (Authenticated)

```
┌─────────────────────────────────────┐
│  Office Network (Same IP Address)  │
│                                     │
│  👤 User A → 5,000 req/hour         │
│  👤 User B → 5,000 req/hour         │
│  👤 User C → 5,000 req/hour         │
│  👤 User D → 5,000 req/hour         │
│                                     │
│  Total: 20,000 req/hour!            │
└─────────────────────────────────────┘
```

**Solution**: Each authenticated user gets their own 5,000/hour quota. Personal and not shared!

---

## Real-World Examples

### Example 1: Solo Developer at Home
```
Anonymous:     60 requests/hour
Authenticated: 5,000 requests/hour (83x improvement!)
```

### Example 2: Team of 5 in Office
```
All Anonymous:     60 req/hour total = 12 per person
All Authenticated: 25,000 req/hour total = 5,000 per person
```

### Example 3: Classroom of 30 Students
```
All Anonymous:     60 req/hour total = 2 per person! 😱
All Authenticated: 150,000 req/hour total = 5,000 per person! 🎉
```

---

## How GitHub Tracks Rate Limits

### For Anonymous Users (Not Signed In)
- Tracked by: **IP Address**
- Limit: 60 requests/hour
- Reset: Every hour
- Shared: YES - All users from same IP share the limit

**Real-world impact**: In an office or school with many users, the 60 requests can be exhausted in minutes!

### For Authenticated Users (Signed In)
- Tracked by: **OAuth Token** (unique per user)
- Limit: 5,000 requests/hour
- Reset: Every hour
- Shared: NO - Each user has their own quota

**Real-world impact**: Each person can browse documentation freely without worrying about rate limits!

---

## Why This Matters for Documentation Sites

Documentation sites make many API calls:
- Fetching commit history
- Loading plugin information
- Checking repository stats
- Displaying contributor data
- Real-time updates

**Without authentication**: 60 requests/hour can be exhausted quickly, especially on:
- Popular documentation pages
- Shared networks (offices, schools)
- Pages with auto-refresh
- Multiple tabs open

**With authentication**: 5,000 requests/hour per user means:
- ✅ No interruptions while browsing
- ✅ Multiple tabs/windows work fine
- ✅ Auto-refresh features work reliably
- ✅ No fighting for quota with colleagues
- ✅ Heavy users don't impact others

---

## Common Questions

### Q: If I sign in, do I use up quota for others?
**A: NO!** Each authenticated user gets their own 5,000/hour quota. You cannot use up anyone else's quota.

### Q: What if some people sign in and others don't?
**A: Great question!**
- Signed-in users: Each gets 5,000/hour
- Non-signed-in users: Share the 60/hour IP-based quota

They don't interfere with each other!

### Q: Does signing out reset my quota?
**A: No.** Your quota is tied to your GitHub account and resets every hour regardless of sign-in status.

### Q: Can I share my authentication with others?
**A: No, and you shouldn't!** Each person should sign in with their own GitHub account to get their own quota.

### Q: What happens if I reach my 5,000 limit?
**A: Rare, but possible!** You'll see a rate limit message and need to wait until your quota resets (shown in the error message). For most users, 5,000/hour is more than enough.

---

## Bottom Line

✅ **5,000 requests/hour is PER AUTHENTICATED USER**
✅ **Each person gets their own separate quota**
✅ **Not shared between users**
✅ **83x improvement over anonymous usage**

Sign in with GitHub to get your personal 5,000 requests/hour quota!

---

## Additional Resources

- [GitHub Rate Limiting Documentation](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [Test Authentication on this Site](/github-auth-test)
- [GitHub OAuth Setup Guide](./GITHUB_OAUTH_SETUP.md)
