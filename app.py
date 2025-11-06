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
**Job Sequencing with Deadlines** problem, implemented in **Python**.  

🧩 **Goal:** Schedule jobs to maximize profit such that each job finishes before its deadline.
""")

# ===================================
# SESSION STATE INITIALIZATION
# ===================================
if "jobs_data" not in st.session_state:
    st.session_state.jobs_data = []
if "run_clicked" not in st.session_state:
    st.session_state.run_clicked = False

# ===================================
# RESET FUNCTION (Fixed for latest Streamlit)
# ===================================
def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.jobs_data = []
    st.session_state.run_clicked = False
    st.rerun()  # ✅ fixed: no experimental_rerun()

# ===================================
# STEP 1: INPUT JOB DATA
# ===================================
st.header("🔹 Step 1: Enter Job Details")

num_jobs = st.number_input("Enter number of jobs:", min_value=1, max_value=15, value=5)
jobs_data = []

st.info("Enter Job ID, Deadline, and Profit for each job below:")

for i in range(num_jobs):
    col1, col2, col3 = st.columns(3)
    with col1:
        job_id = st.text_input(f"Job {i+1} ID:", value=f"J{i+1}", key=f"id_{i}")
    with col2:
        deadline = st.number_input(f"Deadline for {job_id}:", min_value=1, max_value=10, value=min(i+2, 10), key=f"dl_{i}")
    with col3:
        profit = st.number_input(f"Profit for {job_id}:", min_value=1, max_value=500, value=(i+1)*10, key=f"pf_{i}")
    jobs_data.append({"Job ID": job_id, "Deadline": int(deadline), "Profit": int(profit)})

df_jobs = pd.DataFrame(jobs_data)
st.write("### 📋 Job Table")
st.dataframe(df_jobs, use_container_width=True)

# ===================================
# STEP 2: Run / Reset Buttons
# ===================================
st.header("🚀 Step 2: Run / Reset Algorithm")

col_run, col_reset = st.columns(2)
with col_run:
    if st.button("▶️ Run Algorithm"):
        st.session_state.jobs_data = jobs_data
        st.session_state.run_clicked = True
with col_reset:
    if st.button("🔄 Reset"):
        reset_app()

# ===================================
# STEP 3: Algorithm (Converted from C)
# ===================================
if st.session_state.run_clicked and st.session_state.jobs_data:
    st.success("✅ Algorithm executed successfully!")

    # Sort jobs by profit (descending)
    jobs = sorted(st.session_state.jobs_data, key=lambda x: x["Profit"], reverse=True)

    # Find maximum deadline
    max_deadline = max(job["Deadline"] for job in jobs)
    slots = [-1] * (max_deadline + 1)  # index 0 unused

    total_profit = 0
    jobs_done = 0

    # Schedule jobs similar to your C code logic
    for job in jobs:
        for j in range(job["Deadline"], 0, -1):
            if slots[j] == -1:
                slots[j] = job["Job ID"]
                total_profit += job["Profit"]
                jobs_done += 1
                break

    # Prepare scheduled job list (in order of slots)
    scheduled_jobs = []
    for j in range(1, max_deadline + 1):
        if slots[j] != -1:
            job = next(job for job in jobs if job["Job ID"] == slots[j])
            scheduled_jobs.append(job)

    # ===================================
    # STEP 4: Display Results
    # ===================================
    st.subheader("📊 Scheduled Jobs (In Execution Order)")
    scheduled_df = pd.DataFrame(scheduled_jobs)
    st.dataframe(scheduled_df, use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("✅ Total Jobs Done", jobs_done)
    col2.metric("💰 Total Profit", f"₹{total_profit}")

    # ===================================
    # STEP 5: Timeline Visualization
    # ===================================
    st.header("📈 Step 3: Job Scheduling Timeline")

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

    # ===================================
    # STEP 6: Visual Job Path (Boxes)
    # ===================================
    st.header("🧱 Step 4: Job Sequence Path (Visual Blocks)")

    job_path = " ➜ ".join([job["Job ID"] for job in scheduled_jobs])
    st.markdown(f"<h4 style='text-align:center;color:#2E86C1;'> {job_path} </h4>", unsafe_allow_html=True)

    st.markdown("### 📦 Visual Representation:")
    cols = st.columns(len(scheduled_jobs))
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
📘 **About:**  
This algorithm uses a **Greedy strategy** to schedule jobs in decreasing profit order,  
placing each job in the latest available slot before its deadline —  
exactly like the classic C algorithm implementation.
""")
