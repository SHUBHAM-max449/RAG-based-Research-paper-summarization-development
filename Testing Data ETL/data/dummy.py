import feedparser
import csv,urllib
import os

# Define query
base_url = 'http://export.arxiv.org/api/query?'
query = {
    'search_query': 'all:genai',
    'start': 0,
    'max_results': 10  # Change as needed
}
query_url = base_url + urllib.parse.urlencode(query)

# Parse the feed
feed = feedparser.parse(query_url)


# Define path
csv_folder = 'Testing Data ETL/data'
csv_path = os.path.join(csv_folder, 'results.csv')

# Create the directory if it doesn't exist
os.makedirs(csv_folder, exist_ok=True)
# Prepare CSV file
with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'authors', 'published', 'summary', 'arxiv_id', 'pdf_url']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for entry in feed.entries:
        title = entry.title.replace('\n', ' ').strip()
        summary = entry.summary.replace('\n', ' ').strip()
        published = entry.published
        authors = ', '.join(author.name for author in entry.authors)
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

print("CSV file 'results.csv' created successfully.")
