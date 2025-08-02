import feedparser
import csv
import os

# Create output folder
csv_folder = 'Testing Data ETL/data'
os.makedirs(csv_folder, exist_ok=True)
csv_path = os.path.join(csv_folder, 'results.csv')

query_url = (
    "http://export.arxiv.org/api/query?"
    "search_query=cat:cs.AI&"
    "start=0&"
    "max_results=10"
)

feed = feedparser.parse(query_url)
print(f"Found {len(feed.entries)} papers")

# Write CSV
with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'authors', 'published', 'summary', 'arxiv_id', 'pdf_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for entry in feed.entries:
        title = entry.title.strip().replace('\n', ' ')
        authors = ', '.join(author.name for author in entry.authors)
        published = entry.published
        summary = entry.summary.strip().replace('\n', ' ')
        arxiv_id = entry.id.split('/abs/')[-1]
        pdf_url = f"http://arxiv.org/pdf/{arxiv_id}.pdf"

        writer.writerow({
            'title': title,
            'authors': authors,
            'published': published,
            'summary': summary,
            'arxiv_id': arxiv_id,
            'pdf_url': pdf_url
        })

print(f"✅ Done! Check: {os.path.abspath(csv_path)}")
