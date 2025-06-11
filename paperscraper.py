import urllib
import time
import urllib.request
import feedparser
import pandas as pd
import socket

# set up base API query URL
base_url = "http://export.arxiv.org/api/query?";

# search parameters
search_query = 'all:crystalline+structure+AND+all:drug+manufacturing' # search for crystalline structures and drug manufacturing in all fields
start = 0                         # start at the first result
max_results = 100                # want 100 total results
results_per_iteration = 10        # 20 results at a time
wait_time = 3                     # number of seconds to wait between calls (to be kind to the API)

print("Searching arXiv for %s" % search_query)

paper_dict = {
        "arxiv id":[],
        "title":[],
        "published":[],
        "author(s)":[],
        "abs link":[],
        "pdf link":[],
        "journal ref":[],
        "comment":[],
        "abstract":[]}

for i in range(start, max_results, results_per_iteration):
    if len(paper_dict["arxiv id"]) >= max_results:
        break
    
    print("Results %i - %i" % (i, i+results_per_iteration))
    query = "search_query=%s&start=%i&max_results=%i" % (search_query,
                                                         i,
                                                         results_per_iteration)

    # perform a GET request using the base_url and query
    response = urllib.request.urlopen(url=base_url+query, data=None)

    # parse the response using feedparser
    feed = feedparser.parse(response)

    # print out feed information
    print("Feed title: %s" % feed.feed.title)
    print("Feed last updated: %s" % feed.feed.updated)

    # print opensearch metadata
    print("totalResults for this query: %s" % feed.feed.opensearch_totalresults)
    print("itemsPerPage for this query: %s" % feed.feed.opensearch_itemsperpage)
    print("startIndex for this query: %s" % feed.feed.opensearch_startindex)

    # Run through each entry and extract information
    for entry in feed.entries:
        # get arxiv id, title, and date published
        arxiv_id = entry.id.split('/abs/')[-1]
        
        title = entry.title
        
        published = entry.published
        
        try:
            authors = "%s" % ", ".join(author.name for author in entry.authors)
            #print("Authours: %s" % ", ".join(author.name for author in entry.authors))
        except AttributeError:
            authors = "No authors found"

        # get the links to the abs page and pdf for the e-print
        page_link = None
        pdf_link = None
        
        for link in entry.links:
            if link.rel == "alternate":
                page_link = link.href
            elif link.title == "pdf":
                pdf_link = link.href
                
        # The journal reference, comments and primary_category are in the arxiv namespace
        try:
            journal_ref = entry.arxiv_journal_ref
        except AttributeError:
            journal_ref = "No journal ref found"
        
        try:
            comment = entry.arxiv_comment
        except AttributeError:
            comment = "No comment found"
        
        # Abstract is in the <summary> element
        abstract = entry.summary
        
        paper_dict['arxiv id'].append(arxiv_id)
        paper_dict['title'].append(title)
        paper_dict['published'].append(published)
        paper_dict['author(s)'].append(authors)
        paper_dict['abs link'].append(page_link)
        paper_dict['pdf link'].append(pdf_link)
        paper_dict['journal ref'].append(journal_ref)
        paper_dict['comment'].append(comment)
        paper_dict['abstract'].append(abstract)
 
    # Allow the code to sleep a bit before calling API again
    print("Sleeping for %i seconds" % wait_time)
    time.sleep(wait_time)
    
df = pd.DataFrame(paper_dict)

SAVE_PATH = r"C:\Users\Philippa\Documents\GitHub\crystalline-mining\scraped_papers.csv"

df.to_csv(SAVE_PATH, index=False, encoding="utf-8")
print(f"Wrote {len(df)} papers to {SAVE_PATH}")