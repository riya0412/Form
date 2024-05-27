import streamlit as st
import pandas as pd
import mysql.connector

def SizeCalculatorinches():
    # Title of the app
    st.title("Conductor Cost Calculator")

    # Input fields
    st.header("Input Parameters")

    cost_of_conductor = st.number_input("Cost of Conductor (in ₹)", value=1000)
    diam_aluminium_inches = st.number_input("Diameter of Aluminium (inches)", value=0.750)
    diam_steel_inches = st.number_input("Diameter of Steel (inches)", value=0.420)
    

    # Calculations
    def inch_to_mm(inches):
        return inches * 25.4

    def calculate_csa(diameter_mm):
        radius_mm = diameter_mm / 2
        return 3.14159 * (radius_mm ** 2)
    def al_calculate_scsa(diameter_mm):
        return 12.93*(diameter_mm**2)
    def steel_calculate_scsa(diameter_mm):
        return 6.156*(diameter_mm**2)

    diam_aluminium_mm = inch_to_mm(diam_aluminium_inches)
    diam_steel_mm = inch_to_mm(diam_steel_inches)
    radius_aluminium_mm = diam_aluminium_mm / 2
    radius_steel_mm = diam_steel_mm / 2

    csa_aluminium = calculate_csa(diam_aluminium_mm)
    csa_steel = calculate_csa(diam_steel_mm)

    suggested_csa_aluminium = al_calculate_scsa(diam_aluminium_mm)
    suggested_csa_steel = steel_calculate_scsa(diam_steel_mm)
    total_suggested_csa = suggested_csa_aluminium + suggested_csa_steel

    percentage_aluminium = (suggested_csa_aluminium / total_suggested_csa) * 100
    percentage_steel = (suggested_csa_steel / total_suggested_csa) * 100

    cost_aluminium = cost_of_conductor * (percentage_aluminium / 100)
    cost_steel = cost_of_conductor * (percentage_steel / 100)

    supplycost_al = cost_aluminium + 0.05*cost_aluminium
    supplycost_steel= cost_steel +0.05 * cost_steel

    Manf_al = cost_aluminium + 0.1 * cost_aluminium
    Manf_steel = cost_steel + 0.1 * cost_steel

    # Display results
    st.header("Results")

    results = {
        "Parameter": ["Diameter (inches)", "Diameter (mm)", "Radius (mm)", "Cross Sectional Area", "CSA (suggested)", "Percentage", "Cost (in ₹)","Supply Cost (in ₹)","Manufacturing Cost (in ₹)"],
        "Aluminium": [diam_aluminium_inches, diam_aluminium_mm, radius_aluminium_mm, csa_aluminium, suggested_csa_aluminium, percentage_aluminium, cost_aluminium, supplycost_al,Manf_al],
        "Steel": [diam_steel_inches, diam_steel_mm, radius_steel_mm, csa_steel, suggested_csa_steel, percentage_steel, cost_steel, supplycost_steel,Manf_steel]
    }

    results_df = pd.DataFrame(results)

    st.table(results_df)

    total_suggested_csa_result = pd.DataFrame({
        "Total Suggested CSA": [total_suggested_csa],
        "Total Cost (in ₹)": [cost_aluminium + cost_steel],
        "Total Suuply Cost (in ₹) Atleast": [supplycost_al+supplycost_steel],
        "Total Manufacturing Cost (in ₹) Atleast": [Manf_al+Manf_steel],
        "Per KM weight" : [suggested_csa_aluminium+suggested_csa_steel]
    })

    st.table(total_suggested_csa_result)

    Unloading=cost_of_conductor + 0.025* cost_of_conductor
    Stranding = cost_of_conductor + 0.01* cost_of_conductor
    Drawing_Welding= cost_of_conductor + 0.02* cost_of_conductor
    Twisting=cost_of_conductor + 0.01* cost_of_conductor
    Loading =cost_of_conductor + 0.025* cost_of_conductor
    Description = {
        "Parameter": ["Supply Costs (in ₹)","Manufacturing Costs (in ₹)"],
        "Unloading Cost (in ₹)": [Unloading,Unloading],
        "Stranding Cost (in ₹)":[0,Stranding],
        "Drawing and Welding Cost (in ₹)":[0,Drawing_Welding],
        "Twisting Cost (in ₹)":[0,Twisting],
        "Loading Cost (in ₹)":[Loading,Loading]
    }

    Description_df = pd.DataFrame(Description)

    st.table(Description_df)


def SizeCalculatorMM():
    # Title of the app
    st.title("Conductor Cost Calculator")

    # Input fields
    st.header("Input Parameters")

    cost_of_conductor = st.number_input("Cost of Conductor (in ₹)", value=1000)
    diam_aluminium_mm = st.number_input("Diameter of Aluminium (mm)", value=0.000)
    diam_steel_mm = st.number_input("Diameter of Steel (mm)", value=0.000)
    
    # Calculations
    def mm_to_inches(mm):
        return mm / 25.4

    def calculate_csa(diameter_mm):
        radius_mm = diameter_mm / 2
        return 3.14159 * (radius_mm ** 2)
    def al_calculate_scsa(diameter_mm):
        return 12.93*(diameter_mm**2)
    def steel_calculate_scsa(diameter_mm):
        return 6.156*(diameter_mm**2)

    diam_aluminium_inches = mm_to_inches(diam_aluminium_mm)
    diam_steel_inches = mm_to_inches(diam_steel_mm)
    radius_aluminium_mm = diam_aluminium_mm / 2
    radius_steel_mm = diam_steel_mm / 2

    csa_aluminium = calculate_csa(diam_aluminium_mm)
    csa_steel = calculate_csa(diam_steel_mm)

    suggested_csa_aluminium = al_calculate_scsa(diam_aluminium_mm)
    suggested_csa_steel = steel_calculate_scsa(diam_steel_mm)
    total_suggested_csa = suggested_csa_aluminium + suggested_csa_steel

    percentage_aluminium = (suggested_csa_aluminium / total_suggested_csa) * 100
    percentage_steel = (suggested_csa_steel / total_suggested_csa) * 100

    cost_aluminium = cost_of_conductor * (percentage_aluminium / 100)
    cost_steel = cost_of_conductor * (percentage_steel / 100)
    supplycost_al = cost_aluminium + 0.05*cost_aluminium
    supplycost_steel= cost_steel +0.05 * cost_steel

    Manf_al = cost_aluminium + 0.1 * cost_aluminium
    Manf_steel = cost_steel + 0.1 * cost_steel

    # Display results
    st.header("Results")

    results = {
        "Parameter": [ "Diameter (mm)","Diameter (inches)", "Radius (mm)", "Cross Sectional Area", "CSA (suggested)", "Percentage", "Cost (in ₹)","Supply Cost (in ₹)","Manufacturing Cost (in ₹)"],
        "Aluminium": [ diam_aluminium_mm,diam_aluminium_inches, radius_aluminium_mm, csa_aluminium, suggested_csa_aluminium, percentage_aluminium, cost_aluminium, supplycost_al,Manf_al],
        "Steel": [ diam_steel_mm,diam_steel_inches, radius_steel_mm, csa_steel, suggested_csa_steel, percentage_steel, cost_steel, supplycost_steel,Manf_steel]
    }

    results_df = pd.DataFrame(results)

    st.table(results_df)

    total_suggested_csa_result = pd.DataFrame({
        "Total Suggested CSA": [total_suggested_csa],
        "Total Cost (in ₹)": [cost_aluminium + cost_steel],
        "Total Suuply Cost (in ₹) Atleast": [supplycost_al+supplycost_steel],
        "Total Manufacturing Cost (in ₹) Atleast": [Manf_al+Manf_steel],
        "Per KM weight" : [suggested_csa_aluminium+suggested_csa_steel]
    })
    
    st.table(total_suggested_csa_result)

    Unloading=cost_of_conductor + 0.025* cost_of_conductor
    Stranding = cost_of_conductor + 0.01* cost_of_conductor
    Drawing_Welding= cost_of_conductor + 0.02* cost_of_conductor
    Twisting=cost_of_conductor + 0.01* cost_of_conductor
    Loading =cost_of_conductor + 0.025* cost_of_conductor
    Description = {
        "Parameter": ["Supply Costs (in ₹)","Manufacturing Costs (in ₹)"],
        "Unloading Cost (in ₹)": [Unloading,Unloading],
        "Stranding Cost (in ₹)":[0,Stranding],
        "Drawing and Welding Cost (in ₹)":[0,Drawing_Welding],
        "Twisting Cost (in ₹)":[0,Twisting],
        "Loading Cost (in ₹)":[Loading,Loading]
    }

    Description_df = pd.DataFrame(Description)

    st.table(Description_df)

def SWG_to_DA():
    st.title("SWG To Diameter Calculator")

    # Input fields
    st.header("Input Parameter")

    SWG = st.number_input("Enter the SWG Gauge Value", value=0)
    conn=mysql.connector.connect(host='localhost',port="3306",user='root',passwd='Pars@0412',db='Kuber_Inventory')
    c=conn.cursor()
    query=f"SELECT Diameter_inches FROM SWG WHERE SWG = %s"
    c.execute(query,(SWG,))
    result=c.fetchone()
    Diameter=result[0]
    print(Diameter)
    Diameter_inches="%.4f" % float(Diameter)
    print(Diameter_inches)
    Diameter_mm=float(Diameter_inches)*25.4
    SWGCalculator = pd.DataFrame({
        "SWG Value": [SWG],
        "Diameter(inches)": [Diameter_inches],
        "Diameter(mm)" : [Diameter_mm],
        "Area(inches2)":[3.14159 * ((float(Diameter_inches)/2) ** 2)],
        "Area(mm2)":[3.14159 * ((Diameter_mm/2) ** 2)],
        "Area(kcmil)":[(float(Diameter_inches)**2)*1000]
    })
    
    st.table(SWGCalculator)

def Dia_to_SWG():
    st.title("Diameter To SWG Calculator")
    def get_closest_swg(diameter):
        conn=mysql.connector.connect(host='localhost',port="3306",user='root',passwd='Pars@0412',db='Kuber_Inventory')
        c=conn.cursor()
        c.execute("SELECT SWG, Diameter_inches FROM SWG")
        swg_data = c.fetchall()
        
        closest_swg = None
        min_diff = float('inf')
        
        for swg, dia in swg_data:
            diff = abs(float(dia) - diameter)
            if diff < min_diff:
                min_diff = diff
                closest_swg = swg
        
        conn.close()
        return closest_swg, min_diff

    # Input fields
    with st.form(key="Unit"):
        unit=st.selectbox("Unit of Diameter",options=["mm","Inches"])
        submit_button=st.form_submit_button(label="Submit")
        if submit_button:
            if unit=="mm":
                st.header("Input Parameter")
                Diameter_mm = st.number_input("Enter the Diameter in mm", value=0.01)
                Diameter_inches=Diameter_mm/25.4
                SWG,Diff=get_closest_swg(Diameter_inches)
                SWGCalculator = pd.DataFrame({
                    "Diameter(mm)" : [Diameter_mm],
                    "Diameter(inches)": [Diameter_inches],
                    "Closet SWG Value": [SWG],
                    "Difference in size(inches)":[Diff]
                })
                
                st.table(SWGCalculator)
            elif unit=="Inches":
                st.header("Input Parameter")
                Diameter_inches = st.number_input("Enter the Diameter in inches", value=0.01)
                Diameter_mm=Diameter_inches*25.4
                SWG,Diff=get_closest_swg(Diameter_inches)
                SWGCalculator = pd.DataFrame({
                    "Diameter(mm)" : [Diameter_mm],
                    "Diameter(inches)": [Diameter_inches],
                    "Closet SWG Value": [SWG],
                    "Difference in size(inches)":[Diff]
                })
                
                st.table(SWGCalculator)

def layers():
    st.title("Number of Layers")

    # Input fields
    st.header("Input Parameter")

    layer = st.number_input("No. of Layers",value=1)
    Diameter=st.number_input("Diameter(inches)",value=0.01)
    strandcalculator = pd.DataFrame({
        "No. of Layers": [layer],
        "Diameter(inches)": [Diameter],
        "No. of Strands" : [((3*(layer**2))-(3*layer))+1],
        "Overall Diameter" : [Diameter*((2*layer)+1)]
    })

    st.table(strandcalculator)

def RodCost():
    st.title("Rod Cost Calculation")

    # Input fields
    st.header("Input Parameter")

    Rod_Cost=st.number_input("Enter Cost of Rod",value=1.000)
    Rod_to_wire=Rod_Cost+10.000
    Wire_twisting=Rod_to_wire+8.000
    App_cost=Wire_twisting-2.000

    results = {
        "Parameter": [ "Rod Cost(Rs.)","Rod To Wire Cost(Rs.)", "Wire Twisting Cost(Rs.)", "Advanced"],
        "Cost": [Rod_Cost,Rod_to_wire,Wire_twisting,App_cost]
    }

    results_df = pd.DataFrame(results)

    st.table(results_df)
