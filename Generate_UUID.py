import streamlit as st

def generate_uuid():
    ## Generates a random UUID
    
    try:
        import uuid
    except ImportError:
        return "Error: Please install the 'uuid' module."
    try:
        return uuid.uuid4()
    except Exception as e:
        return "Error: " + str(e)

def generate_password(length=12, complexity='strong'):
    ## Generates a random password with specified length and complexity
    try:
        import random
        import string
    except ImportError:
        return "Error: Please install the 'random' module."
    try:
        if complexity == 'strong':
            chars = string.ascii_letters + string.digits + string.punctuation
        elif complexity == 'medium':
            chars = string.ascii_letters + string.digits
        else:
            chars = string.ascii_letters
        return ''.join(random.choice(chars) for _ in range(length))
    except Exception as e:
        return "Error: " + str(e)

def main():
    st.title("Generate a Unique ID or Password")
    
    if st.button("Generate UID"):
        pathinput = generate_uuid()
        Path = f'''{pathinput}'''
        st.code(Path, language="python")
        st.markdown("Enjoy!!")
    
    if st.button("Generate Password"):
        pathinput = generate_password()
        Path = f'''{pathinput}'''
        st.code(Path, language="python")
        st.markdown("Enjoy!!")

if __name__ == "__main__":
    main()
