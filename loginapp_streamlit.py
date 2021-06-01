import sqlite3 as sql3
import streamlit as st
import streamlit.components.v1 as stc

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Select Menu from Sidebar for Navigation</h1>
    </div>
    """
stc.html(HTML_BANNER)


# DB Management
conn = sql3.connect("usersdata.db")
c = conn.cursor()


def create_usertable():
    sql = '''CREATE TABLE IF NOT EXISTS userstable (username VARCHAR(30) unique ,password VARCHAR(30),mobile_number INTEGER PRIMARY KEY,gender VARCHAR(6))'''
    c.execute(sql)


def add_userdata(username, password, mobile_number, gender):
    # def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?,?,?)',
              (username, password, mobile_number, gender))


def login_user(username, password):
    st.sidebar.write("Checking...")
    c.execute('SELECT * FROM userstable WHERE username = ? and password = ?',
              (username, password))
    data = c.fetchall()
    return data


def view_all_user():
    c.execute("Select * from userstable")
    data = c.fetchall()
    return data


def user_details(username):
    c.execute("Select * from userstable where username=?", (username))
    data = c.fetchall()
    return data


def main():
    """Simple Login Page"""

    menu = ["Home", "Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.header("Home Page")
        st.text(f"You are currently in {choice} Page")

    elif choice == "Login":
        st.sidebar.header("Enter your Login Details")
        st.text(f"You are currently in {choice} Page")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type="password")
        login_button = st.sidebar.checkbox("Stay Logged In")
        if login_button:
            create_usertable()
            # if password == "1234":
            result = login_user(username, password)
            if result:
                st.sidebar.success(
                    f"Login Successful, Logged in as {username}")
                task = st.selectbox(
                    "Task", ["To-Do", "Analytics", "Profile"])
                if task == "To-Do":
                    st.subheader("Add Your Task")
                elif task == "Analytics":
                    st.subheader("Analytics")
                elif task == ("Profile"):
                    st.subheader("Profile")
            else:
                st.sidebar.warning("Invaild Password/User name")

    elif choice == "Signup":
        st.header("Creat a New Account")
        st.text(f"You are currently in {choice} Page")
        new_user = st.text_input("Username", "")
        new_password = st.text_input("Password", type="password")
        new_user_mobile = st.text_input("Mobile Number", max_chars=10)
        new_user_gender = st.text_input("Gender: Male , Female or Others")

        if st.button("Sign Up"):
            create_usertable()
            add_userdata(new_user, new_password,
                         new_user_mobile, new_user_gender)
            st.success("Account Created Successfully")
            st.info("Goto menu and Select Login")


if __name__ == "__main__":
    main()
