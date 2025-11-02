# app.py
import streamlit as st
from faces import encode_known_faces, recognize_faces_in_image, save_uploaded_file
from PIL import Image
import os
import tempfile

st.set_page_config(page_title="Streamlit Face Recognition", layout="wide")
st.title("Face Recognition — Streamlit demo")

st.markdown(
    """
    Upload labeled images of *known* people (one person per image, filename = label).
    Then upload an image to recognize faces.
    """
)

KNOWN_DIR = "known_faces"
os.makedirs(KNOWN_DIR, exist_ok=True)

st.sidebar.header("1) Add known faces")
uploaded_known = st.sidebar.file_uploader(
    "Upload an image of a known person (filename used as label)", type=["jpg","jpeg","png"], accept_multiple_files=True
)
if uploaded_known:
    for up in uploaded_known:
        save_uploaded_file(up, KNOWN_DIR)
    st.sidebar.success(f"Saved {len(uploaded_known)} known face file(s).")

st.sidebar.markdown("---")
if st.sidebar.button("(Re)load known faces encodings"):
    with st.spinner("Encoding known faces..."):
        n = encode_known_faces(KNOWN_DIR)
    st.sidebar.success(f"Encoded {n} known face(s).")

st.sidebar.markdown("---")
st.sidebar.header("Deploy / Notes")
st.sidebar.markdown(
    """
- This demo stores uploaded images in the repo folder while running.
- For production, store known faces in secure storage and never expose private data.
"""
)

st.header("2) Recognize faces in a test image")
test_file = st.file_uploader("Upload a test image", type=["jpg","jpeg","png"])
if test_file is not None:
    with st.spinner("Running face recognition..."):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        tmp.write(test_file.getbuffer())
        tmp.flush()
        tmp.close()
        pil_img = Image.open(tmp.name).convert("RGB")
        annotated_path, matches = recognize_faces_in_image(tmp.name)
        st.image(pil_img, caption="Input image", use_column_width=True)
        st.subheader("Recognized faces")
        if not matches:
            st.info("No faces recognized (or no known faces encoded).")
        else:
            for i,(name,dist) in enumerate(matches):
                st.write(f"{i+1}. {name} (distance {dist:.3f})")
