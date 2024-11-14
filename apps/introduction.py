import streamlit as st

def app():
    # Title and Vision
    st.title("Introduction")
    st.subheader("Our Vision")
    st.write(
        """
        Our vision is to transform raw sales data into meaningful insights that help the coffee shop make smarter, 
        data-driven decisions. We believe that data can not only improve operations but also enhance customer satisfaction, 
        loyalty, and profitability. Through this project, we aim to support informed decision-making by uncovering 
        actionable insights from data.
        """
    )

    # Team Introduction Section
    st.subheader("Meet Team Akatsuki")
    st.write("Get to know the talented members who contributed to this project:")

    # Team Members
    team_members = [
        {
            "name": "Afif Hossain Irfan",
            "role": "Team Leader, Data Researcher, and Analyst",
            "contribution": "Led the team in data research and analysis, ensuring we uncover valuable insights. "
                            "Afif guided the data interpretation, maintaining alignment with our vision. "
                            "He also coordinated tasks and contributed to the strategic decision-making throughout the project.",
            "skills": "Data Analysis, Research, Strategic Planning",
            "image": "images/Afif Hossain Irfan.jpg"
        },
        {
            "name": "Shovan Bhattacharjee",
            "role": "Data Analyst and Programmer",
            "contribution": "Handled data cleaning, processing, and dashboard functionality. "
                            "Shovan tackled technical challenges, transforming raw data into an analysis-ready format. "
                            "His expertise in data wrangling and programming ensured the data's accuracy and reliability.",
            "skills": "Data Processing, Python Programming, Data Visualization",
            "image": "images/shovan.jpg"
        },
        {
            "name": "Md Jahidul Islam Supta",
            "role": "Programmer and Dashboard Designer",
            "contribution": "Designed the interactive dashboard, making data insights visually engaging and accessible. "
                            "Jahidul focused on the user experience, ensuring that each visualization tells a clear story "
                            "and enhances usability.",
            "skills": "Streamlit, User Interface Design, Data Visualization",
            "image": "images/Md. Jahidul Islam Supta.jpg"
        }
    ]

    # Display each team member's details with clear layout
    for member in team_members:
        # Create two columns for each member: one for the image, one for the details
        col1, col2 = st.columns([1, 3])  # Adjust column widths for image and text layout

        with col1:
            # Display member's image with circular appearance by setting width and height
            st.image(member["image"], width=140, use_container_width=True, caption=member["name"])

        with col2:
            # Display name, role, and detailed information
            st.markdown(f"### {member['name']}")
            st.write(f"**Role**: {member['role']}")
            st.write(f"**Contribution**: {member['contribution']}")
            st.write(f"**Key Skills**: {member['skills']}")

        # Adding a horizontal line between each member for better separation
        st.markdown("---")

    # Closing Statement
    st.subheader("Our Team's Commitment")
    st.write(
        """
        Together, we combined our skills to create a tool that uncovers hidden data patterns, empowering the 
        coffee shop to make better, data-driven decisions. We believe this project is just the beginning, and we’re excited 
        to see the impact it can have. Now, let’s dive into the analysis!
        """
    )
