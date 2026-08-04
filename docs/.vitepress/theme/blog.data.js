import { createContentLoader } from 'vitepress'

export default createContentLoader('blog/posts/*.md', {
  excerpt: true,
  transform(rawData) {
    return rawData.map(({ url, frontmatter, excerpt }) => {
      return {
        url,
        title: frontmatter.title,
        date: frontmatter.date,
        author: frontmatter.author || 'TheCrazy8',
        tags: frontmatter.tags || [],
        excerpt: frontmatter.excerpt || excerpt || '',
        content: excerpt || ''
      }
    })
  }
})
