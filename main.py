import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import random,os
from google.cloud import storage
#from google.oauth2 import service_account
from io import BytesIO
import gspread
import google.auth
from google.auth.transport.requests import Request

st.set_page_config(layout="wide")
# Initialize page state
if "page" not in st.session_state:
    st.session_state.page = 1

if 'end_survey' not in st.session_state:
    st.session_state.end_survey = False

if 'username' not in st.session_state:
    st.session_state.username = None

if 'starting_time' not in st.session_state:
    st.session_state.starting_time = None

if 'ending_time' not in st.session_state:
    st.session_state.ending_time = None#

if "q1" not in st.session_state: st.session_state.q1 = None
if "q2" not in st.session_state: st.session_state.q2 = None
if "q3" not in st.session_state: st.session_state.q3 = None
if "q4" not in st.session_state: st.session_state.q4 = None
if "q5" not in st.session_state: st.session_state.q5 = None
if "q6" not in st.session_state: st.session_state.q6 = None
if "q7" not in st.session_state: st.session_state.q7 = None
if "q8" not in st.session_state: st.session_state.q8 = None
if "q9" not in st.session_state: st.session_state.q9 = None


def next_page():
    st.session_state.page += 1

def last_page():
    st.session_state.end_survey = True
    #st.experimental_rerun()  # Rerun to finalize the survey

def prev_page():
    st.session_state.page -= 1

def reset():
    st.session_state.page = 1

def save_log(username, email, log_info):
    import gspread
    from google.auth import default

    # Define the required scopes
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # Get application default credentials with scopes
    creds, _ = default(scopes=SCOPES)

    # Authorize with gspread
    client = gspread.authorize(creds)

    # Open the target spreadsheet and worksheet
    sheet_id = '1vIn_wz9TwCiqzqAT3JV8E_84Ck_cHIiybvdDZgfcoug'
    worksheet = client.open_by_key(sheet_id).sheet1

    # Define the expected headers
    headers = [
        "Username",
        "Email",
        "Starting Time",
        "Ending Time",
        "Q1: Main Goal",
        "Q2: Areas of Support",
        "Q3: Main Method",
        "Q4: Metrics/Progress Markers",
        "Q5: Motivational Message",
        "Q6: Shape Style",
        "Q7: Visual Style",
        "Q8: Logo Uploads",
        "Q9: Visuals Uploads",
        "Feedback",
        "Comments"
    ]

    # Ensure header exists
    try:
        first_row = worksheet.row_values(1)
    except Exception:
        first_row = []

    if first_row != headers:
        if first_row:
            worksheet.delete_rows(1)
        worksheet.insert_row(headers, index=1)

    # Validate log_info length (excluding Username and Email)
    #expected_len = len(headers) - 2  # username + email are added separately
    #if not isinstance(log_info, list) or len(log_info) != expected_len:
    #    raise ValueError(f"log_info must be a list of {expected_len} elements.")


    data_row = [username, email] + log_info

    # Append the row
    worksheet.append_row(data_row)


def import_image_from_bucket(file_name):
    try:
        # Try loading ADC and project
        credentials, project = google.auth.default()
        print("[DEBUG] Credentials loaded.")
        print("[DEBUG] ADC project detected:", project)

        # If project still missing, fallback to env or hardcoded value
        if not project:
            project = os.getenv("GOOGLE_CLOUD_PROJECT", "bi-lenus-staging")
            print("[DEBUG] Falling back to default project:", project)

        # Initialize client with explicit credentials + project
        client = storage.Client(credentials=credentials, project=project)

        bucket = client.bucket("bi-lenus-staging")
        blob = bucket.blob(f"coach_app_survey/images/{file_name}")

        image_bytes = blob.download_as_bytes()
        return BytesIO(image_bytes)

    except Exception as e:
        print("[ERROR] Failed to import image from bucket:", str(e))
        raise


def upload_image_to_bucket(image_file, file_name, folder=""):
    try:
        credentials, project = google.auth.default()
        
        if not project:
            project = os.getenv("GOOGLE_CLOUD_PROJECT", "bi-lenus-staging")
            print("[DEBUG] Falling back to project:", project)

        client = storage.Client(credentials=credentials, project=project)

        bucket = client.bucket("bi-lenus-staging")
        blob_path = f"{folder}/{file_name}" if folder else file_name
        blob = bucket.blob(blob_path)

        blob.upload_from_file(image_file, rewind=True)
        print(f"[INFO] Uploaded {file_name} to {blob_path}")
        return blob.public_url

    except Exception as e:
        print("[ERROR] Failed to upload image to bucket:", e)
        raise


#importing needed images
if "image_1_stream" not in st.session_state:
    st.session_state.image_1_stream = import_image_from_bucket('img1.png')
if "image1" not in st.session_state:
    st.session_state.image1 = Image.open(st.session_state.image_1_stream)
# import more images below
if "image_2_stream" not in st.session_state:
    st.session_state.image_2_stream = import_image_from_bucket('Image2.png')
if "Image2" not in st.session_state:
    st.session_state.Image2 = Image.open(st.session_state.image_2_stream)

if "image_3_stream" not in st.session_state:
    st.session_state.image_3_stream = import_image_from_bucket('Round_1.png')
if "Round_1" not in st.session_state:
    st.session_state.image3 = Image.open(st.session_state.image_3_stream)

if "image_4_stream" not in st.session_state:
    st.session_state.image_4_stream = import_image_from_bucket('Round_2.png')
if "Round_2" not in st.session_state:
    st.session_state.image4 = Image.open(st.session_state.image_4_stream)

if "image_5_stream" not in st.session_state:
    st.session_state.image_5_stream = import_image_from_bucket('Round_3.png')
if "Round_3" not in st.session_state:
    st.session_state.image5 = Image.open(st.session_state.image_5_stream)

if "image_6_stream" not in st.session_state:
    st.session_state.image_6_stream = import_image_from_bucket('visual.png')
if "visual" not in st.session_state:
    st.session_state.image6 = Image.open(st.session_state.image_6_stream)

if "image_7_stream" not in st.session_state:
    st.session_state.image_7_stream = import_image_from_bucket('layout_1.png')
if "layout_1" not in st.session_state:
    st.session_state.image7 = Image.open(st.session_state.image_7_stream)

if "image_8_stream" not in st.session_state:
    st.session_state.image_8_stream = import_image_from_bucket('layout_2.png')
if "layout_2" not in st.session_state:
    st.session_state.image8 = Image.open(st.session_state.image_8_stream)   

if "image_9_stream" not in st.session_state:
    st.session_state.image_9_stream = import_image_from_bucket('layout_3.png')
if "layout_3" not in st.session_state:
    st.session_state.image9 = Image.open(st.session_state.image_9_stream)   

# Define total number of pages
total_pages = 12  # adjust based on how many you have

# Draw progress dots
dots_html = """
<style>
.dot-progress {{
    display: flex;
    gap: 6px;
    margin-bottom: 1.5rem;
}}
.dot {{
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: #ddd;
}}
.dot.active {{
    background-color: #294f4f;
}}
</style>
<div class="dot-progress">
{}
</div>
"""

# Generate dots with current page highlighted
dot_elements = ""
for i in range(total_pages):
    if (i+1) == st.session_state.page:
        dot_elements += '<div class="dot active"></div>'
    else:
        dot_elements += '<div class="dot"></div>'

# Show the dots
st.markdown(dots_html.format(dot_elements), unsafe_allow_html=True)

# Custom CSS for buttons and other elements
st.markdown("""
            <style>
            div.stButton > button {
            background-color: #375c5a;
            color: white;
            padding: 0.6rem 1.5rem;
            font-size: 1.1rem;
            font-weight: 600;
            border: none;
            border-radius: 999px;
            cursor: pointer;
            text-align: center;
            transition: background-color 0.2s ease-in-out;
            }

            div.stButton > button:hover {
            background-color: white;
            color: #375c5a;
            }
            div.stButton > button:active {
            background-color: white; !important; /* Keep the hover color on click */
            color: #375c5a; !important; /* Keep the hover color on click */
            }
            </style>
            """, unsafe_allow_html=True)

# Custom CSS for radio buttons, select boxes, and checkboxes
st.markdown("""
    <style>
    /* Change radio button text and selected circle */
    div.row-widget.stRadio > div {
        color: #375c5a;
    }

    /* Make the selected radio circle green */
    div.stRadio [role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
        background-color: #375c5a !important;
        border-color: #375c5a !important;
    }

    /* Change selectbox border and text color */
    .stSelectbox div[data-baseweb="select"] > div {
        color: #375c5a;
        border-color: #375c5a !important;
    }

    /* Optional: change checkboxes */
    div.stCheckbox > label {
        color: #375c5a;
    }

    div.stCheckbox > label > div:first-child {
        border-color: #375c5a !important;
        background-color: #375c5a !important;
    }
    

    div.stCheckbox > label > div:first-child:hover {
        border-color: #2e4f4d !important;
    }

    div.stCheckbox input:checked + div:first-child {
        background-color: #375c5a !important;  /* Checkbox fill when checked */
        border-color: #375c5a !important;
    }

    /* Target the checkbox box */
    input[type="checkbox"] {
    accent-color: #375c5a !important;
    }

    /* Override the red background used in some browsers when checked */
    input[type="checkbox"]:checked {
    background-color: #375c5a !important;
    border-color: #375c5a !important;
    }

    input[type="checkbox"]:checked::before {
    background-color: #375c5a !important;
    color: white !important;
    }
        
    .stMarkdown p {
        color: #375c5a;  /* Caption text */
    }
        
    /* Selected radio label */
    div[data-baseweb="radio"] label[data-selected="true"] {
    background-color: #375c5a !important;
    border: 2px solid #375c5a !important;
    color: white !important;
    font-weight: bold;
    border-radius: 8px !important;
    transition: background-color 0.3s ease;
    }

    /* Unselected radio labels */
    div[data-baseweb="radio"] label {
    border: 1px solid #375c5a !important;
    border-radius: 8px !important;
    color: #375c5a !important;
    padding: 0.5rem;
    }

    /* Hover effect */
    div[data-baseweb="radio"] label:hover {
    background-color: #d3e5e5 !important;
    border-color: #375c5a !important;
    color: #375c5a !important;
    }

    /* Text inside the label */
    div[data-baseweb="radio"] label > div:nth-child(2) {
    color: inherit !important;
    }

    /* Selected checkmark inside radio (fix for some browsers) */
    div[data-baseweb="radio"] svg {
    color: white !important;
    }
            
    </style>
    """, unsafe_allow_html=True)



# Page 1: Intro
if st.session_state.page == 1:
    body = ''' 
        To create a tailored, aligned experience for your branded app that reflects your values, philosophy and client journey, we’ll need your input.

        You’ll be guided through a series of questions covering your core offering, method of working with clients and visual preferences. You’ll also have the opportunity to share visuals to be used in the app. 

        Together with the brand information already provided, this input will form the foundation of our design process. The app’s structure, styling, and feature priorities will be based on the direction you provide here. While adjustments can be made later, we encourage you to answer thoughtfully, as your responses will directly influence the design choices.

        We’ll treat this information as our creative guide. Our goal is to stay as true to your preferences as possible. In some cases, we may suggest adjustments if something doesn’t fully align with your brand or if the right assets aren’t available.
        '''
    
    col1, col2 = st.columns(2)
    st.session_state.starting_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with col1:

        st.header("Designing an app that reflects your brand\n\n")
        st.write(body)

        # Email input
        email = st.text_input(
            "Please enter your email address to continue:")
        
        if email:
        # Basic email format validation
            if "@" in email:
                username = email.split("@")[0]
                st.session_state.email = email
                st.session_state.username = username
                st.success(f"Welcome, {username}!")
            else:
                st.warning("Please enter a valid email address")
        
        if email and '@' in email:
            st.button("Start →", on_click=next_page)

    

    with col2:
        st.image(st.session_state.image1, use_container_width=True)
            

# Page 2: Question 1
elif st.session_state.page == 2:
    if "options_q1" not in st.session_state: 
        st.session_state.options_q1 = [
        "Lose weight", 
        "Weight Gain",
        "Mind & Lifestyle (E.g. reduce stress, develop mindful habits, improve sleep and energy)",
        "After pregnancy recovery (E.g train for a race, master specific movement...)",
        "Recovery after injury",
        "Activity & Performance Goals"
        ]
        random.shuffle(st.session_state.options_q1)
        st.session_state.options_q1 += ["Other"]

    col_left, col_right = st.columns(2)
    #random.shuffle(options)


    with col_left:
        st.header("What is the main goal or transformation your clients typically work towards with you?\n\n")
        st.session_state.q1 = st.radio( "Pick the one that best represents your coaching focus:", st.session_state.options_q1)
        if st.session_state.q1 == 'Other':
            # Inject style to collapse space
            st.markdown("""
                 <style>
                 div[data-testid="stTextInput"] {
                      margin-top: -35px;}
                 </style>""", unsafe_allow_html=True)
            other_input = st.text_input("", placeholder="Please specify")
            st.session_state.q1 += f": {other_input}"
        
        # Navigation buttons
        nav1, _, nav2 = st.columns([3, 1, 2])
        with nav1:
            st.button("← Back", on_click=prev_page)

        with nav2:
            st.button("Next →", on_click=next_page)
    with col_right:
        st.image(st.session_state.image1, use_container_width=True)

        

# Page 3: Question 2
elif st.session_state.page == 3:
    # Styling block to paste ABOVE your checkboxes
    st.markdown("""
<style>
/* White default checkbox */
div[data-baseweb="checkbox"] > div:first-child {
    background-color: white !important;
    border: 2px solid #375c5a !important;
    border-radius: 6px !important;
}

/* Green background when checked */
div[data-baseweb="checkbox"] input:checked + div {
    background-color: #375c5a !important;
    border-color: #375c5a !important;
}

/* White checkmark inside */
div[data-baseweb="checkbox"] svg {
    color: white !important;
    fill: white !important;
}

/* Optional: green label text when checked */
div[data-baseweb="checkbox"] input:checked + div > div {
    color: #375c5a !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

    import random

    if 'selected_areas' not in st.session_state:
        st.session_state.selected_areas = []

    col_left, col_right = st.columns(2)

    with col_left:

        if 'options_p3' not in st.session_state:
            st.session_state.options_p3 = [
                ("Nutrition", "Nutrition plans, inspiration, tips, food logs"),
                ("Workouts & Guided Sessions", "Exercise plans, yoga videos, meditations, breathing sessions"),
                ("Habits & Routines", "Daily or weekly habit tracking"),
                ("Journaling & mindfulness", "Daily reflections or writing prompts, mental clarity"),
                ("Community", "Group discussions, support chats"),
                ("Personal chat", "Direct communication with your clients"),
            ]

        st.header("Which of these areas do you actively support your clients with — through tools, practices, or ongoing interaction?")
        st.write('')
        st.write('We’ll use your answers to create key sections in your app where clients can engage, take action, and track their progress.')
        st.write('For example: if you guide clients in journaling or mental clarity, choose "Journaling & Mindfulness." But if you only mention it occasionally in your content, you can skip it.')
        st.write('')

        # Render checkboxes
        for label, desc in st.session_state.options_p3:
            key = f"checkbox_{label}"
            checked = st.checkbox(f"**{label}**", key=key)
            st.caption(desc)
            if checked and label not in st.session_state.selected_areas:
                st.session_state.selected_areas.append(label)
            elif not checked and label in st.session_state.selected_areas:
                st.session_state.selected_areas.remove(label)

        # Save result
        st.session_state.q2 = st.session_state.selected_areas

        # Navigation buttons
        nav1, _, nav2 = st.columns([3, 1, 2])
        with nav1:
            st.button("← Back", on_click=prev_page)
        with nav2:
            st.button("Next →", on_click=next_page)

    with col_right:
        st.image(st.session_state.image1, use_container_width=True)


# Page 4: Question 3
elif st.session_state.page == 4:

    import random
    # Debug display
    #st.markdown("### Debug: Selected areas from Page 3")
    #st.write(st.session_state.q2)

    # Always recalculate based on latest Page 3 selections
    selected_areas = st.session_state.q2 or []
    initial_q = []

    if 'Nutrition' in selected_areas:
        initial_q.append("You provide nutrition plans, inspiration or guides and task client to track nutrition")

    if 'Workouts & Guided Sessions' in selected_areas:
        initial_q.extend([
        "You offer exercise plans, yoga or video sessions",
        "You offer meditation or breathing sessions"
        ])

    if "Journaling & mindfulness" in selected_areas:
        initial_q.extend([
        "You guide clients in journaling & self reflection",
        "You offer meditation or breathing sessions"
        ])

    if "Habits & Routines" in selected_areas:
        initial_q.append("You help clients build small habits and daily routines")

    if "Community" in selected_areas:
        initial_q.append("You facilitate community interaction and group motivation")

    # Always show these options
    initial_q.extend([
        "You provide educational content through lessons, articles, videos, or structured learning",
        "You motivate clients through time based challenges and structured programs",
        "Other"
    ])

    # Deduplicate and assign
    st.session_state.initial_q = initial_q
    st.session_state.options_p4 = list(dict.fromkeys(initial_q))

    col1, col2 = st.columns(2)
    with col1:
        st.header("What is your main method or offering to help clients reach their goals?")
        st.markdown(
            "_You may support clients in many ways — here, select the method or area that plays the biggest role in your work. "
            "This helps us understand how your app should be structured to highlight your key offering._"
        )

        selected = st.radio(
            "Pick the one that best represents your coaching focus:",
            st.session_state.options_p4
        )

        if selected == "Other":
            other_input = st.text_input("", placeholder="Please specify")
            if other_input:
                st.session_state.q3 = f"Other: {other_input}"
            else:
                st.session_state.q3 = "Other"
        else:
            st.session_state.q3 = selected

        # Navigation buttons
        nav1, _, nav2 = st.columns([3, 1, 2])
        with nav1:
            st.button("← Back", on_click=prev_page)
        with nav2:
            st.button("Next →", on_click=next_page)

    with col2:
        st.image(st.session_state.image1, use_container_width=True)

# Page 5: Question 4 – Metrics / Progress Markers
elif st.session_state.page == 5:
    # Debug: Show selected areas from Page 3
    #st.markdown("### 🐛 Debug Info")
    #st.write("Selections from Page 3 (`q2`):")
    #st.write(st.session_state.q2)

    if "q4" not in st.session_state or st.session_state.q4 is None:
        st.session_state.q4 = []

    
    selected_areas = st.session_state.q2 or []
    metrics = {}

    # Nutrition
    if "Nutrition" in selected_areas:
        metrics["🥦 Nutrition & Hydration"] = [
            "Nutrition tracking / adherence to plan",
            "Water intake"
        ]
    else:
        metrics["🥦 Nutrition & Hydration"] = [
            "Water intake"
        ]

    # Body Metrics (only visible if Workouts selected)
    if "Workouts & Guided Sessions" in selected_areas:
        metrics["📊 Body Metrics"] = [
            "Weight",
            "Body circumference (e.g. waist, hips, arms)",
            "Body fat % or muscle mass"
        ]
    else:
        metrics["📊 Body Metrics"] = [
            "Weight"
        ]

    # Fitness & Activity
    if "Workouts & Guided Sessions" in selected_areas:
        metrics["💪 Fitness & Activity Metrics"] = [
            "Workout plan completion",
            "Max lifted weight",
            "Specific exercise performance",
            "Steps",
            "Running",
            "Active time",
            "Burned calories"
        ]
    else:
        # Still always show steps and running under fitness if not selected
        metrics["💪 Fitness & Activity Metrics"] = [
            "Steps",
            "Running",
            "Active time",
            "Burned calories"
        ]

    # Habit Metrics
    metrics["🔁 Habit & Consistency Metrics"] = []
    if "Habits & Routines" in selected_areas:
        metrics["🔁 Habit & Consistency Metrics"].append("Habit completion")
        metrics["🔁 Habit & Consistency Metrics"].append("Overall consistency - days with any log")
    else:
        metrics["🔁 Habit & Consistency Metrics"].append("Overall consistency - days with any log")

    # Lifestyle Metrics
    if "Journaling & mindfulness" in selected_areas:
        metrics["🧘 Well-being & Lifestyle Metrics"] = [
            "Reflections logged",
            "Energy levels",
            "Stress or mood levels",
            "Sleep quality"
        ]

    # Other (always show)
    metrics[""] = ["Other"]

    st.session_state.metrics_options = metrics

    col1, col2 = st.columns(2)
    with col1:
        # UI
        st.header("Which of these metrics / progress markers do you want your clients to focus on the most?")
        st.markdown("_We’ll use your selection to highlight the most important metrics in your app — helping your clients stay focused, motivated, and aligned with their progress._")

        for section, items in st.session_state.metrics_options.items():
            if section:
                st.markdown(f"**{section}**")
            for item in items:
                key = f"q4_{item}"
    
                if item == "Other":
                    checked = st.checkbox("Other", key=key)
                    if checked:
                        other_input = st.text_input(label="", placeholder="Please specify", key="q4_other_input")
                        if other_input:
                            full_other = f"Other: {other_input}"
                            if full_other not in st.session_state.q4:
                                st.session_state.q4.append(full_other)
                        # Remove old entries if unchecked or cleared
                        else:
                            st.session_state.q4 = [opt for opt in st.session_state.q4 if not opt.startswith("Other:")]
                    else:
                        st.session_state.q4 = [opt for opt in st.session_state.q4 if not opt.startswith("Other:")]
    
                else:
                    checked = st.checkbox(item, key=key)
                    if checked and item not in st.session_state.q4:
                        st.session_state.q4.append(item)
                    elif not checked and item in st.session_state.q4:
                        st.session_state.q4.remove(item)

        nav1, _, nav2 = st.columns([3, 1, 2])
        with nav1:
            st.button("← Back", on_click=prev_page)
        with nav2:
            st.button("Next →", on_click=next_page)

    with col2:
        st.image(st.session_state.image1, use_container_width=True)

# Page 6: Motivational Message
elif st.session_state.page == 6:
    if "q5" not in st.session_state:
        st.session_state.q5 = ""

    col1, col2 = st.columns(2)
    with col1:
        st.header("What’s a motivational phrase or message you'd like your clients to see in their app?")
        st.markdown(
          "_This will be shown on their main screen to inspire and remind them of your coaching tone or philosophy_"
        )
    
        st.session_state.q5 = st.text_area(
            "",
            placeholder='E.g. “Small steps every day lead to lasting change”',
            key="motivation_input",
            height=100
        )

        # Navigation buttons
        back_col, _, next_col = st.columns([3, 1, 2])
        with back_col:
            st.button("← Back", on_click=prev_page)
        with next_col:
            st.button("Next →", on_click=next_page)
    with col2:
        st.image(st.session_state.image1, use_container_width=True)

# Page 7: Shape style selection
elif st.session_state.page == 7:
    import random

    if "q6" not in st.session_state:
        st.session_state.q6 = None  # initialize as None

    # Handler to rerun app when selection changes
    #def update_image():
    #    st.experimental_rerun()

    shape_options = ["Less rounding", "Medium rounding", "More rounding"]

    col_left, col_right = st.columns(2)

    with col_left:
        st.header("What kind of shape style do you prefer for your app’s cards, buttons, and elements?")
        st.markdown("_This helps us set the overall feel of your app — soft and friendly, or clean and modern_")

        #st.session_state.q7 = st.radio("Select a shape style:", shape_options, index=shape_options.index(st.session_state.q7),
        #    key="q7",
        #    on_change=update_image)

        # Radio input with default to None
        shape_selected = st.radio("Select a shape style:", shape_options)
        st.session_state.q6 = shape_selected
        # Debug: Show current selection
        #st.write(f"Current selection: {st.session_state.q6}")


        # st.session_state.q6 = shape_selected  # Store the selection

        # Navigation buttons
        nav1, _, nav2 = st.columns([3, 1, 2])
        with nav1:
            st.button("← Back", on_click=prev_page)
        with nav2:
            st.button("Next →", on_click=next_page)

    with col_right:
        # Default image
        #image_to_show = st.session_state.get("Image2", None)
        if st.session_state.q6 == "Less rounding":
            st.image(st.session_state.image3)
        elif st.session_state.q6 == "Medium rounding":
            st.image(st.session_state.image4)
        elif st.session_state.q6 == "More rounding":
            st.image(st.session_state.image5)
        else:
            # Show default if nothing selected
            st.image(st.session_state.Image2, use_container_width=True)

# Page 8:Visual Style
elif st.session_state.page == 8:
    import random

    if "q7" not in st.session_state:
        st.session_state.q7 = None  # initialize as None

    layout_options = ["Classic layout", "Overlay layout", "Minimal layout"]

    col_left, col_right = st.columns(2)

    with col_left:
        st.header("What visual style best matches your branded app?")
        st.markdown("_Choose the layout style that best reflects your brand and how you want your content to be experienced. This will influence the overall structure and feel of your app's main screens_")

        visual_selected = st.radio("Select a visual style:", layout_options)
        st.session_state.q7 = visual_selected  # Store the selection

        # Navigation buttons
        nav1, _, nav2 = st.columns([3, 1, 2])
        with nav1:
            st.button("← Back", on_click=prev_page)
        with nav2:
            st.button("Next →", on_click=next_page)

    with col_right:

        if st.session_state.q7 == "Classic layout":
            st.image(st.session_state.image7)
        elif st.session_state.q7 == "Overlay layout":
            st.image(st.session_state.image8)
        elif st.session_state.q7 == "Minimal layout":
            st.image(st.session_state.image9)
        else:
            # Show default if nothing selected
            st.image(st.session_state.image6, use_container_width=True)

# Page 9: Upload your logos
elif st.session_state.page == 9:
    if "q8" not in st.session_state:
        st.session_state.q8 = None

    col1, col2 = st.columns(2)
    with col1:
        st.header("Upload your logo(s)")
        st.markdown(
        "**If you haven’t already shared your logo with Lenus, please upload it here**\n\n"
        "Please use a PNG or SVG with transparent background (no solid boxes).\n"
        "If you have different versions for light and dark backgrounds, please upload both."
        )

        # --- Logo for light backgrounds ---
        st.markdown("#### Logo for light backgrounds")
        st.caption("Used on white or light sections — usually a darker or colored version")
        uploaded_light = st.file_uploader("Upload Light Logo", type=["png", "svg"], key="light_logo", label_visibility="collapsed")

        # --- Logo for dark backgrounds ---
        st.markdown("#### Logo for dark backgrounds")
        st.caption("Used on dark sections — usually a lighter version")
        uploaded_dark = st.file_uploader("Upload Dark Logo", type=["png", "svg"], key="dark_logo", label_visibility="collapsed")

        # --- Custom styles ---
        st.markdown("""
        <style>
        [data-testid="stFileUploader"] > label div {
            display: none;  /* Hide default text */
        }
        [data-testid="stFileUploader"] button {
            background-color: #e5efef;
            color: #375c5a;
            border: none;
            padding: 0.5rem 1.5rem;
            border-radius: 1.5rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: none;
            transition: all 0.2s ease-in-out;
        }
        [data-testid="stFileUploader"] button:hover {
            background-color: #d3e5e5;
        }
        </style>
        """, unsafe_allow_html=True)

        from datetime import datetime
        # --- Preview Uploaded Images ---
        if uploaded_light:
            st.success("Light logo uploaded!")
            st.image(uploaded_light, caption="Light Logo Preview", use_container_width=True)

            username = st.session_state.get("username", "anonymous")
            folder = f"coach_app_survey/user_uploads/{username}"

            # Upload to Google Cloud Storage
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            light_name = f"light_logo_{timestamp}_{uploaded_light.name}"
            light_path = upload_image_to_bucket(uploaded_light, light_name, folder=folder)
            
            if st.session_state.q8 is None:
                st.session_state.q8 = {}
            st.session_state.q8["light"] = light_path
            #st.caption(f"Stored at: `{light_path}`")


        if uploaded_dark:
            st.success("Dark logo uploaded!")
            st.image(uploaded_dark, caption="Dark Logo Preview", use_container_width=True)

            username = st.session_state.get("username", "anonymous")
            folder = f"coach_app_survey/user_uploads/{username}"


            # Upload to Google Cloud Storage
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            dark_name = f"dark_logo_{timestamp}_{uploaded_dark.name}"
            dark_path = upload_image_to_bucket(uploaded_dark, dark_name, folder=folder)

            if st.session_state.q8 is None:
                st.session_state.q8 = {}
            st.session_state.q8["dark"] = dark_path
            #st.caption(f"Stored at: `{dark_path}`")

        
        # --- Navigation buttons ---
        nav1, _, nav2 = st.columns([3, 1, 2])
        with nav1:
            st.button("← Back", on_click=prev_page)
        with nav2:
            st.button("Next →", on_click=next_page)

    # Right column image
    with col2:
        st.image(st.session_state.image1, use_container_width=True)

# Page 10: Upload Your Visuals
elif st.session_state.page == 10:
    if "q9" not in st.session_state:
        st.session_state.q9 = None
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("Upload Your Visuals")
        st.markdown(
            "To help personalize your app, we’ll use your brand imagery in key visual areas — "
            "where it fits best based on your layout and content. Please upload the following:"
        )

        # --- Image Uploaders ---
        # Portrait image
        st.markdown("#### Portrait Image")
        st.caption(
            "A square or slightly vertical portrait-style photo of you. This will be used in e.g. hero sections or welcome screens.\n"
            "Ideal size: 1000×1000px or larger"
        )
        portrait_img = st.file_uploader("Upload Portrait", type=["png", "jpg", "jpeg"], key="portrait", label_visibility="collapsed")
        
        # Background images
        st.markdown("#### Background images (up to 3 images)")
        st.caption(
            "Vertical lifestyle photos, you in action — anything that reflects your brand. "
            "These may be used in areas that support full-screen visuals (like splash or intro moments).\n"
            "Ideal size: 1080×1920px or larger"
        )
        background_imgs = st.file_uploader(
            "Upload Backgrounds", type=["png", "jpg", "jpeg"], key="backgrounds", label_visibility="collapsed", accept_multiple_files=True
        )

        # Content images
        st.markdown("#### Content images (up to 5 images)")
        st.caption(
            "Landscape or square supporting images to be used in content cards or features.\n"
            "Ideal size: 800×800px or larger"
        )
        content_imgs = st.file_uploader(
            "Upload Content Images", type=["png", "jpg", "jpeg"], key="content", label_visibility="collapsed", accept_multiple_files=True
        )

        # Note at the bottom
        st.markdown(
            "💡 *Not sure what to upload? You can skip any section — we’ll use matching placeholder visuals or brand colors in those cases, and you can update images later.*"
        )

        # Styling uploader buttons like previous step
        st.markdown("""
        <style>
        [data-testid="stFileUploader"] > label div {
        display: none;
        }
        [data-testid="stFileUploader"] button {
        background-color: #e5efef;
        color: #375c5a;
        border: none;
        padding: 0.5rem 1.5rem;
        border-radius: 1.5rem;
        font-weight: 600;
        cursor: pointer;
        box-shadow: none;
        transition: all 0.2s ease-in-out;
        }
        [data-testid="stFileUploader"] button:hover {
        background-color: #d3e5e5;
        }
        </style>
        """, unsafe_allow_html=True)


        from datetime import datetime
        # Upload portrait image to Google Cloud Storage
        if portrait_img:
            st.success("Portrait image uploaded!")
            st.image(portrait_img, caption="Portrait Image Preview", use_container_width=True)

            username = st.session_state.get("username", "anonymous")
            folder = f"coach_app_survey/user_uploads/{username}"
            # Upload to Google Cloud Storage
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            portrait_name = f"portrait_{timestamp}_{portrait_img.name}"
            portrait_path = upload_image_to_bucket(portrait_img, portrait_name, folder=folder)

            if st.session_state.q9 is None:
                st.session_state.q9 = {}
            st.session_state.q9['portrait'] = portrait_path  # Store path in session state
            #st.caption(f"Stored at: `{portrait_path}`")

        if background_imgs:
            st.success(f"{len(background_imgs)} background image(s) uploaded!")
            for img in background_imgs:
                st.image(img, use_container_width=True)

                username = st.session_state.get("username", "anonymous")
                folder = f"coach_app_survey/user_uploads/{username}"

                # Upload background images to Google Cloud Storage
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                background_name = f"background_{timestamp}_{img.name}"
                background_path = upload_image_to_bucket(img, background_name, folder=folder)

                if st.session_state.q9 is None: 
                    st.session_state.q9 = {}
                st.session_state.q9['backgrounds'] = background_path  # Store path in session state
                #st.caption(f"Stored at: `{background_path}`")

        
        if content_imgs:
            st.success(f"{len(content_imgs)} content image(s) uploaded!")
            for img in content_imgs:
                st.image(img, use_container_width=True)
                username = st.session_state.get("username", "anonymous")
                folder = f"coach_app_survey/user_uploads/{username}"

                # Upload content images to Google Cloud Storage
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                content_name = f"content_{timestamp}_{img.name}"
                content_path = upload_image_to_bucket(img, content_name, folder=folder)

                if st.session_state.q9 is None:
                    st.session_state.q9 = {}
                st.session_state.q9['content'] = content_path  # Store path in session state
                #st.caption(f"Stored at: `{content_path}`")

        
        # Navigation
        nav1, _, nav2 = st.columns([3, 1, 2])
        with nav1:
            st.button("← Back", on_click=prev_page)
        with nav2:
            st.button("Next →", on_click=next_page)
    with col2:
        st.image(st.session_state.image1)

# Page 11: Thank You
elif st.session_state.page == 11:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## Thank you!")
        st.write(
            "Thanks for sharing your input — we’ve got everything we need to create your branded app experience.\n\n"
            "You’ll receive your personalized app suggestion shortly.\n"
            "Your KAM will reach out to you with the concept and you’ll be able to review, give feedback and adjust it together if needed."
        )
        st.button("Next →", on_click=next_page)


    with col2:
        st.image(st.session_state.image1, use_container_width=True)


# last Page: Submit
elif st.session_state.page == 12:
    st.header("Feedback")
    st.session_state.q10 = st.slider("How satisfied are you with our customer care?", 1, 5)
    st.session_state.q11 = st.text_area("Any additional feedback?")
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col3:
        st.button("Submit", on_click=last_page)

if st.session_state.end_survey == True:
    st.session_state.ending_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    answers_to_log = [
        str(st.session_state.starting_time),
        str(st.session_state.ending_time),
        str(st.session_state.q1),
        str(st.session_state.q2),
        str(st.session_state.q3),
        str(st.session_state.q4),
        str(st.session_state.q5),
        str(st.session_state.q6),
        str(st.session_state.q7),
        str(st.session_state.q8),
        str(st.session_state.q9),
        str(st.session_state.q10),
        str(st.session_state.q11)
    ]
    save_log(
        st.session_state.get("username", "anonymous"),
        st.session_state.get("email", "unknown@example.com"),
        answers_to_log)
    st.success("🎉 Your answer have been recorded. Thank you for your response!")
    st.button("Reset", on_click=reset)
    st.session_state.end_survey = False