######################################ALEXANDER MILLER AND MAX HEARNDEN, 31ST JULY TO 3RD AUGUST
######################################ECONOMIC CALCULATIONS DONE BY HARRY TOUBE
######################################ECONOMY SIM v1.0
import sqlite3
import sys
import tkinter
import matplotlib.pyplot as plot
window = tkinter.Tk()
tariff_rate_a = 5
tariff_rate_l = 10
tariff_rate_o = 10
tariff_rate_e = 10
tariff_rate_elec= 5
print("Please note - only tariffs between 0 and 30 will work due to there only being data for that")
print("The current income tax rate is a flat tax of 35%")

elec_price =2300 ##electronics
a_price = 3762 #agri
o_price = 6804 ##ore
e_price = 34906.18##energy
m_price = 9570.03 ##medicine
man_price = 12319.4520124 ##manufacturing
trans_price = 9050
##gdp = [(a_price+o_price+e_price+m_price+man_price)]
con = sqlite3.connect('food.db')
##for calculating gdp
###########################################
const = 20844113804390 #total gdp + all labour costs
##workforces for each sector
wf_t = 4640000
wf_h = 8318500
wf_f = 13445360
wf_tech = 6700000
wf_u = 198130
wf_man = 12400000
incmtax_rate = 0
##wages for each sector
wage_t= 37660
wage_h = 79160
wage_f = 25000
wage_tech = 76540
wage_u = 55003
wage_man = 50083
def change_gdp():
    ##Gdp is calculated by`
    ###3574470584390 - (total workforce * (wages + tariff effects))
    ##tariff effects = adjusted  tariff costs - base costs
    gdp = const
    gdp= gdp-  ((wf_t *(wage_t+((o_price+e_price)-9050)))+
                  (wf_h *(wage_h+((m_price)-9570.03)))+
                  (wf_f *(wage_f+((a_price)-3762)))+
                  (wf_tech *(wage_tech+((elec_price)-2300)))+
                  (wf_u *(wage_u+((e_price)-34906.18)))+
                  (wf_man *(wage_man+((man_price)-12319.4520124))))
    for i in range(0,incmtax_rate):
        gdp = gdp*(incmtax_rate*0.97)
    return gdp

print("Your current GDP is",change_gdp())
##def prop(variable_to_be_decremented,previous_value_of_other_variable,new_value_of_other_variable):
##    a=new_value_of_other_variable-previous_value_of_other_variable
##    return -3*a+variable_to_be_decremented    
def predict(a,commodity):
    def wval(a):
        b=[0.5,1,2,5,10,20,30,100]
        for i in range(len(b)-1):
            if a<b[i]:
                return [b[i-1],b[i]]
        return [b[-2],b[-1]]
    def line(x1,y1,x2,y2,x3):
        m = (y1-y2)/(x1-x2)
        c = y1-(x1 * m)
        return (m * x3)+c
    def getval(v,c):##v is the tariff increase, c is the commodity
        cs = con.cursor()
        cs.execute("SELECT Price FROM "+str(c)+" WHERE Tariff = "+str(v))
        foo = cs.fetchall()
        for row in foo:
            r = row[0]
        return r
        
    values=wval(a)
    return line(values[0],getval(values[0],commodity),values[1],getval(values[1],commodity),a)

def agriculture_tariff(t):
    
    print("The current tariff on agricultural imports is",t)
    t = float(input("Please enter the amount you would like to Change the tariff on agricultural products(dairy products, wheat, etc)"))
    if (t > 30 or t <0.0000000000000000000000000000001):
        print("That's not a valid input, please enter an input above 0 and below 30")
    else:
        cs = con.cursor()
        cs.execute( "SELECT * FROM food_prices WHERE Tariff = ?;", (t,) )
        p_f_o = cs.fetchall()
        if( len(p_f_o) == 0 ) :
            cs.execute("INSERT INTO food_prices (Tariff,Price) VALUES(?,?)",(t, predict(t,"food_prices")))
            cs.execute("COMMIT;")
            cs.execute("SELECT Price FROM food_prices WHERE Tariff = ?",(t,))
            p_f_o = cs.fetchall()
        else:
            cs.execute("SELECT Price FROM food_prices WHERE Tariff = ?",(t,))
            p_f_o = cs.fetchall()
        for row in p_f_o:
            print ("The new average price per person per year for food is now",row[0])
            global a_price
            a_price = row[0]
            change_gdp()

        
        
def luxury_tariff(t):
    
    print("The current tariff on agricultural imports is",t)
    t = float(input("Please enter the amount you would like to Change the tariff on luxury products(medicine etc)"))
    if (t > 30 or t <0.0000000000000000000000000000001):
        print("That's not a valid input, please enter an input above 0 and below 30")
    else:
        cs = con.cursor()
        cs.execute( "SELECT * FROM healthcare_costs WHERE Tariff = ?;", (t,) )
        p_f_o = cs.fetchall()
        if( len(p_f_o) == 0 ) :
            cs.execute("INSERT INTO healthcare_costs (Tariff,Price) VALUES(?,?)",(t, predict(t,"healthcare_costs")))
            cs.execute("COMMIT;")
            cs.execute("SELECT Price FROM healthcare_costs WHERE Tariff = ?",(t,))
            p_f_o = cs.fetchall()
        else:
            cs.execute("SELECT Price FROM healthcare_costs WHERE Tariff = ?",(t,))
            p_f_o = cs.fetchall()
        for row in p_f_o:
            print ("The new average price per person per year for healthcare is now",row[0])
            change_gdp()
            global m_price
            m_price = row[0]
    ####################################################################
        cs.execute( "SELECT * FROM manufacturing WHERE Tariff = ?;", (t,) )
        p_f_o = cs.fetchall()
        if( len(p_f_o) == 0 ) :
            cs.execute("INSERT INTO manufacturing (Tariff,Price) VALUES(?,?)",(t, predict(t,"manufacturing")))
            cs.execute("COMMIT;")
            cs.execute("SELECT Price FROM manufacturing WHERE Tariff = ?",(t,))
            p_f_o = cs.fetchall()
        else:
            cs.execute("SELECT Price FROM manufacturing WHERE Tariff = ?",(t,))
            p_f_o = cs.fetchall()
        for row in p_f_o:
            print ("The new average price per person per year for manufactured goods is now",row[0])
            change_gdp()
            
            global o_price
            o_price = row[0]

        
def ore_tariff(t):
    
    print("The current tariff on ore imports is",t)
    t = float(input("Please enter the amount you would like to Change the tariff on ore (steel etc)"))
    cs = con.cursor() 
    cs.execute( "SELECT * FROM ore_prices WHERE Tariff = ?;", (t,) )
    
    p_f_o = cs.fetchall()
    if( len(p_f_o) == 0 ) :
        cs.execute("INSERT INTO ore_prices (Tariff,Price) VALUES(?,?)",(t, predict(t,"ore_prices")))
        cs.execute("COMMIT;")
        cs.execute("SELECT Price FROM ore_prices WHERE Tariff = ?",(t,))
        p_f_o = cs.fetchall()
    else:
        cs.execute("SELECT Price FROM ore_prices WHERE Tariff = ?",(t,))
        p_f_o = cs.fetchall()
    for row in p_f_o:
        print ("The new average price per person per year for ore is now",row[0])
        change_gdp()
        global o_price
        o_price = row[0]
        
def energy_tariff(t):
    
    print("The current tariff on energy imports is",t)
    t = float(input("Please enter the amount you would like to Change the tariff on energy (oil etc)"))
    cs = con.cursor() 
    cs.execute( "SELECT * FROM energy_price WHERE Tariff = ?;", (t,) )
    
    p_f_o = cs.fetchall()
    if( len(p_f_o) == 0 ) :
        cs.execute("INSERT INTO energy_price (Tariff,Price) VALUES(?,?)",(t, predict(t,"energy_price")))
        cs.execute("COMMIT;")
        cs.execute("SELECT Price FROM energy_price WHERE Tariff = ?",(t,))
        p_f_o = cs.fetchall()
    else:
        cs.execute("SELECT Price FROM energy_price WHERE Tariff = ?",(t,))
        p_f_o = cs.fetchall()
    for row in p_f_o:
        print ("The new average price per person per year for energy is now",row[0])
        change_gdp()
        global e_price
        e_price = row[0]
        
        
def elec_tariff(t):
    
    print("The current tariff on electronics imports is",t)
    t = float(input("Please enter the amount you would like to Change the tariff on electronics (computers etc)"))
    if (t > 30 or t <0.0000000000000000000000000000001):
        print("That's not a valid input, please enter an input above 0 and below 30")
    else:
        cs = con.cursor() 

        ##################################
        cs.execute( "SELECT * FROM elec_prices WHERE Tariff = ?;", (t,) )
        
        p_f_o = cs.fetchall()
        if( len(p_f_o) == 0 ) :
            cs.execute("INSERT INTO elec_prices (Tariff,Price) VALUES(?,?)",(t, predict(t,"elec_prices")))
            cs.execute("COMMIT;")
            cs.execute("SELECT Price FROM elec_prices WHERE Tariff = ?",(t,))
            p_f_o = cs.fetchall()
        else:
            cs.execute("SELECT Price FROM elec_prices WHERE Tariff = ?",(t,))
            p_f_o = cs.fetchall()
        for row in p_f_o:
            print ("The new average price per person per year for electronics is now",row[0])
            change_gdp()
            global elec_price
            elec_price = row[0]

window.title("Options")
def callback_a():
    agriculture_tariff(tariff_rate_a)
b_a = tkinter.Button(text="Change tariffs on agriculture", command=callback_a)
b_a.pack(side = "left",fill="x", expand=1)

def callback_l():
    luxury_tariff(tariff_rate_l)
b_l = tkinter.Button(text="Change tariffs on luxuries", command=callback_l )
b_l.pack(side = "left",fill="x", expand=1)

def callback_o():
    ore_tariff(tariff_rate_o)
b_o = tkinter.Button(text="Change tariffs on ore", command=callback_o)
b_o.pack(side = "left",fill="x", expand=1)

def callback_e():
    energy_tariff(tariff_rate_e)
b_e = tkinter.Button(text="Change tariffs on energy", command=callback_e)
b_e.pack(side = "left",fill="x", expand=1)

def callback_elec():
    elec_tariff(tariff_rate_elec)
b_elec = tkinter.Button(text="Change tariffs on electronics", command=callback_elec)
b_elec.pack(side = "left",fill="x", expand=1)

def callback_trans():
    print("The value of the transport sector is currently",(o_price+e_price))
tra_elec = tkinter.Button(text="View transport prices", command=callback_trans)
tra_elec.pack(side = "left",fill="x", expand=1)

def callback_util():
    print("The value of the utilities sector is currently",(e_price))
tra_util = tkinter.Button(text="View utilities prices", command=callback_util)
tra_util.pack(side = "left",fill="x", expand=1)


def callback_gdp():
    print("Estimated GDP is now",str(change_gdp()))
gdp = tkinter.Button(text="View GDP", command=callback_gdp)
gdp.pack(side = "left",fill="x", expand=1)

def callback_incmtax():
    try:
        c = int(input("Please enter the amount you wish to raise the income tax rate by"))
        global incmtax_rate
        incmtax_rate = c
        print("The new income tax rate is",(35+c),"%")
    except:
        print("Whole numbers only, please!")
        callback_incmtax()
    
    

mw = tkinter.Button(text="Raise income tax", command=callback_incmtax)
mw.pack(side = "left",fill="x", expand=1)
def callback_viewstats():
      print("The tariff rate on agricultural products is",tariff_rate_a,"%")
      print("The tariff rate on luxury products is",tariff_rate_l,"%")
      print("The tariff rate on ore is",tariff_rate_o,"%")
      print("The tariff rate on energy is",tariff_rate_e,"%")
      print("The tariff rate on electrical products is",tariff_rate_elec,"%")
      print("The price per person for food is $",a_price)
      print("The price per person for steel is $",o_price)
      print("The price per person for energy is $",e_price)
      print("The price per person for medicine is $",m_price)
      print("The price per person for manufactured goods is $",man_price)
      print("The price per person for transport is $",trans_price)
      print("The price per person for electronic products is $",elec_price)
      print("The workforce for the transport sector is",wf_t,"people")
      print("The workforce for the healthcare sector is",wf_h,"people")
      print("The workforce for the food sector is",wf_f,"people")
      print("The workforce for the technology sector is",wf_tech,"people")
      print("The workforce for the utilities sector is",wf_u,"people")
      print("The workforce for the manufacturing sector is",wf_man,"people")  
      print("Your income tax rate is",(35+incmtax_rate),"%")
      print("The average wage in the transport sector is $",wage_t)
      print("The average wage in the healthcare sector is $",wage_h)
      print("The average wage in the food sector is $",wage_f)
      print("The average wage in the technology sector is $",wage_tech)
      print("The average wage in the manufacturing sector is $",wage_man)
      print("The average wage in the utilities sector is $",wage_u)

s= tkinter.Button(text="View stats", command=callback_viewstats)
s.pack(side = "left",fill="x", expand=1)


