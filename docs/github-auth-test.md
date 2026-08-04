# GitHub Authentication Test

This page demonstrates the GitHub OAuth Device Flow authentication.

## Try it out!

<script setup>
import GitHubAuthButton from './.vitepress/theme/components/GitHubAuthButton.vue'
</script>

<GitHubAuthButton 
  message="Sign in with GitHub for higher rate limits (5,000/hour vs 60/hour)"
  :showSignIn="true"
  :showRateLimit="true"
/>

## How It Works

The GitHub Device Flow allows you to authenticate without requiring a backend server:

1. **Click "Sign in with GitHub"** - A modal appears with a unique code
2. **Copy the code** - Click the copy button to copy the code
3. **Open GitHub** - Click the button to open GitHub in a new tab
4. **Paste the code** - Paste the code on GitHub and authorize
5. **Done!** - You'll be automatically signed in with higher rate limits

## Benefits

- **5,000 requests/hour PER USER** instead of 60/hour shared by IP for anonymous users
- Each signed-in user gets their own personal quota (not shared!)
- No backend server required (Device Flow)
- Secure OAuth 2.0 authentication
- Only requests read-only `public_repo` access

### Rate Limit Breakdown

| User Type | Rate Limit | Shared? |
|-----------|------------|---------|
| Anonymous (not signed in) | 60/hour | Yes (by IP address) |
| Authenticated (signed in) | 5,000/hour | No (per user) |

**Example Scenario**: 
- 🏢 10 people in an office, none signed in → Share 60 requests/hour (6 per person!)
- ✅ 10 people in an office, all signed in → Each gets 5,000 requests/hour (50,000 total!)

## Testing

Try these actions after signing in:

- Check the rate limit display
- View commit history on other pages
- Verify authenticated requests work
- Sign out and sign in again

## For Developers

This implementation uses:
- **GitHub Device Flow OAuth** - No backend required
- **Client ID**: `Ov23li1xL6Hj2CflCVf2` (public, safe to commit)
- **Scope**: `public_repo` (read-only)
- **Token Storage**: localStorage with expiry
- **Polling**: Automatic token exchange

See [GITHUB_OAUTH_SETUP.md](./GITHUB_OAUTH_SETUP.md) for more details.
