import path from 'path'
import { writeFileSync, mkdirSync, readdirSync, readFileSync } from 'fs'
import { Feed } from 'feed'
import matter from 'gray-matter'

export async function generateFeeds(config) {
  // Use the site config for base URL
  const baseUrl = config.site?.base || '/SplatoonDimensions/'
  const siteUrl = 'https://thecrazy8.github.io' + baseUrl.replace(/\/$/, '')
  const blogUrl = `${siteUrl}/blog`

  const feed = new Feed({
    title: 'BrightOS Blog',
    description: 'Official blog for BrightOS - Arduino modular programming platform',
    id: blogUrl,
    link: blogUrl,
    language: 'en',
    image: `${siteUrl}/icon-512x512.png`,
    favicon: `${siteUrl}/favicon.ico`,
    copyright: 'Copyright © 2025-present TheCrazy8',
    feedLinks: {
      rss: `${blogUrl}/feed.xml`,
      atom: `${blogUrl}/feed.atom`,
    },
  })

  // Load blog posts from filesystem
  const postsDir = path.join(config.srcDir, 'blog/posts')
  const files = readdirSync(postsDir).filter(f => f.endsWith('.md'))

  const posts = []
  for (const file of files) {
    const filePath = path.join(postsDir, file)
    const content = readFileSync(filePath, 'utf-8')
    const { data, content: markdown } = matter(content)
    
    posts.push({
      file,
      frontmatter: data,
      content: markdown
    })
  }

  // Sort posts by date (newest first)
  posts.sort((a, b) => 
    new Date(b.frontmatter.date) - new Date(a.frontmatter.date)
  )

  // Add posts to feed
  for (const post of posts) {
    const slug = post.file.replace('.md', '')
    const url = `${siteUrl}/blog/posts/${slug}.html`
    
    feed.addItem({
      title: post.frontmatter.title,
      id: url,
      link: url,
      description: post.frontmatter.excerpt || post.content.substring(0, 200) + '...',
      content: post.content,
      author: [
        {
          name: post.frontmatter.author || 'TheCrazy8',
        },
      ],
      date: new Date(post.frontmatter.date),
      category: (post.frontmatter.tags || []).map(tag => ({ name: tag })),
    })
  }

  // Ensure blog directory exists
  const outDir = path.join(config.outDir, 'blog')
  try {
    mkdirSync(outDir, { recursive: true })
  } catch (err) {
    // Directory might already exist
  }

  // Write RSS feed
  writeFileSync(path.join(outDir, 'feed.xml'), feed.rss2(), 'utf-8')
  
  // Write Atom feed
  writeFileSync(path.join(outDir, 'feed.atom'), feed.atom1(), 'utf-8')

  console.log('✅ RSS and Atom feeds generated')
}
