# Advanced Web Search using SERPAPI

This Streamlit application allows users to perform advanced web searches using the SERPAPI service. Users can select target regions and areas, add additional search terms, and save selected search results to a CSV file.

## Features

- **Region Selection**: Choose from predefined regions to narrow down your search.
- **Target Areas**: Select specific target areas for more focused search results.
- **Additional Search Terms**: Add custom terms to refine your search query.
- **Save Results**: Select and save search results to a CSV file with region and timestamp.
- **Customizable Summary Length**: Adjust the character length of result summaries through the UI.

## Prerequisites

- Python 3.7 or higher
- A SERPAPI API key. You can get one from [SERPAPI](https://serpapi.com).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pleabargain/streamlit-serpapi-search.git
   cd streamlit-serpapi-search
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and add your SERPAPI API key:
   ```
   SERPAPI_KEY=your_serpapi_key_here
   ```

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and go to `http://localhost:8501`.

3. **Select Regions**: Choose the regions you want to include in your search.

4. **Select Target Areas**: Pick the target areas relevant to your search.

5. **Additional Search Terms**: Enter any additional terms to refine your search.

6. **Customize Display**: Adjust the number of results and summary length using the sliders.

7. **Enter API Key**: Input your SERPAPI API key in the sidebar if not already set in the `.env` file.

8. **Search**: Click the "Search" button to perform the search.

9. **Select Results**: Use the checkboxes to select the results you want to save.

10. **Save Results**: Click "Save Selected Results" to save the selected results to a CSV file. The file will be named in the format: `region_query_timestamp.csv`.

## File Naming Convention

Files are saved with the following format:
- `region_query_timestamp.csv`
Example: `saudi_arabia_outbound_luxury_travel_20241118_135027.csv`

## Notes

- Ensure your SERPAPI API key is valid and has sufficient quota for the searches.
- The application uses session state to maintain search results across interactions.
- Search results can be selected and saved without page refreshes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Source Repository

This project is available at [github.com/pleabargain/streamlit-serpapi-search](https://github.com/pleabargain/streamlit-serpapi-search)