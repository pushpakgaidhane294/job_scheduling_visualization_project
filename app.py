import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# =============================
# Streamlit Page Configuration
# =============================
st.set_page_config(page_title="Job Sequencing Visualization", layout="wide")
st.title("💼 Job Sequencing with Deadlines — DAA Mini Project")

st.markdown("""
This project demonstrates the **Greedy Algorithm** for solving the  
**Job Sequencing with Deadlines** problem.

🧩 **Goal:** Schedule jobs to maximize profit while ensuring each job finishes before its deadline.
""")

# ===================================
# SESSION STATE INITIALIZATION
# ===================================
if "jobs_data" not in st.session_state:
    st.session_state.jobs_data = []
if "run_clicked" not in st.session_state:
    st.session_state.run_clicked = False

# ===================================
# RESET FUNCTION
# ===================================
def reset_app():
    st.session_state.jobs_data = []
    st.session_state.run_clicked = False
    st.experimental_rerun()

# ===================================
# STEP 1: INPUT OPTIONS
# ===================================
st.header("🔹 Step 1: Input Jobs")

input_mode = st.radio(
    "Select Input Mode:",
    ("Manual Entry", "CSV Upload", "Custom Text Input"),
    horizontal=True
)

jobs_data = []

# ========== MODE 1: MANUAL ENTRY ==========
if input_mode == "Manual Entry":
    num_jobs = st.number_input("Enter number of jobs:", min_value=1, max_value=100, value=5)
    st.info("Enter Job ID, Deadline, and Profit for each job below:")

    for i in range(num_jobs):
        col1, col2, col3 = st.columns(3)
        with col1:
            job_id = st.text_input(f"Job {i+1} ID:", value=f"J{i+1}", key=f"id_{i}")
        with col2:
            deadline = st.number_input(f"Deadline for {job_id}:", min_value=1, max_value=100, value=min(i+2, 100), key=f"dl_{i}")
        with col3:
            profit = st.number_input(f"Profit for {job_id}:", min_value=1, max_value=10000, value=(i+1)*10, key=f"pf_{i}")
        jobs_data.append({"Job ID": job_id, "Deadline": int(deadline), "Profit": int(profit)})

# ========== MODE 2: CSV UPLOAD ==========
elif input_mode == "CSV Upload":
    st.info("Upload a CSV file with columns: Job ID, Deadline, Profit")
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df, use_container_width=True)
            jobs_data = df.to_dict(orient="records")
        except:
            st.error("⚠️ Error reading CSV. Ensure it has columns: Job ID, Deadline, Profit")

# ========== MODE 3: CUSTOM TEXT INPUT ==========
elif input_mode == "Custom Text Input":
    st.info("Enter jobs in this format:  JobID,Deadline,Profit (one per line)")
    text_input = st.text_area(
        "Example:\nJ1,2,60\nJ2,1,100\nJ3,3,20\nJ4,2,40\nJ5,1,20",
        height=150,
    )
    if text_input.strip():
        try:
            for line in text_input.strip().split("\n"):
                parts = line.strip().split(",")
                if len(parts) == 3:
                    jobs_data.append({
                        "Job ID": parts[0].strip(),
                        "Deadline": int(parts[1].strip()),
                        "Profit": int(parts[2].strip())
                    })
            st.success(f"{len(jobs_data)} jobs added successfully.")
        except:
            st.error("⚠️ Invalid format. Please follow: JobID,Deadline,Profit")

# Display Input Table
if jobs_data:
    df_jobs = pd.DataFrame(jobs_data)
    st.write("### 📋 Job Table")
    st.dataframe(df_jobs, use_container_width=True)

# ===================================
# STEP 2: Buttons
# ===================================
st.header("🚀 Step 2: Run / Reset Algorithm")

col_run, col_reset = st.columns(2)
with col_run:
    if st.button("▶️ Run Algorithm"):
        st.session_state.jobs_data = jobs_data
        st.session_state.run_clicked = True
with col_reset:
    st.button("🔄 Reset", on_click=reset_app)

# ===================================
# STEP 3: Algorithm Execution
# ===================================
if st.session_state.run_clicked and st.session_state.jobs_data:
    st.success("Algorithm executed successfully!")

    sorted_jobs = sorted(st.session_state.jobs_data, key=lambda x: x["Profit"], reverse=True)
    max_deadline = max(job["Deadline"] for job in sorted_jobs)
    slots = [-1] * (max_deadline + 1)
    total_profit = 0
    job_sequence = []

    for job in sorted_jobs:
        for j in range(job["Deadline"], 0, -1):
            if slots[j] == -1:
                slots[j] = job["Job ID"]
                total_profit += job["Profit"]
                job_sequence.append(job)
                break

    scheduled_jobs = [job for job in job_sequence if job is not None]
    total_jobs_done = len(scheduled_jobs)

    # Display Results
    st.subheader("📊 Scheduled Jobs (Optimal Order)")
    st.dataframe(pd.DataFrame(scheduled_jobs), use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("✅ Total Jobs Done", total_jobs_done)
    col2.metric("💰 Total Profit", f"₹{total_profit}")

    # Visualization: Timeline
    st.header("📈 Step 3: Job Scheduling Timeline")
    st.markdown("Each bar represents a time slot and the job scheduled in it.")

    fig = go.Figure()
    for i, job in enumerate(scheduled_jobs):
        fig.add_trace(go.Bar(
            x=[1],
            y=[f"Slot {i+1}"],
            orientation='h',
            name=job["Job ID"],
            text=f"{job['Job ID']} (P={job['Profit']})",
            textposition='inside'
        ))

    fig.update_layout(
        barmode='stack',
        title="🕒 Job Scheduling Timeline",
        xaxis_title="Time Slot",
        yaxis_title="Scheduled Jobs",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

    # Visualization: Job Path (Boxes)
    st.header("🧱 Step 4: Job Sequence Path (Visual Blocks)")

    job_path = " ➜ ".join([job["Job ID"] for job in scheduled_jobs])
    st.markdown(f"<h4 style='text-align:center;color:#2E86C1;'> {job_path} </h4>", unsafe_allow_html=True)

    st.markdown("### 📦 Visual Representation:")
    cols = st.columns(total_jobs_done)
    for i, job in enumerate(scheduled_jobs):
        with cols[i]:
            st.markdown(
                f"""
                <div style='background-color:#AED6F1;padding:20px;border-radius:10px;
                text-align:center;border:2px solid #2980B9;'>
                <b>{job['Job ID']}</b><br>
                Deadline: {job['Deadline']}<br>
                Profit: ₹{job['Profit']}
                </div>
                """,
                unsafe_allow_html=True
            )

# ===================================
# FOOTER
# ===================================
st.markdown("""
---
📘 **Project Summary:**  
This project applies a **Greedy Algorithm** to maximize total profit in job scheduling under deadline constraints.  
Perfect for **DAA (Design and Analysis of Algorithms)** mini-project submission.
""")
