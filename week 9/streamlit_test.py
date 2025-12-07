import streamlit as st
import pandas as pd
import numpy as np



st.title("hi , I am amsha!")
st.header("i hate people")
st.markdown("*i* am **sick**")

st.markdown("<h1 style='color:#FF69B4;'>Hello World</h1>", unsafe_allow_html=True)


if st.button("Click if you also hate people"):
    st.write("Passed the vibe check!")

agree = st.checkbox("I am also sick")

st.markdown("""
    <style>
    .stApp {
        background-color: #1E90FF;
    }
    </style>
""", unsafe_allow_html=True)

val = st.slider(
"How much do you like me",
0, 100, 50
 )


df=pd.DataFrame({
    "name":["Zahny","Hudha","Amsha"],
     "age":[18,18,20]

})

st.dataframe(df)


st.divider()

st.image(
  "https://miro.medium.com/0*A7MUqyCLvZDcHkfM.jpg",
   caption="testing",
   
)

data=pd.DataFrame(
  np.random.randn(20,3),
  columns=["A",'B',"C"]
)
st.write(data)
st.bar_chart(data)
st.line_chart(data)


scatter_data = pd.DataFrame(
np.random.randn(100, 3),
columns=["x", "y", "size"]
)
st.subheader("Scatter chart")
st.scatter_chart(scatter_data, x="x", y="y", size="size")



with st.expander('see details'):  #useful for showing data
    st.write ("more details")
    st.dataframe(data)



    