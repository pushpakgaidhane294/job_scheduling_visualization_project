import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Sequencing with Deadlines", layout="wide")

st.title("💼 Job Sequencing with Deadlines — DAA Mini Project")

st.markdown("""
This interactive mini project demonstrates the **Greedy Algorithm** for the 
*Job Sequencing with Deadlines* problem.  
You can add custom jobs (with deadlines and profits) and visualize how the algorithm schedules them to **maximize total profit**.
""")

# ==========================================================
# RESET FUNCTION — fixed for Streamlit >= 1.36
# ==========================================================
def reset_app():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.jobs_data = []
    st.session_state.run_clicked = False
    st.rerun()  # ✅ works perfectly with latest Streamlit
# ==========================================================


# Initialize session state variables
if "jobs_data" not in st.session_state:
    st.session_state.jobs_data = []
if "run_clicked" not in st.session_state:
    st.session_state.run_clicked = False


# ==========================================================
# STEP 1: Add Job Inputs
# ==========================================================
st.header("🧮 Step 1: Add Job Details")

col1, col2, col3, col4 = st.columns([1, 1, 1, 0.8])

with col1:
    job_id = st.text_input("Job ID", value=f"J{len(st.session_state.jobs_data)+1}")
with col2:
    deadline = st.number_input("Deadline", min_value=1, max_value=10, value=1)
with col3:
    profit = st.number_input("Profit", min_value=1, max_value=100, value=10)
with col4:
    if st.button("➕ Add Job"):
        st.session_state.jobs_data.append({"Job ID": job_id, "Deadline": int(deadline), "Profit": int(profit)})
        st.success(f"Job {job_id} added successfully!")

# Display Job Table
if st.session_state.jobs_data:
    st.subheader("📋 Job List")
    df_jobs = pd.DataFrame(st.session_state.jobs_data)
    st.dataframe(df_jobs, use_container_width=True)

# ==========================================================
# STEP 2: Run Algorithm
# ==========================================================
st.header("🚀 Step 2: Run Algorithm")

if st.button("▶ Run Job Sequencing"):
    st.session_state.run_clicked = True

if st.session_state.run_clicked and st.session_state.jobs_data:
    jobs = st.session_state.jobs_data.copy()

    # Sort by profit descending (same as C code)
    jobs.sort(key=lambda x: x["Profit"], reverse=True)

    max_deadline = max(job["Deadline"] for job in jobs)
    slots = [-1] * (max_deadline + 1)
    total_profit = 0
    jobs_done = 0
    scheduled_jobs = []

    # Greedy scheduling (converted from your C code)
    for job in jobs:
        for j in range(job["Deadline"], 0, -1):
            if slots[j] == -1:
                slots[j] = job["Job ID"]
                total_profit += job["Profit"]
                jobs_done += 1
                scheduled_jobs.append(job)
                break

    # Display Results
    st.subheader("✅ Algorithm Results")
    st.write(f"**Total Jobs Done:** {jobs_done}")
    st.write(f"**Maximum Profit:** ₹{total_profit}")

    st.subheader("📊 Jobs Scheduled")
    scheduled_df = pd.DataFrame(scheduled_jobs)
    st.dataframe(scheduled_df, use_container_width=True)

    # Visualization (Timeline)
    vis_data = []
    for i, job in enumerate(slots[1:], start=1):
        if job != -1:
            vis_data.append({"Slot": f"Time Slot {i}", "Job": job})
    if vis_data:
        vis_df = pd.DataFrame(vis_data)
        fig = px.bar(vis_df, x="Slot", y=["Job"], color="Job", title="Job Scheduling Timeline", barmode="group")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No jobs scheduled.")

# ==========================================================
# STEP 3: Reset Button
# ==========================================================
st.header("🔁 Step 3: Reset App")
if st.button("♻ Reset"):
    reset_app()
