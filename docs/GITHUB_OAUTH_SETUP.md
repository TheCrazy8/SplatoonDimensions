# GitHub OAuth Setup Guide

## Overview

BrightOS documentation site uses GitHub's API to fetch commit history and other dynamic content. To prevent rate limiting (60 requests/hour for unauthenticated users), the site implements **GitHub Device Flow OAuth** authentication.

## Device Flow Authentication

✅ **No backend server required!**

The site uses GitHub's Device Flow OAuth, which allows users to authenticate without requiring a backend server to exchange tokens. This is perfect for static sites hosted on GitHub Pages.

### How It Works

1. User clicks "Sign in with GitHub"
2. App requests a device code from GitHub
3. User copies the code and authorizes on GitHub
4. App polls GitHub for the access token
5. Token is stored locally and used for API requests

## For Users

### Why Sign In?

- **Higher Rate Limits**: Authenticated users get **5,000 requests/hour PER USER** vs 60/hour shared by IP for anonymous users
- **Better Experience**: No interruptions due to rate limiting
- **Secure**: Uses OAuth 2.0 standard authentication flow
- **No Backend Required**: Device Flow works without a server
- **Personal Quota**: Each signed-in user gets their own rate limit quota

### How to Sign In

1. Look for the "Sign in with GitHub" button on pages that fetch GitHub data
2. Click the button to open the authentication modal
3. Copy the unique code displayed
4. Click "Open GitHub to Authorize" to open GitHub in a new tab
5. Paste the code on GitHub and click "Continue"
6. Authorize the app
7. Return to the documentation - you'll be automatically signed in!

### What Permissions Are Requested?

- **`public_repo`**: Read-only access to public repository data
- No write permissions or access to private data
- No access to personal information

## For Developers/Maintainers

### Setup (Already Configured!)

The Device Flow is already set up and requires minimal configuration:

**OAuth App Client ID**: `Ov23li1xL6Hj2CflCVf2`

This client ID is:
- ✅ Safe to commit to public repositories
- ✅ Configured for Device Flow
- ✅ Limited to `public_repo` scope
- ✅ No client secret needed (Device Flow advantage!)

### Testing the Authentication

1. Navigate to the [GitHub Auth Test Page](/github-auth-test)
2. Click "Sign in with GitHub"
3. Follow the Device Flow process
4. Verify authentication status and rate limits

### Creating Your Own OAuth App (Optional)

If you want to use your own OAuth App:

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the details:
   - **Application name**: Your App Name
   - **Homepage URL**: Your site URL
   - **Authorization callback URL**: Not used for Device Flow
   - **Application description**: Description

4. After creation, note your **Client ID**
5. Enable **Device Flow** in your OAuth App settings
6. Update the client ID in `.env`:
   ```bash
   VITE_GITHUB_CLIENT_ID=your_client_id_here
   ```

### Architecture

**No Backend Needed!** The implementation uses:

```
User Browser
    ↓ (1) Request device code
GitHub API (Device Flow)
    ↓ (2) Return device code + verification URL
User Browser → GitHub Website (User authorizes)
    ↓ (3) Poll for token
GitHub API
    ↓ (4) Return access token
User Browser (Token stored in localStorage)
    ↓ (5) Authenticated API requests
GitHub API
```

### Implementation Details

**File**: `docs/.vitepress/theme/config/github-auth.js`
```javascript
// Device Flow configuration
const GITHUB_CONFIG = {
  clientId: 'Ov23li1xL6Hj2CflCVf2',
  deviceCodeUrl: 'https://github.com/login/device/code',
  accessTokenUrl: 'https://github.com/login/oauth/access_token',
  scope: 'public_repo',
  pollInterval: 5 // seconds
}
```

**Component**: `docs/.vitepress/theme/components/GitHubAuthButton.vue`
- Modal-based UI for Device Flow
- Automatic polling for token
- Token storage with expiry
- Rate limit display

**Usage in Markdown**:
```vue
<GitHubAuthButton 
  message="Sign in for higher limits"
  :showSignIn="true"
  :showRateLimit="true"
/>
```

## Current Implementation Status

### ✅ Fully Implemented
- GitHub Device Flow OAuth authentication
- Modal UI with code display and copy
- Automatic token polling
- Token storage and management
- Authenticated API requests with `githubFetch`
- Rate limit detection and display
- SSR-safe implementation

### 🎯 Benefits Over Traditional OAuth
- ✅ No backend server required
- ✅ No client secret to protect
- ✅ Works on static hosting (GitHub Pages)
- ✅ Secure and standards-compliant
- ✅ User-friendly copy-paste flow

## Security Considerations

- ✅ No client secret needed (Device Flow advantage)
- ✅ Client ID safe to expose (public by design)
- ✅ CSRF not applicable (no redirect callback)
- ✅ Tokens stored in localStorage with expiry
- ✅ Only requests `public_repo` scope (read-only)
- ✅ No access to private repositories or user data

## Troubleshooting

### Modal doesn't appear
- Check browser console for errors
- Verify JavaScript is enabled
- Try disabling ad blockers

### Authorization fails
- Verify the code was copied correctly
- Check if the code expired (10 minutes timeout)
- Try the process again with a new code

### Rate limiting still occurs
- Verify you're signed in (check auth status)
- Check if authentication token is being sent (browser dev tools)
- Verify token hasn't expired (check localStorage)

### Polling timeout
- Check internet connection
- Ensure you clicked "Authorize" on GitHub
- Try signing in again

## Alternative: Personal Access Token (Development Only)

For local development, you can manually set a Personal Access Token:

1. Generate a token at https://github.com/settings/tokens
2. Select `public_repo` scope
3. Manually set token in browser console:
   ```javascript
   localStorage.setItem('github_oauth_token', 'your_token_here')
   localStorage.setItem('github_oauth_expiry', new Date(Date.now() + 86400000).toISOString())
   ```

**⚠️ Never commit personal access tokens to the repository!**

## Resources

- [GitHub Device Flow Documentation](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps#device-flow)
- [GitHub API Rate Limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [OAuth 2.0 Device Flow RFC](https://datatracker.ietf.org/doc/html/rfc8628)
- [Test Authentication Page](/github-auth-test)

