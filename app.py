import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="Job Sequencing", layout="wide")
st.title("💼 Job Sequencing with Deadlines — Greedy Algorithm")

st.markdown("""
This app solves the **Job Sequencing with Deadlines** problem using a **Greedy Algorithm**.

🧩 **Goal:** Schedule jobs to maximize profit, ensuring each job finishes before its deadline.
""")

# Session state
if "jobs_data" not in st.session_state:
    st.session_state.jobs_data = []
if "run_clicked" not in st.session_state:
    st.session_state.run_clicked = False

# Reset function
def reset_app():
    st.session_state.jobs_data = []
    st.session_state.run_clicked = False
    st.experimental_rerun()

# Input section
st.header("🔹 Step 1: Input Jobs")
input_mode = st.radio("Select Input Mode:", ("Manual Entry", "CSV Upload", "Text Input"), horizontal=True)
jobs_data = []

if input_mode == "Manual Entry":
    num_jobs = st.number_input("Number of jobs:", min_value=1, max_value=100, value=5)
    st.info("Enter Job ID, Deadline, and Profit:")
    for i in range(num_jobs):
        col1, col2, col3 = st.columns(3)
        with col1:
            job_id = st.text_input(f"Job {i+1} ID", value=f"J{i+1}", key=f"id_{i}")
        with col2:
            deadline = st.number_input(f"Deadline for {job_id}", min_value=1, max_value=100, value=min(i+2, 100), key=f"dl_{i}")
        with col3:
            profit = st.number_input(f"Profit for {job_id}", min_value=1, max_value=10000, value=(i+1)*10, key=f"pf_{i}")
        jobs_data.append({"Job ID": job_id, "Deadline": int(deadline), "Profit": int(profit)})

elif input_mode == "CSV Upload":
    st.info("Upload CSV with columns: Job ID, Deadline, Profit")
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df, use_container_width=True)
            jobs_data = df.to_dict(orient="records")
        except:
            st.error("⚠️ Invalid CSV format.")

elif input_mode == "Text Input":
    st.info("Enter jobs as: JobID,Deadline,Profit (one per line)")
    text_input = st.text_area("Example:\nJ1,2,60\nJ2,1,100\nJ3,3,20", height=150)
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
            st.success(f"{len(jobs_data)} jobs added.")
        except:
            st.error("⚠️ Invalid format.")

# Display input
if jobs_data:
    df_jobs = pd.DataFrame(jobs_data)
    st.write("### 📋 Job Table")
    st.dataframe(df_jobs, use_container_width=True)

# Buttons
st.header("🚀 Step 2: Run / Reset")
col_run, col_reset = st.columns(2)
with col_run:
    if st.button("▶️ Run Algorithm"):
        st.session_state.jobs_data = jobs_data
        st.session_state.run_clicked = True
with col_reset:
    st.button("🔄 Reset", on_click=reset_app)

# Algorithm execution
if st.session_state.run_clicked and st.session_state.jobs_data:
    st.success("✅ Algorithm executed!")

    jobs = sorted(st.session_state.jobs_data, key=lambda x: x["Profit"], reverse=True)
    max_deadline = max(job["Deadline"] for job in jobs)
    slots = [None] * (max_deadline + 1)
    total_profit = 0
    scheduled_jobs = []

    for job in jobs:
        for j in range(job["Deadline"], 0, -1):
            if slots[j] is None:
                slots[j] = job
                total_profit += job["Profit"]
                scheduled_jobs.append(job)
                break

    st.subheader("📊 Scheduled Jobs")
    st.dataframe(pd.DataFrame(scheduled_jobs), use_container_width=True)

    col1, col2 = st.columns(2)
    col1.metric("✅ Jobs Scheduled", len(scheduled_jobs))
    col2.metric("💰 Total Profit", f"₹{total_profit}")

    # Timeline plot
    st.header("📈 Job Scheduling Timeline")
    st.markdown("Each bar shows a time slot and the job assigned to it.")

    fig = go.Figure()
    for i, job in enumerate(scheduled_jobs):
        fig.add_trace(go.Bar(
            x=[1],
            y=[f"Slot {i+1}"],
            orientation='h',
            name=job["Job ID"],
            text=f"{job['Job ID']} (₹{job['Profit']})",
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

    # Visual blocks
    st.header("🧱 Job Sequence Blocks")
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

# Footer
st.markdown("""
---
📘 **Summary:**  
This app uses a greedy strategy to schedule jobs for maximum profit under deadline constraints.  
Perfect for DAA mini-projects and algorithm visualization.
""")
