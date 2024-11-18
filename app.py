import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Get default API key from environment
DEFAULT_API_KEY = os.getenv('SERPAPI_KEY', '')

# Configuration and constants
REGIONS = {
    "Poland": "pl",
    "Czech Republic": "cz",
    "Romania": "ro",
    "France": "fr",
    "Saudi Arabia": "sa",
}

TARGETS = {
    "luxury travel market": "luxury travel market trends analysis",
    "outbound luxury travel": "outbound luxury travel market trends analysis",
    "airline news": "airline industry news updates",
    "exclusive travel": "exclusive VIP travel experiences premium"
}

def truncate_summary(text, max_words=50):
    """
    Truncate summary to specified number of words and add ellipsis if needed
    """
    words = text.split()
    if len(words) <= max_words:
        return text
    return ' '.join(words[:max_words]) + '...'

def search_serpapi(query, api_key, num_results=10, region=None):
    """
    Perform a search using SERPAPI and return results
    """
    base_url = "https://serpapi.com/search"
    
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": num_results,
    }
    
    if region:
        params["gl"] = region
        params["hl"] = "en"
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        results = data.get("organic_results", [])
        
        processed_results = []
        for result in results[:num_results]:
            summary = truncate_summary(result.get("snippet", "No summary available"))
            
            processed_results.append({
                "selected": False,  # Add checkbox column
                "title": result.get("title", "No title"),
                "summary": summary,
                "url": result.get("link", "No URL available")
            })
            
        return processed_results
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error making API request: {str(e)}")
        return []
    except KeyError as e:
        st.error(f"Error processing API response: {str(e)}")
        return []

def build_search_query(selected_regions, selected_targets, additional_terms=""):
    """
    Build a search query based on selected options and additional terms
    """
    query_parts = []
    
    for target in selected_targets:
        query_parts.append(TARGETS[target])
    
    region_terms = [f"in {region}" for region in selected_regions]
    if region_terms:
        query_parts.append(" OR ".join(region_terms))
    
    if additional_terms:
        query_parts.append(additional_terms)
    
    return " ".join(query_parts)

def save_selected_results(df, search_query, selected_regions):
    """
    Save selected results to a CSV file with region, query and timestamp
    Format: region_query_timestamp.csv
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Get region string (combine multiple regions with underscore)
    region_str = "_".join(selected_regions) if selected_regions else "global"
    region_str = region_str.lower().replace(' ', '_')
    
    # Clean the search query to make it filename-friendly
    clean_query = "".join(x for x in search_query[:30] if x.isalnum() or x in (' ', '-', '_')).strip()
    clean_query = clean_query.replace(' ', '_')
    
    # Remove common words and phrases to keep filename shorter
    words_to_remove = ['market', 'trends', 'analysis', 'in']
    for word in words_to_remove:
        clean_query = clean_query.replace(word, '')
    
    # Clean up any double underscores that might have been created
    clean_query = '_'.join(filter(None, clean_query.split('_')))
    
    filename = f"{region_str}_{clean_query}_{timestamp}.csv"
    
    # Filter selected rows and remove the 'selected' column
    selected_df = df[df['selected']].drop('selected', axis=1)
    
    # Save both metadata and results
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Search Query: {search_query}\n")
        f.write(f"# Regions: {', '.join(selected_regions)}\n")
        f.write(f"# Timestamp: {timestamp}\n")
        f.write("#" + "=" * 50 + "\n")
    
    # Append the actual results
    selected_df.to_csv(filename, mode='a', index=False)
    
    return filename

def main():
    st.set_page_config(layout="wide")
    
    st.title("Advanced Web Search using SERPAPI")
    
    # Move the region selection here
    st.write("Select Regions:")
    region_cols = st.columns(len(REGIONS))
    selected_regions = []
    for col, (region, _) in zip(region_cols, REGIONS.items()):
        if col.checkbox(region, key=f"region_{region}", help=f"Search in {region}"):
            selected_regions.append(region)
    
    # Create a horizontal line for visual separation
    st.markdown("---")
    
    # Create columns for targets
    st.write("Select Target Areas:")
    target_cols = st.columns(len(TARGETS))
    selected_targets = []
    for col, (target, _) in zip(target_cols, TARGETS.items()):
        if col.checkbox(target, key=f"target_{target}", help=f"Search for {target}"):
            selected_targets.append(target)
    
    # Separator
    st.markdown("---")
    
    # API key moved to sidebar
    with st.sidebar:
        api_key = st.text_input("Enter your SERPAPI API key:", 
                               value=DEFAULT_API_KEY,
                               type="password")
    
    # Search interface
    search_col1, search_col2 = st.columns([3, 1])
    
    with search_col1:
        additional_terms = st.text_input(
            "Additional search terms:",
            help="Add specific terms to refine your search"
        )
    
    with search_col2:
        num_results = st.slider(
            "Number of results:",
            min_value=1,
            max_value=20,
            value=10
        )
        summary_length = st.slider(
            "Summary length (characters):",
            min_value=100,
            max_value=1000,
            value=300,
            step=50
        )
    
    # Build and display the search query
    if selected_regions or selected_targets:
        search_query = build_search_query(selected_regions, selected_targets, additional_terms)
        st.text_area("Generated search query:", search_query, disabled=True)
    
    # Initialize session state for search results
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None

    if st.button("Search", type="primary"):
        if not api_key:
            st.error("Please enter your SERPAPI API key in the sidebar.")
            return
            
        if not (selected_regions or selected_targets or additional_terms):
            st.error("Please select at least one region, target area, or enter search terms.")
            return
            
        with st.spinner("Searching..."):
            region_code = REGIONS[selected_regions[0]] if selected_regions else None
            results = search_serpapi(search_query, api_key, num_results, region_code)
            
            if results:
                st.session_state.search_results = pd.DataFrame(results)
            else:
                st.warning("No results found or an error occurred.")
    
    # Display results if available
    if st.session_state.search_results is not None:
        df = st.session_state.search_results
        
        st.subheader("Search Results")
        
        # Custom CSS for table formatting
        st.markdown("""
        <style>
            .stDataFrame td {
                white-space: normal !important;
                min-width: 150px;
            }
            .stDataFrame th {
                white-space: normal !important;
                min-width: 150px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Make DataFrame editable for checkboxes
        edited_df = st.data_editor(
            df,
            column_config={
                "selected": st.column_config.CheckboxColumn(
                    "Select",
                    help="Select to save",
                    default=False,
                ),
                "title": st.column_config.Column(
                    "Title",
                    width="medium",
                ),
                "summary": st.column_config.TextColumn(
                    "Summary",
                    width="large",
                    max_chars=summary_length
                ),
                "url": st.column_config.LinkColumn(
                    "URL",
                    width="medium",
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Add save button
        if st.button("Save Selected Results"):
            if edited_df['selected'].any():
                filename = save_selected_results(edited_df, search_query, selected_regions)
                st.success(f"Selected results saved to {filename}")
                
                # Provide download button
                with open(filename, 'r', encoding='utf-8') as f:
                    st.download_button(
                        label="Download CSV",
                        data=f.read(),
                        file_name=filename,
                        mime='text/csv'
                    )
            else:
                st.warning("Please select at least one result to save.")
    
    # Add usage instructions
    with st.sidebar.expander("How to use"):
        st.markdown("""
        1. Select target regions and areas at the top
        2. Add any additional search terms
        3. Click Search
        4. Select results using checkboxes
        5. Click 'Save Selected Results' to save to CSV
        
        Note: Your SERPAPI key is in the sidebar
        Get your key at: https://serpapi.com
        """)

if __name__ == "__main__":
    main()