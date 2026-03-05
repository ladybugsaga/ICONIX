import requests
import xml.etree.ElementTree as ET
from datetime import datetime

BLOG_SITEMAP = "https://iconix254.blogspot.com/sitemap.xml"
MY_DOMAIN = "https://beyonddennis.shop"
SITEMAP_FILE = "sitemap.xml"

def fetch_blog_urls():
    try:
        response = requests.get(BLOG_SITEMAP)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        
        # Namespace handling for sitemap XML
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        urls = []
        for url in root.findall('ns:url', ns):
            loc = url.find('ns:loc', ns).text
            # Convert Blogger URL to Custom Domain URL
            # https://iconix254.blogspot.com/2026/03/post.html -> https://beyonddennis.shop/2026/03/post.html
            new_loc = loc.replace("https://iconix254.blogspot.com", MY_DOMAIN)
            urls.append(new_loc)
        return urls
    except Exception as e:
        print(f"Error fetching blog sitemap: {e}")
        return []

def update_local_sitemap(blog_urls):
    if not blog_urls:
        print("No URLs found, skipping update.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    
    # Start building the XML
    sitemap_content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <!-- Main page -->',
        '  <url>',
        f'    <loc>{MY_DOMAIN}/</loc>',
        f'    <lastmod>{today}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
        '  <!-- Blog posts (automatically mirrored from Blogger) -->'
    ]

    for url in blog_urls:
        # Avoid duplicating root
        if url.strip("/") == MY_DOMAIN:
            continue
            
        sitemap_content.append('  <url>')
        sitemap_content.append(f'    <loc>{url}</loc>')
        sitemap_content.append(f'    <lastmod>{today}</lastmod>')
        sitemap_content.append('    <changefreq>weekly</changefreq>')
        sitemap_content.append('    <priority>0.8</priority>')
        sitemap_content.append('  </url>')

    sitemap_content.append('</urlset>')
    
    with open(SITEMAP_FILE, "w") as f:
        f.write("\n".join(sitemap_content))
    
    print(f"Successfully updated {SITEMAP_FILE} with {len(blog_urls)} posts.")

if __name__ == "__main__":
    urls = fetch_blog_urls()
    update_local_sitemap(urls)
