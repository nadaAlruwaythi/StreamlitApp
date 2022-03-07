import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Speech-to-Text Transcription App", layout="wide"
)


def _max_width_():
    max_width_str = f"max-width: 1200px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )

_max_width_()

st.image("mo.jpg", width=350)

def main():
    pages = {
        "👾 Free mode (2MB per API call)": demo,
        "🤗 Full mode": API_key,
    }

    if "page" not in st.session_state:
        st.session_state.update(
            {
                # Default page
                "page": "Home",
            }
        )

    with st.sidebar:
        page = st.radio("Select your mode", tuple(pages.keys()))

    pages[page]()
    
f = st.file_uploader("", type=[".wav"])

st.info(
                f"""
                        👆 Upload a .wav file. Or try a sample: [Wav sample 01](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/Welcome.wav?raw=true) | [Wav sample 02](https://github.com/CharlyWargnier/CSVHub/blob/main/Wave_files_demos/The_National_Park.wav?raw=true)
                        """
            )


if f is not None:
        path_in = f.name
        # Get file size from buffer
        # Source: https://stackoverflow.com/a/19079887
        old_file_position = f.tell()
        f.seek(0, os.SEEK_END)
        getsize = f.tell()  # os.path.getsize(path_in)
        f.seek(old_file_position, os.SEEK_SET)
        getsize = round((getsize / 1000000), 1)
        st.caption("The size of this file is: " + str(getsize) + "MB")

        if getsize < 2:  # File more than 2MB
            st.success("OK, less than 1 MB")
            
        else:
            st.error("More than 1 MB! Please use your own API")
            st.stop()
    
headers = {"Authorization": f"Bearer {api_token}"}
API_URL = "https://api-inference.huggingface.co/models/kmfoda/wav2vec2-large-xlsr-arabic"

def query(data):
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

data = query(bytes_data)
# Extract the dictionary values

values_view = data.values()
value_iterator = iter(values_view)
text_value = next(value_iterator)

# Convert all cases to lowercase

text_value = text_value.lower()

# Print the output to your Streamlit app

st.success(text_value)