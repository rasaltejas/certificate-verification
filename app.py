import streamlit as st
import hashlib
import uuid
from datetime import datetime
from blockchain import certificate_chain

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="Blockchain Certificate Verification",
    page_icon="🔗",
    layout="wide"
)

# ---------------- Custom CSS ----------------
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            color: #1a237e;
            font-size: 2.2rem;
            font-weight: bold;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            text-align: center;
            color: #555;
            margin-bottom: 1.5rem;
        }
        .block-card {
            background: #ffffff;
            border-left: 6px solid #1a237e;
            border-radius: 8px;
            padding: 15px 20px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .hash-text {
            font-family: monospace;
            font-size: 0.78rem;
            color: #444;
            word-break: break-all;
            background: #f5f5f5;
            padding: 4px 8px;
            border-radius: 4px;
        }
        .valid-box {
            background: #c8e6c9;
            border-left: 6px solid #1b5e20;
            padding: 18px;
            border-radius: 8px;
        }
        .invalid-box {
            background: #ffcdd2;
            border-left: 6px solid #b71c1c;
            padding: 18px;
            border-radius: 8px;
        }
        .warn-box {
            background: #fff3cd;
            border-left: 6px solid #856404;
            padding: 18px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)


# ---------------- Helper Functions ----------------
def generate_cert_hash(data):
    raw = f"{data['student_name']}{data['course']}{data['institution']}{data['certificate_id']}"
    return hashlib.sha256(raw.encode()).hexdigest()


def init_session_state():
    if "issued_cert_id" not in st.session_state:
        st.session_state.issued_cert_id = None
    if "verify_result" not in st.session_state:
        st.session_state.verify_result = None


# ---------------- Header ----------------
st.markdown('<div class="main-title">🔗 Academic Certificate Verification using Blockchain</div>',
            unsafe_allow_html=True)
st.markdown('<div class="subtitle">Secure • Immutable • Tamper-Proof Certificate Storage</div>',
            unsafe_allow_html=True)

init_session_state()

# ---------------- Sidebar Navigation ----------------
st.sidebar.title("⚙️ Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home / Ledger", "📜 Issue Certificate", "✅ Verify Certificate", "🧪 Tamper Demo"])
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Chain Length:** {len(certificate_chain.chain)} blocks")
st.sidebar.markdown(f"**Difficulty:** {certificate_chain.difficulty} leading zeros")
if certificate_chain.is_chain_valid():
    st.sidebar.success("Blockchain: ✅ VALID")
else:
    st.sidebar.error("Blockchain: ❌ INVALID")


# ============================================================
# PAGE 1: HOME / LEDGER
# ============================================================
if page == "🏠 Home / Ledger":
    st.header("⛓️ Blockchain Ledger")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Blocks", len(certificate_chain.chain))
    col2.metric("Difficulty", certificate_chain.difficulty)
    col3.metric("Chain Status",
                "✅ VALID" if certificate_chain.is_chain_valid() else "❌ INVALID")

    st.markdown("---")

    for block in certificate_chain.chain:
        data = block.certificate_data
        with st.container():
            st.markdown(f"""
            <div class="block-card">
                <h4 style="color:#1a237e; margin-top:0;">📦 Block #{block.index}</h4>
                <p><b>Timestamp:</b> {datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')}</p>
                {f'''
                    <p><b>Student:</b> {data.get('student_name','')}</p>
                    <p><b>Course:</b> {data.get('course','')}</p>
                    <p><b>Institution:</b> {data.get('institution','')}</p>
                    <p><b>Certificate ID:</b> {data.get('certificate_id','')}</p>
                ''' if data.get('student_name') else f'<p><i>{data.get("info","")}</i></p>'}
                <p><b>Previous Hash:</b></p>
                <div class="hash-text">{block.previous_hash}</div>
                <p style="margin-top:8px;"><b>Current Hash:</b></p>
                <div class="hash-text">{block.hash}</div>
                <p style="margin-top:8px;"><b>Nonce:</b> {block.nonce}</p>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# PAGE 2: ISSUE CERTIFICATE
# ============================================================
elif page == "📜 Issue Certificate":
    st.header("📜 Issue New Certificate")
    st.write("Fill in the details below. A block will be mined and added to the blockchain.")

    with st.form("issue_form", clear_on_submit=True):
        student_name = st.text_input("Student Name", placeholder="e.g., Alice Sharma")
        course = st.text_input("Course", placeholder="e.g., B.Tech Computer Science")
        institution = st.text_input("Institution", placeholder="e.g., ABC University")

        submitted = st.form_submit_button("⛓️ Issue Certificate on Blockchain")

    if submitted:
        if not (student_name and course and institution):
            st.error("⚠️ Please fill all fields.")
        else:
            cert_id = "CERT-" + str(uuid.uuid4())[:8].upper()
            data = {
                "certificate_id": cert_id,
                "student_name": student_name,
                "course": course,
                "institution": institution,
                "issue_date": datetime.now().strftime("%Y-%m-%d"),
            }
            data["cert_hash"] = generate_cert_hash(data)

            with st.spinner("⛏️ Mining block (Proof-of-Work)..."):
                block = certificate_chain.add_block(data)

            st.session_state.issued_cert_id = cert_id

            st.success(f"✅ Certificate issued successfully!")
            st.info(f"📌 **Certificate ID (save this for verification):** `{cert_id}`")

            st.markdown("### 🔍 New Block Details")
            st.json(block.to_dict())


# ============================================================
# PAGE 3: VERIFY CERTIFICATE
# ============================================================
elif page == "✅ Verify Certificate":
    st.header("✅ Verify Certificate")
    st.write("Enter the Certificate ID to verify authenticity against the blockchain.")

    with st.form("verify_form"):
        cert_id = st.text_input("Certificate ID", placeholder="e.g., CERT-A1B2C3D4")
        verify_btn = st.form_submit_button("🔍 Verify on Blockchain")

    if verify_btn:
        if not cert_id.strip():
            st.error("⚠️ Please enter a Certificate ID.")
        else:
            block = certificate_chain.find_certificate(cert_id.strip())

            if block:
                expected_hash = generate_cert_hash(block.certificate_data)
                is_authentic = (expected_hash == block.certificate_data["cert_hash"])

                if is_authentic and certificate_chain.is_chain_valid():
                    st.markdown(f"""
                    <div class="valid-box">
                        <h3 style="margin-top:0;">✅ Certificate is AUTHENTIC</h3>
                        <p><b>Student:</b> {block.certificate_data['student_name']}</p>
                        <p><b>Course:</b> {block.certificate_data['course']}</p>
                        <p><b>Institution:</b> {block.certificate_data['institution']}</p>
                        <p><b>Issue Date:</b> {block.certificate_data['issue_date']}</p>
                        <p><b>Certificate ID:</b> {block.certificate_data['certificate_id']}</p>
                        <p><b>Stored in Block #:</b> {block.index}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("**Block Hash:**")
                    st.code(block.hash, language="text")

                else:
                    st.markdown(f"""
                    <div class="invalid-box">
                        <h3 style="margin-top:0;">❌ Certificate TAMPERED!</h3>
                        <p>Data integrity check failed. This certificate has been modified.</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warn-box">
                    <h3 style="margin-top:0;">⚠️ Certificate NOT FOUND</h3>
                    <p>No certificate with ID <code>{cert_id}</code> exists on the blockchain.</p>
                </div>
                """, unsafe_allow_html=True)


# ============================================================
# PAGE 4: TAMPER DEMO
# ============================================================
elif page == "🧪 Tamper Demo":
    st.header("🧪 Tamper Demonstration")
    st.write("Show how altering a block's data invalidates the entire chain.")

    if len(certificate_chain.chain) <= 1:
        st.warning("⚠️ Issue at least one certificate first from the 'Issue Certificate' page.")
    else:
        options = [f"Block #{b.index} - {b.certificate_data.get('student_name', b.certificate_data.get('info',''))}"
                   for b in certificate_chain.chain[1:]]

        selected = st.selectbox("Select a block to tamper", options)
        block_index = int(selected.split()[1].replace("#", ""))

        new_name = st.text_input("New (fake) student name", value="HACKED STUDENT")

        if st.button("💥 Tamper Block"):
            certificate_chain.tamper_block(block_index, new_name)
            st.error(f"🚨 Block #{block_index} has been tampered!")

        st.markdown("---")

        if st.button("🔄 Reset Blockchain (Restart App)"):
            st.warning("Restart the Streamlit app to reset the blockchain.")

        st.markdown("### Current Chain Validity:")
        if certificate_chain.is_chain_valid():
            st.success("✅ Chain is VALID")
        else:
            st.error("❌ Chain is INVALID — tampering detected!")
            st.info("Go to 'Home / Ledger' page to view the broken chain.")