# Documentation Features Guide

## Overview

This guide covers all the quality-of-life features available in the BrightOS documentation site.

### Understanding GitHub API Rate Limits

**Anonymous/Unauthenticated Users**:
- 60 requests per hour
- **Shared by IP address** - if multiple users access from the same network, they share the 60 request limit
- Can run out quickly on shared networks (schools, offices, etc.)

**Authenticated Users (Signed in with GitHub)**:
- **5,000 requests per hour PER USER** 🎉
- Each person who signs in gets their own separate quota
- Your personal 5,000/hour limit is NOT shared with other users
- Perfect for heavy documentation browsing

**Example**: If 10 people in your office sign in with GitHub, each person gets their own 5,000 requests/hour!

---

## 1. 🔍 Search Functionality

### Local Search (Default)

The site uses VitePress's built-in local search, which:
- Works offline after initial load
- Searches across all documentation pages
- Includes fuzzy matching (tolerates typos)
- Boosts results by title and headings
- No external dependencies required

**How to use:**
- Press `Ctrl+K` or `Cmd+K` to open search
- Or click the search icon in the navigation bar
- Type your query and browse results

### Upgrading to Algolia DocSearch (Optional)

For larger documentation sites, you can upgrade to Algolia DocSearch:

1. Apply at https://docsearch.algolia.com/
2. Once approved, update `docs/.vitepress/config.mjs`:
   ```javascript
   search: {
     provider: 'algolia',
     options: {
       appId: 'YOUR_APP_ID',
       apiKey: 'YOUR_API_KEY',
       indexName: 'YOUR_INDEX_NAME'
     }
   }
   ```

## 2. ⏳ Loading Indicators

### LoadingSpinner Component

A reusable loading spinner for async data operations.

**Usage in Markdown:**
```vue
<LoadingSpinner :loading="isLoading" text="Loading data...">
  <p>Your content here</p>
</LoadingSpinner>
```

**Usage in Vue Components:**
```vue
<script setup>
import { ref } from 'vue'
import LoadingSpinner from './.vitepress/theme/components/LoadingSpinner.vue'

const loading = ref(true)

// Your data fetching logic
</script>

<template>
  <LoadingSpinner :loading="loading" text="Fetching data...">
    <div>{{ data }}</div>
  </LoadingSpinner>
</template>
```

### DownloadStats Component

Displays plugin download statistics with automatic loading state.

**Usage in Markdown:**
```vue
<DownloadStats />
```

This component:
- Fetches real-time stats from Supabase
- Shows loading spinner while fetching
- Displays download counts in a grid layout
- Handles errors gracefully

## 3. 📱 PWA Features

### PWA Install Prompt

The site can be installed as a Progressive Web App (PWA) for:
- Offline access to documentation
- Faster load times
- App-like experience on mobile and desktop

**User Experience:**
1. A prompt appears after 3 seconds on first visit
2. Users can install immediately or dismiss
3. Dismissed prompts reappear after 7 days
4. Option to dismiss permanently

**How to Install:**
1. Wait for the install prompt or click the install icon in browser
2. Click "Install" in the prompt
3. The app will be added to your device

### PWA Update Notifications

When a new version is available:
- A notification appears at the bottom right
- Click "Update Now" to refresh with the latest version
- Or click "Later" to continue with current version

## 4. 🔐 GitHub OAuth Integration

### For Users

**Benefits:**
- **5,000 API requests/hour** vs 60 for unauthenticated users
- No interruptions from rate limiting
- Better experience when browsing commit history

**How to Sign In:**
1. Look for the "Sign in with GitHub" button on pages with GitHub data
2. Click to authorize the app
3. Grant `public_repo` read-only permission
4. You're done! Higher rate limits apply automatically

**Permissions:**
- Only requests `public_repo` scope (read-only access to public repos)
- No write permissions
- No access to private repositories
- No access to personal data

### For Developers

See [GITHUB_OAUTH_SETUP.md](./GITHUB_OAUTH_SETUP.md) for complete setup instructions including:
- Creating a GitHub OAuth App
- Configuring environment variables
- Setting up backend token exchange
- Deployment configuration

## 5. 📦 Always Fresh Plugin Data

The plugin marketplace now fetches data directly from GitHub:
- **Source**: `https://raw.githubusercontent.com/TheCrazy8/.../plugins-cache.json`
- **Benefits**:
  - Always up-to-date with repository
  - No stale bundled cache
  - No rate limiting (raw content)
- **Automatic**: Works without configuration

## 6. 💾 Smart Caching

### Service Worker Caching

The PWA service worker caches:
- **Static Assets**: HTML, CSS, JS, images (long-term cache)
- **GitHub API**: Commits, repository data (1 hour cache)
- **Supabase API**: Download stats, reviews (1 hour cache)
- **Fonts**: Google Fonts (1 year cache)

### Browser Caching

- **Commit History**: Cached for 5 minutes in localStorage
- **OAuth Tokens**: Stored securely with expiry
- **User Preferences**: PWA install dismissals, theme settings

## Using Components in Markdown

All components are globally registered and can be used directly in markdown files:

### LoadingSpinner
```vue
<LoadingSpinner :loading="true" text="Loading...">
  Content here
</LoadingSpinner>
```

### DownloadStats
```vue
<DownloadStats />
```

### GitHubAuthButton
```vue
<GitHubAuthButton 
  message="Sign in for higher rate limits"
  :showRateLimit="true"
/>
```

### PluginCard
```vue
<PluginCard :plugin="pluginData" @try-in-web="handleTry" />
```

## Performance Optimizations

1. **Lazy Loading**: Components loaded only when needed
2. **Code Splitting**: Separate bundles for different pages
3. **Asset Optimization**: Images, fonts, and icons optimized
4. **Caching Strategy**: Multi-layer caching (service worker + localStorage)
5. **SSR**: Server-side rendering for fast initial load

## Accessibility

- **Keyboard Navigation**: All interactive elements keyboard-accessible
- **Screen Readers**: Proper ARIA labels and semantic HTML
- **Color Contrast**: WCAG AA compliant color contrasts
- **Focus Indicators**: Clear focus states for navigation

## Browser Support

- **Modern Browsers**: Chrome, Firefox, Safari, Edge (latest 2 versions)
- **PWA Support**: Chrome, Edge, Safari (iOS 11.3+), Samsung Internet
- **Fallbacks**: Graceful degradation for older browsers

## Troubleshooting

### Search Not Working
- Check if JavaScript is enabled
- Clear browser cache and reload
- Ensure you're on the latest site version

### PWA Install Not Showing
- Already installed (check browser apps)
- Browser doesn't support PWA
- Dismissed permanently (clear localStorage)

### Rate Limiting Issues
- Sign in with GitHub for higher limits
- Check if authentication token is valid
- Wait for rate limit reset (shown in error message)

### Loading Indicators Stuck
- Check browser console for errors
- Verify network connection
- Refresh the page

## Contributing

Found a bug or want to suggest a feature?
- [Open an issue](https://github.com/TheCrazy8/Blaze-And-Company-Official/issues)
- [Start a discussion](https://github.com/TheCrazy8/Blaze-And-Company-Official/discussions)
- Submit a pull request

## Resources

- [VitePress Documentation](https://vitepress.dev/)
- [PWA Documentation](https://web.dev/progressive-web-apps/)
- [GitHub OAuth Guide](./GITHUB_OAUTH_SETUP.md)
- [Supabase Setup](./SUPABASE_SETUP.md)
