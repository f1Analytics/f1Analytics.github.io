import streamlit as st
from data_engine.main import GPBucket


# Function to create a list of years from 2000 to 2022
def generate_years():
    return list(range(2024, 2000, -1))


# Function to create a list of gpnames from 1 to 20
def generate_gp():
    return list(range(1, 20))


async def create_bucket(year, gp):
    return GPBucket(year=year, gp_id=gp)


def get_bucket(year, gp):
    gpbucket = GPBucket(year=year, gp_id=gp)
    return gpbucket


# Streamlit app layout
def main():
    st.title("Year and GP Selector")

    # Slider for selecting year
    year = st.sidebar.selectbox("Select Year", options=generate_years(), index=0)

    # Slider for selecting year
    gp = st.sidebar.selectbox("Select GP", options=generate_gp(), index=0)

    st.write("Selected Year:", year)
    st.write("Selected GP:", gp)

    bucket = get_bucket(year, gp)

    (
        tab1,
        tab2,
    ) = st.tabs(["Tyre Strategy", "Best Lap Comparison"])

    with tab1:
        st.header("Tyre startegy summary")

        fig = bucket.get_tyre_strategy_summary()
        st.pyplot(fig)

    with tab2:
        st.header("Driver Best Lap Comparison")

        st.markdown("Select two drivers from the panel below to compare their best lap")
        driver1 = st.selectbox("Driver 1", bucket.get_drivers())

        driver2 = st.selectbox("Driver 2", bucket.get_drivers())

        fig = bucket.get_quali_comparison(driver_1=driver1, driver_2=driver2)
        st.pyplot(fig)


if __name__ == "__main__":
    main()
