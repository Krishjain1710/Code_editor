import requests
import streamlit as st
from streamlit_ace import st_ace
import os
import subprocess

# Ollama API Endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Supported languages
languages = {
    "Python": "py",
    "C++": "cpp",
    "Java": "java"
}

# Streamlit App UI
st.title("🚀 AI Code Editor & Compiler (Ollama Codellama)")

# Sidebar - Language Selection
st.sidebar.header("🔹 Select Language")
language = st.sidebar.selectbox("Choose a programming language", list(languages.keys()))

# Ace Editor for Writing Code
st.subheader(f"Write your {language} code below:")
language_mode = {"Python": "python", "C++": "c_cpp", "Java": "java"}

code_input = st_ace(
    language=language_mode[language],
    theme="monokai",
    height=300,
    key="code_editor",
    value=""
)

# AI Code Suggestion using Ollama Codellama
if st.button("💡 Get AI Suggestion"):
    if code_input.strip():
        try:
            # Prepare the payload for Ollama API
            payload = {
                "model": "codellama",  # Use the correct model
                "prompt": f"Improve and complete this code:\n{code_input}",
                "stream": False
            }

            # Make a POST request to Ollama API
            response = requests.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()

            # Debug API Response
            response_json = response.json()
            st.write("🔍 API Response Debug:", response_json)

            # Extract the suggestion
            suggestion = response_json.get("response", response_json.get("error", "⚠️ No valid response received")).strip()
            st.text_area("🧠 AI Suggestion:", suggestion, height=200)
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("⚠️ Enter some code to get AI suggestions.")

# Code Execution (Compile & Run)
if st.button("▶️ Run Code"):
    if code_input.strip():
        file_extension = languages[language]
        file_name = f"temp_code.{file_extension}"
        
        # Save code to file
        with open(file_name, "w") as file:
            file.write(code_input)
        
        # Run the code
        if language == "Python":
            result = subprocess.run(["python", file_name], capture_output=True, text=True)
        
        elif language == "C++":
            compile_result = subprocess.run(["g++", file_name, "-o", "output"], capture_output=True, text=True)
            if compile_result.returncode == 0:
                result = subprocess.run(["./output"], capture_output=True, text=True)
            else:
                st.error(f"❌ Compilation error:\n{compile_result.stderr}")
                os.remove(file_name)
                st.stop()

        elif language == "Java":
            compile_result = subprocess.run(["javac", file_name], capture_output=True, text=True)
            if compile_result.returncode == 0:
                # Extract class name for Java execution
                java_class = file_name.replace(".java", "")
                result = subprocess.run(["java", java_class], capture_output=True, text=True)
            else:
                st.error(f"❌ Compilation error:\n{compile_result.stderr}")
                os.remove(file_name)
                st.stop()
        
        # Show Output
        if result.returncode == 0:
            st.subheader("🖥️ Output:")
            st.code(result.stdout)
        else:
            st.error(f"❌ Error in execution:\n{result.stderr}")

        # Cleanup
        os.remove(file_name)
        if os.path.exists("output"):
            os.remove("output")
    else:
        st.warning("⚠️ Please write some code before running it.")

# Code Download Option
if st.button("⬇️ Download Code"):
    if code_input.strip():
        file_extension = languages[language]
        file_name = f"code.{file_extension}"
        
        # Write the code to the file
        with open(file_name, "w") as file:
            file.write(code_input)

        # Provide a download link
        with open(file_name, "rb") as file:
            st.download_button(f"Download {file_name}", file, file_name)

        os.remove(file_name)
    else:
        st.warning("⚠️ Please write some code before downloading it.")
