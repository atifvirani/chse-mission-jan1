import streamlit as st
import pandas as pd
import json
import os
from datetime import date

# --- CONFIGURATION ---
st.set_page_config(page_title="CHSE Odisha Tracker", layout="wide")

# --- DATA: CHSE SYLLABUS STRUCTURE ---
# Organized by Subject -> Priority -> Chapter -> Concepts
SYLLABUS = {
    "Physics": {
        "High Priority": {
            "Electrostatics": ["Coulomb's Law", "Gauss’s Law & Applications (Sheet/Wire/Shell)", "Capacitance (Parallel Plate)", "Dipole (Axial/Equatorial)"],
            "Current Electricity": ["Drift Velocity (I=nAqv)", "Kirchhoff’s Laws (Numericals)", "Potentiometer (EMF Comparison)", "Wheatstone Bridge"],
            "Moving Charges & Mag": ["Biot-Savart Law (Circular Loop)", "Ampere’s Circuital Law (Solenoid)", "Moving Coil Galvanometer"],
            "Optics (Ray & Wave)": ["Lens Maker’s Formula", "Prism Formula", "YDSE (Fringe Width Derivation)", "Huygens Principle (Reflection/Refraction)"]
        },
        "Low Priority": {
            "Dual Nature": ["Photoelectric Equation", "de-Broglie Wavelength"],
            "Atoms & Nuclei": ["Bohr’s Model Postulates", "Radioactive Decay Law (N=N0e^-lt)", "Mass Defect"],
            "Semiconductors": ["PN Junction (Forward/Reverse)", "Logic Gates (AND, OR, NAND, NOR)"]
        }
    },
    "Chemistry": {
        "High Priority": {
            "Solutions": ["Raoult’s Law", "Colligative Properties (Elevation BP/Depression FP)", "Van't Hoff Factor"],
            "Electrochemistry": ["Nernst Equation (Numericals)", "Kohlrausch’s Law", "Conductance"],
            "Chemical Kinetics": ["Zero Order Derivation", "First Order Derivation", "Half-life Period"],
            "Organic (Halo-Amines)": ["SN1 vs SN2", "Name Rxns: Reimer-Tiemann", "Name Rxns: Kolbe's", "Name Rxns: Aldol/Cannizzaro", "Lucas Test"]
        },
        "Low Priority": {
            "Coordination Compounds": ["IUPAC Nomenclature", "Valence Bond Theory (Hybridization/Magnetic)"],
            "Surface Chemistry": ["Lyophilic vs Lyophobic", "Hardy-Schulze Rule"],
            "Biomolecules": ["DNA vs RNA", "Structure of Glucose"]
        }
    },
    "Mathematics": {
        "High Priority": {
            "Matrices & Determinants": ["Inverse of Matrix", "Solving Linear Equations (AX=B)", "Properties of Determinants"],
            "Vectors": ["Dot & Cross Product", "Projection of Vector", "Area of Triangle/Parallelogram"],
            "3D Geometry": ["Shortest Distance b/w Skew Lines", "Equation of Plane (3 points)", "Angle between planes"],
            "Linear Programming": ["Maximization/Minimization (Graph Method)"]
        },
        "Low Priority": {
            "Continuity & Diff": ["Continuity Test", "Chain Rule", "Maxima/Minima Word Problems"],
            "Integrals": ["Definite Integral Properties", "Area under curves"],
            "Probability": ["Bayes' Theorem", "Conditional Probability"]
        }
    },
    "IT (Info Tech)": {
        "High Priority": {
            "Database (SQL)": ["SELECT, UPDATE, INSERT", "Aggregate Functions (SUM, AVG)", "Group By/Having"],
            "Networking": ["Topologies (Star, Bus, Ring)", "TCP/IP vs OSI", "Devices (Switch, Router, Hub)"]
        },
        "Low Priority": {
            "Python Programming": ["List & Dictionary Operations", "Functions", "Looping Logic"]
        }
    },
    "English": {
        "High Priority": {
            "Prose": ["My Greatest Olympic Prize", "The Portrait of a Lady"],
            "Poetry": ["Daffodils", "The Ballad of Father Gilligan"],
            "Writing Skills": ["Report Writing (News/Business)", "Note Making"]
        },
        "Low Priority": {
            "Grammar": ["Tense & Aspect", "Passive Voice", "Direct/Indirect Speech"]
        }
    }
}

# --- FILE HANDLING (SAVE/LOAD PROGRESS) ---
PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

# Initialize Session State
if "progress" not in st.session_state:
    st.session_state.progress = load_progress()

def toggle_concept(subject, chapter, concept):
    key = f"{subject}_{chapter}_{concept}"
    current_status = st.session_state.progress.get(key, False)
    st.session_state.progress[key] = not current_status
    save_progress(st.session_state.progress)

# --- DASHBOARD LOGIC ---
def calculate_metrics():
    metrics = {}
    total_high_pcm = 0 # Physics, Chem, Math High Priority
    done_high_pcm = 0
    
    for subject, priorities in SYLLABUS.items():
        total_concepts = 0
        completed_concepts = 0
        
        for priority, chapters in priorities.items():
            for chapter, concepts in chapters.items():
                for concept in concepts:
                    key = f"{subject}_{chapter}_{concept}"
                    total_concepts += 1
                    is_done = st.session_state.progress.get(key, False)
                    if is_done:
                        completed_concepts += 1
                    
                    # Special tracking for Dec-Jan Goal (PCM High Priority)
                    if subject in ["Physics", "Chemistry", "Mathematics"] and priority == "High Priority":
                        total_high_pcm += 1
                        if is_done:
                            done_high_pcm += 1
                            
        percentage = int((completed_concepts / total_concepts) * 100) if total_concepts > 0 else 0
        metrics[subject] = percentage
    
    return metrics, total_high_pcm, done_high_pcm

# --- UI LAYOUT ---

st.title("🎓 CHSE Odisha 12th: Mission Jan 1st")
st.markdown("---")

# 1. TIME TRACKER
today = date.today()
target = date(2026, 1, 1)
days_left = (target - today).days

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Days Remaining", value=f"{days_left} Days", delta="-1 Day", delta_color="inverse")
with col2:
    st.info(f"**Target:** Finish ALL High Priority PCM Chapters by **Jan 1, 2026**.")

# 2. OVERALL PROGRESS DASHBOARD
metrics, total_pcm_high, done_pcm_high = calculate_metrics()

# The "Mission Critical" Progress Bar
pcm_high_percent = int((done_pcm_high / total_pcm_high) * 100) if total_pcm_high > 0 else 0
st.subheader(f"🚀 PCM High Priority Target ({pcm_high_percent}%)")
st.progress(pcm_high_percent / 100)

if pcm_high_percent < 50 and days_left < 20:
    st.error("⚠️ Warning: You are behind schedule on High Priority topics!")
elif pcm_high_percent == 100:
    st.success("🎉 Congratulations! You have completed the Jan 1st Goal!")

st.markdown("### Subject Wise Progress")
d_cols = st.columns(len(metrics))
for idx, (subj, percent) in enumerate(metrics.items()):
    d_cols[idx].metric(label=subj, value=f"{percent}%")

st.markdown("---")

# 3. CHAPTER TRACKING TABS
tabs = st.tabs(list(SYLLABUS.keys()))

for i, subject in enumerate(SYLLABUS.keys()):
    with tabs[i]:
        st.header(f"{subject} Tracker")
        
        priorities = SYLLABUS[subject]
        
        # Split into High and Low columns
        p_col1, p_col2 = st.columns(2)
        
        with p_col1:
            st.subheader("🔴 High Priority (Do First)")
            high_data = priorities.get("High Priority", {})
            for chapter, concepts in high_data.items():
                with st.expander(f"**{chapter}**", expanded=True):
                    for concept in concepts:
                        key = f"{subject}_{chapter}_{concept}"
                        is_checked = st.session_state.progress.get(key, False)
                        st.checkbox(
                            concept, 
                            value=is_checked, 
                            key=key,
                            on_change=toggle_concept,
                            args=(subject, chapter, concept)
                        )

        with p_col2:
            st.subheader("🟢 Low Priority (Do Later)")
            low_data = priorities.get("Low Priority", {})
            for chapter, concepts in low_data.items():
                with st.expander(f"{chapter}", expanded=False):
                    for concept in concepts:
                        key = f"{subject}_{chapter}_{concept}"
                        is_checked = st.session_state.progress.get(key, False)
                        st.checkbox(
                            concept, 
                            value=is_checked, 
                            key=key,
                            on_change=toggle_concept,
                            args=(subject, chapter, concept)
                        )