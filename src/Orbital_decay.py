import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


#Constant
mu =3.986e14    #Earth's gravitational parameter [m^3/s^2]
Re= 6.371e6     #Earth's radius [m]
h_reentry = 150e3      #reentry altitude [m]
day= 86400      # [s]
year= 365.25 *day #[s]
years_Max= 30  #max simulation duration [years]



#Satellite specification (assumption for cube satellites)
Cd = 2.2   # resistance coefficient
Mass = 4.0 #[kg]
A = 0.03 #[m^2]

def ballistic(area):
    "B = Cd*A/m [m^2/kg]."
    return Cd * area/ Mass
B= ballistic(A)

#Density
# Density [kg/m^3] from NRLMSIS 2.0 via pymsis
# average over 24 hours and over 30 points (6 longitudes x 5 latitudes)
h_tab = np.array([150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 700, 800]) *1e3
d_active = np.array([1.69e-09, 2.55e-10, 6.99e-11, 2.40e-11, 9.34e-12, 3.91e-12,
                       1.73e-12, 7.92e-13, 3.77e-13, 1.86e-13, 5.13e-14, 1.77e-14])
# d(h)= log-interpolation of h_tab and d_tab
def d(h):
    return np.exp(np.interp(h,h_tab, np.log(d_active)))



#Model
#differential equation as a model for height 
def f(t,y,B):
    h= y[0]
    return [-d(h)*B*np.sqrt(mu*(Re+h))]

#simulation stops y[0]-150e3 equals 0 thus meaning satellite exited the horbit
def reentry (t, y, B):
    return y[0]- h_reentry
reentry.terminal = True
reentry.direction = -1


#differential equation solution starting at given altitude h0, time span = years_max years, stop event = reentry, solution metod LSODA, max step 1 day 
def simulate(h0_km, B, years_max=years_Max):
    sol = solve_ivp(f, [0.0, years_max * year], [h0_km * 1e3],
                    args=(B,),events=reentry, method='LSODA', max_step=day,
                    rtol=1e-8, atol=1.0)
    reentered = sol.t_events[0].size > 0
    return sol.t / day, sol.y[0] / 1e3, reentered

#Graph

for h0 in [300, 400, 500, 600]:
    t, h, reentered = simulate(h0, B)
    plt.plot(t / 365.25, h, label=f'{h0} km')
    print(h0, 'km:', round(t[-1] / 365.25, 2), 'years')

plt.xlabel('Time [years]')
plt.ylabel('altitude [km]')
plt.title('Orbital decay, CubeSat 3U')
plt.legend()
plt.grid(alpha=0.3)
plt.savefig('decay_vs_time.png', dpi=200, bbox_inches='tight')
plt.show()




#ISS Validation
M_ISS= 420000 #[Kg]
A_ISS= 1600 #[m^2]     ## Estimated area and mass of the ISS
B_ISS= 2.2 *A_ISS/M_ISS

t, h, reentered = simulate(400, B_ISS, years_max=30 / 365.25)
print('ISS: decay in 30 days =', round(h[0] - h[-1], 2), 'km')
    

#Area sensibility 
B_end = ballistic(0.01)
for h0 in [300, 400, 500, 600]:
    t, h, reentered = simulate(h0, B_end)
    print(h0, 'km:', round(t[-1] / 365.25, 2), 'years', '' if reentered else '(more than 30 years)')