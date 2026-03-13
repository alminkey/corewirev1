# SEO Readiness Checklist

## Crawl and Indexing

- [ ] `robots.ts` exposes crawl rules and sitemap reference
- [ ] `sitemap.ts` includes homepage and article URLs
- [ ] article pages expose canonical URLs through metadata alternates
- [ ] `developing_story` pages emit controlled robots directives

## Metadata

- [ ] homepage metadata is generated from live homepage payloads
- [ ] article metadata is generated from live article payloads
- [ ] Open Graph fields are populated for homepage and articles
- [ ] slugs remain stable across publish/update flows

## Structured Data

- [ ] article pages include JSON-LD `NewsArticle`
- [ ] structured data fields reflect the visible article content
- [ ] timestamps and canonical article URLs are present

## Verification

- [ ] web smoke tests pass
- [ ] browser smoke reaches `/`, article page, `/sitemap.xml`, and `/robots.txt`
- [ ] no placeholder draft pages are exposed to indexing
