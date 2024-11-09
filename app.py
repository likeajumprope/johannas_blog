import streamlit as st
import pandas as pd
import numpy as np
import os
from markdown import markdown
import importlib


def load_post(filepath):
    """Load blog-style post metadata and content."""
    with open(filepath, "r") as file:
        lines = file.readlines()
        title = lines[0].strip().replace("# ", "")
        image_url = lines[1].strip().replace("image: ", "")
        summary = lines[2].strip().replace("summary: ", "")
        content = markdown("".join(lines[4:]))
        return {"title": title, "image": image_url, "summary": summary, "content": content}


# Load all data demo posts
data_post_files = [os.path.join("data_posts", f) for f in os.listdir("data_posts") if f.endswith(".md")]
data_posts = [load_post(post) for post in data_post_files]

# Initialize session state for selected data demo post
if "selected_data_demo" not in st.session_state:
    st.session_state.selected_data_demo = None

def select_data_post(post_index):
    """Select a specific data demo post."""
    st.session_state.selected_data_demo = post_index

def go_back_to_data_posts():
    """Go back to data demo list."""
    st.session_state.selected_data_demo = None
    
def load_model_demo(filepath):
    spec = importlib.util.spec_from_file_location("model_demo", filepath)
    model_demo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_demo)
    return model_demo

# Load model demos dynamically
model_files = [os.path.join("model_demos", f) for f in os.listdir("model_demos") if f.endswith(".py")]
model_demos = [{"name": os.path.splitext(os.path.basename(f))[0], "path": f} for f in model_files]

# Initialize session state for selected model
if "selected_model_demo" not in st.session_state:
    st.session_state.selected_model_demo = None

def select_model_demo(index):
    st.session_state.selected_model_demo = index

def go_back_to_model_list():
    st.session_state.selected_model_demo = None

# Load all blog posts
post_files = [os.path.join("posts", f) for f in os.listdir("posts") if f.endswith(".md")]
blog_posts = [load_post(post) for post in post_files]

# Initialize session state for selected blog post
if "selected_post" not in st.session_state:
    st.session_state.selected_post = None

def select_post(post_index):
    """Select a specific blog post."""
    st.session_state.selected_post = post_index

def go_back_to_posts():
    """Go back to blog post summaries."""
    st.session_state.selected_post = None



# Sidebar Navigation
st.sidebar.title("Navigation")
tab = st.sidebar.selectbox("Go to", ["Home", "Blog", "Data Demo", "Model Demo", "CV"])

# Data Demo Tab
if tab == "Data Demo":
    if st.session_state.selected_data_demo is not None:
        # Display selected data demo post
        post = data_posts[st.session_state.selected_data_demo]
        st.title(post["title"])
        st.image(post["image"], use_column_width=True)
        st.write(post["content"], unsafe_allow_html=True)

        # Add dynamic data visualization (example based on post content)
        if "sample dataset" in post["content"].lower():
            data = pd.DataFrame({
                'Category': ['A', 'B', 'C', 'D'],
                'Values': np.random.randint(1, 100, 4)
            })
            st.write("Here's a sample dataset:")
            st.write(data)
            st.bar_chart(data.set_index('Category'))
        
        st.button("Back to Data Posts", on_click=go_back_to_data_posts)
    
    else:
        st.title("Data Demo Posts")

        col1, col2 = st.columns(2)
        for i, post in enumerate(data_posts):
            col = col1 if i % 2 == 0 else col2
            with col:
                st.image(post["image"], use_column_width=True)
                st.subheader(post["title"])
                st.write(post["summary"])
                st.button("Read More", key=f"data_read_more_{i}", on_click=select_data_post, args=(i,))

# Other Tabs
elif tab == "Home":
    st.title("Welcome to My Website!")
    st.image("https://via.placeholder.com/800x300", caption="Sample Banner")

elif tab == "Blog":
    if st.session_state.selected_post is not None:
        # Display the selected blog post
        post = blog_posts[st.session_state.selected_post]
        st.title(post["title"])
        st.image(post["image"], use_column_width=True)
        st.write(post["content"], unsafe_allow_html=True)
        
        # Back button
        st.button("Back to Blog Posts", on_click=go_back_to_posts)
    else:
        # Display all blog post summaries
        st.title("Blog Posts")
        col1, col2, col3 = st.columns(3)
        for i, post in enumerate(blog_posts):
            col = [col1, col2, col3][i % 3]  # Distribute posts across columns
            with col:
                st.markdown(f"""
                <div class="card">
                    <h2>{post["title"]}</h2>
                    <img src="{post['image']}" style="width:100%; border-radius:8px; margin-bottom:10px;">
                    <p>{post["summary"]}</p>
                </div>
                """, unsafe_allow_html=True)
                st.button("Read More", key=f"read_more_{i}", on_click=select_post, args=(i,))
    
                
elif tab == "Model Demo":
    if st.session_state.selected_model_demo is not None:
        demo = model_demos[st.session_state.selected_model_demo]
        model_demo = load_model_demo(demo["path"])
        model_demo.run()  # Call the `run()` function in the selected demo
        st.button("Back to Model List", on_click=go_back_to_model_list)
    else:
        st.title("Model Demos")
        for i, demo in enumerate(model_demos):
            st.button(demo["name"].replace("_", " ").title(), key=f"model_demo_{i}", on_click=select_model_demo, args=(i,))
    st.title("Model Demo")
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    st.line_chart(pd.DataFrame({"x": x, "y": y}).set_index("x"))

st.sidebar.write("(C) Johanna Bayer, 2024")


