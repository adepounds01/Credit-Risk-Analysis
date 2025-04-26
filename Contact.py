def app(st, current_dir, Image):
    # ----------------------- Directory Setup -----------------------
    resume_file = current_dir / "Resume" / "MyResume.pdf"
    profile_pic = current_dir / "Photos" / "profile-pic.jpg"
    social_icons = {
        "LinkedIn": current_dir / "Photos" / "linkedin.png",
        "GitHub": current_dir / "Photos" / "github.png",
        "Email": current_dir / "Photos" / "gmail.png"
    }

    # ----------------------- Page Configuration --------------------
    st.header("Charles Adeola", divider="rainbow")
    st.write("## Financial Technology & Data Analytics Specialist")
    
    # ----------------------- Profile Section -----------------------
    with st.container():
        col1, col2 = st.columns([1, 2], gap="medium")
        
        with col1:
            profile_img = Image.open(profile_pic)
            st.image(profile_img, use_container_width=True)  # Fixed deprecation
            
            # Resume Download
            with open(resume_file, "rb") as pdf_file:
                PDFbyte = pdf_file.read()
            
            st.download_button(
                label="📑 Download Full Resume",
                data=PDFbyte,
                file_name='Charles_Adeola_Resume.pdf',
                mime="application/octet-stream",
                use_container_width=True,
                help="Access my complete professional history and qualifications"
            )

        with col2:
            st.subheader("Professional Profile")
            st.markdown("""
                🎓 **MSc Financial Technology Candidate** | Teesside University  
                📈 **Specialization**: FinTech Solutions & Financial Data Analysis  
                💼 **Experience**: 2+ years in financial data modeling and analysis  
                
                As a passionate FinTech graduate student, I combine financial expertise with technical skills 
                to develop innovative financial solutions. My current research focuses on:
                - Algorithmic trading strategies
                - Blockchain applications in finance
                - Risk modeling using machine learning
                - Payment system innovations

                **Core Competencies**:  
                ✔️ Financial Data Analysis & Visualization  
                ✔️ Predictive Modeling for Market Trends  
                ✔️ Python for Quantitative Finance  
                ✔️ Regulatory Technology (RegTech)  
                ✔️ Financial API Integration
                """)

    st.divider()

    # ----------------------- Contact Section -----------------------
    st.subheader("Professional Network", anchor="contact")
    
    cols = st.columns(len(social_icons))
    for idx, (platform, icon_path) in enumerate(social_icons.items()):
        with cols[idx]:
            with st.container(border=True):
                st.image(Image.open(icon_path), width=45)
                st.write(f"**{platform}**")
                link_info = {
                    "LinkedIn": ("View Profile", "https://www.linkedin.com/in/charles-adeola-416789128/"),
                    "GitHub": ("Explore Code", "https://github.com/adepounds01"),
                    "Email": ("Contact Me", "mailto:adeola.charles01@gmail.com")
                }
                text, url = link_info[platform]
                st.link_button(text, url, use_container_width=True)

    # ----------------------- Custom CSS ----------------------------
    st.markdown("""
    <style>
        [data-testid="stDownloadButton"] button {
            background: linear-gradient(45deg, #1E90FF, #4169E1);
            color: white !important;
            transition: all 0.3s ease;
        }
        [data-testid="stDownloadButton"] button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(30, 144, 255, 0.4);
        }
        [data-testid="stVerticalBlock"] {
            padding: 1rem;
            border-radius: 10px;
            background: rgba(245, 245, 245, 0.1);
        }
        .st-emotion-cache-1v0mbdj img {
            border: 2px solid #F0F2F6;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)