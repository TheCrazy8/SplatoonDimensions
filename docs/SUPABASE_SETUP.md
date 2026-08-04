# Supabase Database Setup

This document provides the SQL commands needed to set up the database tables, views, and policies for the Plugin Marketplace review and analytics system.

## Database Configuration

**Supabase URL:** `https://rshigflhanzjrqeoynpa.supabase.co`

**Project ID:** `rshigflhanzjrqeoynpa`

## SQL Setup Commands

Run these commands in the Supabase SQL Editor to set up the database schema.

### 1. Create Plugin Downloads Table

```sql
-- Create plugin_downloads table to track all downloads
CREATE TABLE IF NOT EXISTS plugin_downloads (
  id BIGSERIAL PRIMARY KEY,
  plugin_id TEXT NOT NULL,
  plugin_name TEXT NOT NULL,
  downloaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  user_agent TEXT,
  referrer TEXT
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_plugin_downloads_plugin_id ON plugin_downloads(plugin_id);
CREATE INDEX IF NOT EXISTS idx_plugin_downloads_downloaded_at ON plugin_downloads(downloaded_at);
```

### 2. Create Plugin Reviews Table

```sql
-- Create plugin_reviews table to store user reviews
CREATE TABLE IF NOT EXISTS plugin_reviews (
  id BIGSERIAL PRIMARY KEY,
  plugin_id TEXT NOT NULL,
  plugin_name TEXT NOT NULL,
  user_name TEXT NOT NULL,
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  helpful_count INTEGER DEFAULT 0
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_plugin_reviews_plugin_id ON plugin_reviews(plugin_id);
CREATE INDEX IF NOT EXISTS idx_plugin_reviews_created_at ON plugin_reviews(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_plugin_reviews_rating ON plugin_reviews(rating);
```

### 3. Create Plugin Stats View

```sql
-- Create a view to aggregate plugin statistics
CREATE OR REPLACE VIEW plugin_stats AS
SELECT 
  COALESCE(d.plugin_id, r.plugin_id) AS plugin_id,
  COALESCE(d.plugin_name, r.plugin_name) AS plugin_name,
  COALESCE(d.download_count, 0) AS download_count,
  COALESCE(r.review_count, 0) AS review_count,
  COALESCE(r.avg_rating, 0) AS avg_rating
FROM (
  -- Download counts
  SELECT 
    plugin_id,
    plugin_name,
    COUNT(*) AS download_count
  FROM plugin_downloads
  GROUP BY plugin_id, plugin_name
) d
FULL OUTER JOIN (
  -- Review stats
  SELECT 
    plugin_id,
    plugin_name,
    COUNT(*) AS review_count,
    AVG(rating) AS avg_rating
  FROM plugin_reviews
  GROUP BY plugin_id, plugin_name
) r ON d.plugin_id = r.plugin_id;
```

### 4. Create Helper Function for Incrementing Helpful Count

```sql
-- Create function to increment helpful count atomically
CREATE OR REPLACE FUNCTION increment_helpful_count(review_id BIGINT)
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  UPDATE plugin_reviews
  SET helpful_count = helpful_count + 1
  WHERE id = review_id;
END;
$$;
```

### 5. Set Up Row Level Security (RLS)

```sql
-- Enable Row Level Security
ALTER TABLE plugin_downloads ENABLE ROW LEVEL SECURITY;
ALTER TABLE plugin_reviews ENABLE ROW LEVEL SECURITY;

-- Allow public read access to downloads
CREATE POLICY "Allow public read access to downloads"
  ON plugin_downloads
  FOR SELECT
  USING (true);

-- Allow public insert access to downloads
CREATE POLICY "Allow public insert to downloads"
  ON plugin_downloads
  FOR INSERT
  WITH CHECK (true);

-- Allow public read access to reviews
CREATE POLICY "Allow public read access to reviews"
  ON plugin_reviews
  FOR SELECT
  USING (true);

-- Allow public insert access to reviews
CREATE POLICY "Allow public insert to reviews"
  ON plugin_reviews
  FOR INSERT
  WITH CHECK (true);

-- Allow public update access to reviews (for helpful count)
CREATE POLICY "Allow public update to reviews"
  ON plugin_reviews
  FOR UPDATE
  USING (true)
  WITH CHECK (true);
```

### 6. Grant Public Access to Views and Functions

```sql
-- Grant access to the view
GRANT SELECT ON plugin_stats TO anon;
GRANT SELECT ON plugin_stats TO authenticated;

-- Grant execute permission on the function
GRANT EXECUTE ON FUNCTION increment_helpful_count(BIGINT) TO anon;
GRANT EXECUTE ON FUNCTION increment_helpful_count(BIGINT) TO authenticated;
```

## Verification

After running all the SQL commands, verify the setup:

### Check Tables

```sql
-- Verify tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN ('plugin_downloads', 'plugin_reviews');
```

### Check View

```sql
-- Verify view exists and works
SELECT * FROM plugin_stats LIMIT 5;
```

### Check Policies

```sql
-- Verify RLS policies
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename IN ('plugin_downloads', 'plugin_reviews');
```

### Test Insert

```sql
-- Test inserting a download record
INSERT INTO plugin_downloads (plugin_id, plugin_name, user_agent)
VALUES ('test-plugin-id', 'Test Plugin', 'Mozilla/5.0');

-- Test inserting a review record
INSERT INTO plugin_reviews (plugin_id, plugin_name, user_name, rating, comment)
VALUES ('test-plugin-id', 'Test Plugin', 'Test User', 5, 'Great plugin!');

-- Verify data was inserted
SELECT * FROM plugin_stats WHERE plugin_id = 'test-plugin-id';
```

## Security Notes

- The current setup allows **public read and write access** to facilitate easy community engagement
- All data is anonymous (no authentication required)
- User agents and referrers are logged for analytics purposes only
- Consider adding rate limiting at the application level to prevent abuse
- For production, you may want to add:
  - Rate limiting policies
  - Input validation functions
  - Audit logging
  - Backup policies

## Maintenance

### Clean Up Old Data

```sql
-- Delete downloads older than 1 year (optional)
DELETE FROM plugin_downloads 
WHERE downloaded_at < NOW() - INTERVAL '1 year';
```

### View Statistics

```sql
-- Total downloads
SELECT SUM(download_count) AS total_downloads FROM plugin_stats;

-- Total reviews
SELECT SUM(review_count) AS total_reviews FROM plugin_stats;

-- Average rating across all plugins
SELECT AVG(avg_rating) AS overall_avg_rating FROM plugin_stats WHERE review_count > 0;

-- Top 10 most downloaded plugins
SELECT plugin_name, download_count 
FROM plugin_stats 
ORDER BY download_count DESC 
LIMIT 10;

-- Top 10 highest rated plugins (with at least 5 reviews)
SELECT plugin_name, avg_rating, review_count 
FROM plugin_stats 
WHERE review_count >= 5
ORDER BY avg_rating DESC 
LIMIT 10;
```

## Troubleshooting

### Issue: Cannot insert data

**Solution:** Check that RLS policies are properly set up:
```sql
-- Disable RLS temporarily for testing
ALTER TABLE plugin_downloads DISABLE ROW LEVEL SECURITY;
ALTER TABLE plugin_reviews DISABLE ROW LEVEL SECURITY;
```

### Issue: View returns no data

**Solution:** Check if tables have data:
```sql
SELECT COUNT(*) FROM plugin_downloads;
SELECT COUNT(*) FROM plugin_reviews;
```

### Issue: Function not found

**Solution:** Recreate the function with proper permissions:
```sql
DROP FUNCTION IF EXISTS increment_helpful_count(BIGINT);
-- Then recreate the function from step 4 above
```

## Support

For issues with Supabase setup, consult:
- [Supabase Documentation](https://supabase.com/docs)
- [Supabase SQL Editor Guide](https://supabase.com/docs/guides/database/overview)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
