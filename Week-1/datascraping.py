import streamlit as st
import requests
from bs4 import BeautifulSoup
from PIL import Image
import pandas as pd

def scrape_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        with open('paragraphs.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n--- Paragraphs from {url} ---\n")
            for p in paragraphs:
                text = p.get_text(strip=True)
                if text:
                    f.write(text + '\n\n')
                    images = soup.find_all('img')
        image_count = 0
        image_filenames = []
        for i, img in enumerate(images):
            src = img.get('src')
            if not src:
                continue

            if not src.startswith('http'):
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = url.rstrip('/') + src
                else:
                    src = url.rstrip('/') + '/' + src

            try:
                img_data = requests.get(src, timeout=5).content
                safe_url = ''.join(c if c.isalnum() or c in ('-', '_', '.') else '_' for c in src)
                filename = f"{safe_url}.jpg"
                with open(filename, 'wb') as f:
                    f.write(img_data)
                image_filenames.append(filename)
                image_count += 1
            except Exception:
                continue
        tables = []
        html_tables = soup.find_all("table")

        for table_tag in html_tables:
            headers = []
            rows = []
            for th in table_tag.find_all("th"):
                headers.append(th.get_text(strip=True))
            for tr in table_tag.find_all("tr"):
                cells = tr.find_all(["td", "th"])
                if cells:
                    row = [cell.get_text(strip=True) for cell in cells]
                    rows.append(row)
            if rows:
                df = pd.DataFrame(rows)
                if headers and len(headers) == len(df.columns):
                    df.columns = headers
                tables.append(df)
                df.to_csv(f"table_{len(tables)}.csv", index=False)

        return len(paragraphs), image_count, tables, image_filenames

    except Exception as e:
        return f"Error: {e}", 0, [], []
def main():
    st.set_page_config(page_title="Web Scraper", page_icon="🕸️")

    try:
        img = Image.open("/home/sensen/Downloads/scrapping.jpg")
        st.image(img, use_container_width=True)
    except FileNotFoundError:
        st.warning("Header image not found.")

    st.title("🌐 Web Scraper Tool")
    st.markdown("Easily scrape **paragraphs**, **images**, and **tables** from web pages.")

    st.header("Choose Input Method")
    input_option = st.radio("Select how you'd like to input URLs:", ["Single URL", "List of URLs", "Text File"])
    urls = []

    if input_option == "Single URL":
        url = st.text_input("Enter a single URL:")
        if url:
            urls.append(url)

    elif input_option == "List of URLs":
        url_input = st.text_area("Enter one URL per line:")
        if url_input:
            urls = url_input.strip().splitlines()

    elif input_option == "Text File":
        uploaded_file = st.file_uploader("Upload a text file with URLs (one per line):", type=['txt'])
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            urls = content.strip().splitlines()

    if st.button("🚀 Submit and Scrape"):
        if urls:
            st.info("Scraping in progress...")

            for url in urls:
                with st.spinner(f"Scraping {url}..."):
                    paragraphs, image_count, tables, image_filenames = scrape_url(url)

                    if isinstance(paragraphs, str): 
                        st.error(paragraphs)
                        continue

                    st.success(f"✅ {url} — {paragraphs} paragraphs, {image_count} images downloaded.")
                    with st.expander(f"📄 View Paragraphs from {url}"):
                        with open('paragraphs.txt', 'r', encoding='utf-8') as f:
                            all_text = f.read()
                            relevant_text = []
                            capture = False
                            for line in all_text.splitlines():
                                if f"--- Paragraphs from {url} ---" in line:
                                    capture = True
                                    continue
                                elif line.startswith("--- Paragraphs from"):
                                    capture = False
                                if capture:
                                    relevant_text.append(line)
                            if relevant_text:
                                st.text("\n".join(relevant_text))
                            else:
                                st.info("No paragraphs found.")

                    
                    with st.expander(f"🖼️ View Images from {url}"):
                        if image_filenames:
                            for img_file in image_filenames:
                                try:
                                    img = Image.open(img_file)
                                    st.image(img, use_container_width=True, caption=img_file)
                                except:
                                    continue
                        else:
                            st.info("No images found or saved.")

                    
                    if tables:
                        with st.expander(f"📊 View Tables from {url}"):
                            for idx, table in enumerate(tables):
                                st.markdown(f"**Table {idx+1}**")
                                st.dataframe(table)
                                csv_filename = f"table_{idx+1}.csv"
                                csv = table.to_csv(index=False).encode('utf-8')
                                st.download_button(
                                    label="Download CSV",
                                    data=csv,
                                    file_name=csv_filename,
                                    mime='text/csv'
                                )
                    else:
                        st.info("No tables found on this page.")

            st.balloons()
        else:
            st.warning("⚠️ Please enter at least one URL to proceed.")


if __name__ == "__main__":
    main()
