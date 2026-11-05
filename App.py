HSSLive Study Notes Extractor

Developed with Python and Streamlit

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

st.set_page_config(
page_title="Study AI - HSSLive Extractor",
page_icon="📚",
layout="centered"
)

st.title("📚 Study AI")
st.subheader("HSSLive Study Notes Extractor")

st.write(
"Extract educational content from HSSLive "
"and prepare it for your Study AI."
)

st.divider()

url = st.text_input(
"Enter HSSLive Article URL",
placeholder="https://www.hsslive.in/..."
)

def extract_notes(url):

parsed = urlparse(url)

if parsed.scheme != "https" or parsed.hostname not in (
    "hsslive.in",
    "www.hsslive.in"
):
    raise ValueError("Please enter a valid HSSLive HTTPS URL.")

headers = {
    "User-Agent": "StudyNotesExtractor/1.0 (personal study)"
}

response = requests.get(
    url,
    headers=headers,
    timeout=20
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Remove unnecessary elements
for tag in soup([
    "script",
    "style",
    "nav",
    "footer",
    "header",
    "aside",
    "form"
]):
    tag.decompose()

# Find main article
article = (
    soup.find("article")
    or soup.find("main")
    or soup.find(class_="post-body")
    or soup.body
)

if article is None:
    raise ValueError("No readable article content found.")

# Extract useful content
extracted = []

for element in article.find_all(
    ["h1", "h2", "h3", "h4", "p", "li"]
):

    text = element.get_text(" ", strip=True)

    if text and text not in extracted:
        extracted.append(text)

result = "\n\n".join(extracted)

if not result.strip():
    raise ValueError("No study notes found on this page.")

return result[:60000]

if st.button("🚀 Extract Study Notes", use_container_width=True):

if not url:
    st.warning("Please enter an article URL.")

else:
    try:
        with st.spinner("Extracting study notes..."):

            notes = extract_notes(url)

            st.session_state["notes"] = notes

            st.success("Notes extracted successfully!")

    except Exception as error:
        st.error(f"Extraction failed: {error}")

if "notes" in st.session_state:

st.divider()

st.subheader("📖 Extracted Study Notes")

st.text_area(
    "Your extracted content",
    st.session_state["notes"],
    height=400
)

st.download_button(
    label="📥 Download Notes",
    data=st.session_state["notes"],
    file_name="study_notes.txt",
    mime="text/plain",
    use_container_width=True
)

st.info(
    "Your notes are ready to be used by your Study AI."
)

st.divider()

st.caption("Study AI | HSSLive Notes Extractor")