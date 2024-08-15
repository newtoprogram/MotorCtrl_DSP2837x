import dearpygui.dearpygui as dpg
from math import sin, ceil
import numpy as np
import threading, time, collections
from scipy.fftpack import fft,ifft


dpg.create_context()

sindatax = []
sindatay = []
sindatay2 = []
for i in range(0, 100):
    sindatax.append(i / 100)
    sindatay.append(5.5 + 0.5 * sin(50 * i / 100))
    sindatay2.append(55.5 + 0.5 * sin(50 * i / 100))

x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)

global NUM, TSC, T_BODE
NUM = 16384
TSC = 1e-4
T_BODE = 600 #unit: [s]

import struct
import socket

class Listen(object):
    def __init__(self, HOST='192.168.4.55', PORT=5001):   #    192.168.56.1
        # establish socket communication
        self.HOST = HOST
        self.PORT = PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.HOST, self.PORT))
            print(
                f"Connected to server, HOST: {self.HOST}, PORT: {self.PORT}. ")
        except socket.error as e:
            print(f"Error: {e}")
    
    def recvall(self, count):
        buf = b''
        while count:
            newbuf = self.socket.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


    def recv_data(self):
        # global data_unpacked
        all_data = b''
        # dt_0 = struct.pack('<i', 1)
        # # while True:
        # self.socket.sendall(dt_0)
        all_data = self.recvall(32*NUM)  #self.socket.recv(6400)
        # all_data += data
        # if len(data) < 6400:
        # # either 0 or end of data
        #     break
        num_floats = 8*NUM
        format_string = f"{num_floats}f"  # 例如：'2if'
        data_unpacked = struct.unpack('<'+format_string, all_data)
            # print(f"Listen: {data_unpacked}")
            
        # dt_0 = struct.pack('<i', 500)
        # # while True:
        # self.socket.sendall(dt_0)
        return data_unpacked    

global step
step = 0

def realtime_update_data():
    global data_x, data_y, data_y2, data_y3, data_y4, data_y5, data_y6, data_y7, data_y8
    global CONSOLE, step    
    
    CONSOLE.counter = 0
    while True:
        if not CONSOLE._pause:
            data = []
            data = Nile_listen.recv_data()
            for i in range(NUM):
                step+=TSC
                data_x.append(step)

            data_y.extend(data[:NUM])
            data_y2.extend(data[NUM:2*NUM])
            data_y3.extend(data[2*NUM:3*NUM])
            data_y4.extend(data[3*NUM:4*NUM])
            data_y5.extend(data[4*NUM:5*NUM])
            data_y6.extend(data[5*NUM:6*NUM])
            data_y7.extend(data[6*NUM:7*NUM])
            data_y8.extend(data[7*NUM:8*NUM])
            
            if step < T_BODE:
                data_y11.extend(data[6*NUM:7*NUM])
                data_y12.extend(data[7*NUM:8*NUM])                
                
            N_sam = len(data_y7)
            resolution = 1/(N_sam*TSC) # [Hz]
            Neff = ceil(N_sam/2) # number of effective points 
            
            x_ref_dft=fft(data_y7)
            x_fdb_dft=fft(data_y8)
            x_ref_hat = np.append(x_ref_dft[0]/N_sam, 2*x_ref_dft[1:Neff+1]/N_sam)  # 原始复数dft结果（双边变单边，除了直流分量，其他分量全部要乘以2）
            x_fdb_hat = np.append(x_fdb_dft[0]/N_sam, 2*x_fdb_dft[1:Neff+1]/N_sam)
            
            x_axis = np.array(list(range(0, Neff+1)))*resolution
            y_axis = abs(x_ref_hat)
            yy_axis = abs(x_fdb_hat)            
            data_hz.extend(x_axis[:CONSOLE.index_f])
            data_y10.extend(y_axis[:CONSOLE.index_f])
            data_y20.extend(yy_axis[:CONSOLE.index_f])
            # Set the series x and y to the last nsamples (using collections.deque)
            if dpg.does_item_exist("tag_realtime_plot1") and dpg.does_item_exist("tag_realtime_plot2") and dpg.does_item_exist("tag_realtime_plot3"):

                dpg.set_value('tag_realtime_plot1', [list(data_x), list(data_y)])
                dpg.fit_axis_data('tag_x_axis')
                dpg.fit_axis_data('tag_y_axis1')      

                # Set the series x and y to the last nsamples (using collections.deque)
                dpg.set_value('tag_realtime_plot2', [list(data_x), list(data_y2)])
                dpg.fit_axis_data('tag_x_axis')
                dpg.fit_axis_data('tag_y_axis1')    

                # Set the series x and y to the last nsamples (using collections.deque)
                dpg.set_value('tag_realtime_plot3', [list(data_x), list(data_y3)])
                dpg.fit_axis_data('tag_x_axis')
                dpg.fit_axis_data('tag_y_axis2')    
  
                # Set the series x and y to the last nsamples (using collections.deque)
                dpg.set_value('tag_realtime_plot4', [list(data_x), list(data_y4)])
                dpg.fit_axis_data('tag_x_axis')
                dpg.fit_axis_data('tag_y_axis2')    

                # Set the series x and y to the last nsamples (using collections.deque)
                dpg.set_value('tag_realtime_plot5', [list(data_x), list(data_y5)])
                dpg.fit_axis_data('tag_x_axis')
                dpg.fit_axis_data('tag_y_axis3')    

                # Set the series x and y to the last nsamples (using collections.deque)
                dpg.set_value('tag_realtime_plot6', [list(data_x), list(data_y6)])
                dpg.fit_axis_data('tag_x_axis')
                dpg.fit_axis_data('tag_y_axis3')

                # Set the series x and y to the last nsamples (using collections.deque)
                dpg.set_value('tag_realtime_plot7', [list(data_x), list(data_y7)])
                dpg.fit_axis_data('tag_x_axis')
                dpg.fit_axis_data('tag_y_axis3')    

                # Set the series x and y to the last nsamples (using collections.deque)
                dpg.set_value('tag_realtime_plot8', [list(data_x), list(data_y8)])
                dpg.fit_axis_data('tag_x_axis')
                dpg.fit_axis_data('tag_y_axis3')
                
                ##FFT                
                dpg.set_value('tag_realtime_plot10', [list(data_hz), list(data_y10)])
                dpg.fit_axis_data('tag_fs_axis')
                dpg.fit_axis_data('tag_fft_axis')
                dpg.bind_item_theme("tag_realtime_plot10", "plot_theme_green")
                
                dpg.set_value('tag_realtime_plot20', [list(data_hz), list(data_y20)])
                dpg.fit_axis_data('tag_fs_axis')
                dpg.fit_axis_data('tag_fft_axis')
                dpg.bind_item_theme("tag_realtime_plot20", "plot_theme_yellow")     
                
            # if dpg.does_item_exist("tag_realtime_plot13") and dpg.does_item_exist("tag_realtime_plot14"):  
            #     ##BODE PLOT                
            #     dpg.set_value('tag_realtime_plot13', [list(data_bode), list(data_y13)])
            #     dpg.fit_axis_data('bode_fs_axis')
            #     dpg.fit_axis_data('bode_amp_axis')
                
            #     dpg.set_value('tag_realtime_plot14', [list(data_bode), list(data_y14)])
            #     dpg.fit_axis_data('bode_fs_axis')
            #     dpg.fit_axis_data('bode_phase_axis')

            time.sleep(0.00001) # limit resource usage   
        else:
            time.sleep(0.00001)

with dpg.font_registry():
    default_font = dpg.add_font("./Roboto-Black.ttf", 15)
    
    
window_states = {
    "Wave Scope": False,
    "Bode Scope": False,
}

def on_close_window(button_id):
    global window_states
    window_tag = f"window_{button_id}"
    dpg.delete_item(window_tag)
    window_states[button_id] = False
    data_bode.clear()
    data_y13.clear()
    data_y14.clear()

  
def on_wave_scope(button_id):
    global window_states
    if not window_states[button_id]:
        window_tag = f"window_{button_id}"
        with dpg.window(label=f"{button_id} Window",tag=window_tag, on_close=lambda: on_close_window(button_id), width=600, height=900):
            dpg.bind_font(default_font)           
            
            with dpg.plot(label="Multi Axes Plot", height=400, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="x / [s]",  tag='tag_x_axis')
                dpg.add_plot_axis(dpg.mvYAxis, label="current / [Ap]", tag='tag_y_axis1')
                dpg.add_line_series(x=list(data_x),y=list(data_y), label='data_y',  parent='tag_y_axis1', tag='tag_realtime_plot1')
                dpg.add_line_series(x=list(data_x),y=list(data_y2), label='data_y2', parent='tag_y_axis1', tag='tag_realtime_plot2')
                # create y axis 2
                dpg.add_plot_axis(dpg.mvYAxis, label="velocity / [rpm]", tag='tag_y_axis2')
                dpg.add_line_series(x=list(data_x),y=list(data_y3), label='data_y3',  parent='tag_y_axis2', tag='tag_realtime_plot3')
                dpg.add_line_series(x=list(data_x),y=list(data_y4), label='data_y4',  parent='tag_y_axis2', tag='tag_realtime_plot4')
                # create y axis 3
                dpg.add_plot_axis(dpg.mvYAxis, label="voltage / [Vp]", tag='tag_y_axis3')
                dpg.add_line_series(x=list(data_x),y=list(data_y5), label='data_y5',  parent='tag_y_axis3', tag='tag_realtime_plot5')
                dpg.add_line_series(x=list(data_x),y=list(data_y6), label='data_y6',  parent='tag_y_axis3', tag='tag_realtime_plot6')
                dpg.add_line_series(x=list(data_x),y=list(data_y7), label='data_y7',  parent='tag_y_axis3', tag='tag_realtime_plot7')
                dpg.add_line_series(x=list(data_x),y=list(data_y8), label='data_y8',  parent='tag_y_axis3', tag='tag_realtime_plot8')
                
                dpg.bind_item_theme("tag_realtime_plot1", "plot_theme_green")
                dpg.bind_item_theme("tag_realtime_plot2", "plot_theme_blue")
                
            
            with dpg.plot(label="FFT for Velocity", height=400, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="x / [Hz]",  tag='tag_fs_axis')
                dpg.add_plot_axis(dpg.mvYAxis, label="Amp / []", tag='tag_fft_axis')
                dpg.add_line_series(x=list(data_hz),y=list(data_y10), label='FFT-ref',  parent='tag_fft_axis', tag='tag_realtime_plot10')
                dpg.add_line_series(x=list(data_hz),y=list(data_y20), label='FFT-fdb',  parent='tag_fft_axis', tag='tag_realtime_plot20')
                
                
            b3 = dpg.add_button(label="Stop/Start Animation", callback=_stop_animation)
                
            window_states[button_id] = True
            
            thread = threading.Thread(target=realtime_update_data)
            thread.daemon = True
            thread.start()


def on_bode_scope(button_id):
    global window_states
    CONSOLE._pause ^= True
    time.sleep(0.1)
    if not window_states[button_id]:
        window_tag = f"window_{button_id}"
        with dpg.window(label=f"{button_id} Window",tag=window_tag, on_close=lambda: on_close_window(button_id), width=600, height=500):
            dpg.bind_font(default_font)           
            data_bode.clear()
            data_y13.clear()
            data_y14.clear()
            ################################################################
            if  not window_states[button_id]:
                bode_N_sam = len(data_y11)
                bode_resolution = 1/(bode_N_sam*TSC) # [Hz]
                bode_Neff = ceil(bode_N_sam/2) # number of effective points 
                
                bode_x_ref_dft=fft(data_y11)
                bode_x_fdb_dft=fft(data_y12)
                bode_x_ref_hat = np.append(bode_x_ref_dft[0]/bode_N_sam, 2*bode_x_ref_dft[1:bode_Neff+1]/bode_N_sam)  # 原始复数dft结果（双边变单边，除了直流分量，其他分量全部要乘以2）
                bode_x_fdb_hat = np.append(bode_x_fdb_dft[0]/bode_N_sam, 2*bode_x_fdb_dft[1:bode_Neff+1]/bode_N_sam)
                
                bode_x_axis = np.array(list(range(0, bode_Neff+1)))*bode_resolution
                bode_amp_axis = [qep/ref for ref, qep in zip(abs(bode_x_ref_hat), abs(bode_x_fdb_hat))] #abs(bode_x_ref_hat)
                bode_phase_axis = [qep-ref for ref, qep in zip(np.arctan2(bode_x_ref_hat.imag, bode_x_ref_hat.real), np.arctan2(bode_x_fdb_hat.imag, bode_x_fdb_hat.real))]
                
                motor_phase = []
                M_VL_AF = []
                M_VL_PF = []
                for ii in bode_phase_axis :
                    if ii > np.pi :
                      ii = ii - 2* np.pi
                    elif ii < -np.pi :
                      ii = ii + 2* np.pi  
                    motor_phase.append(ii)  
                      
                M_VL_AF = [20*np.log10(el) for el in bode_amp_axis]
                M_VL_PF = [(el)/np.pi*180 for el in motor_phase]
                index_max = ceil(CONSOLE.max_freq*(bode_N_sam*TSC))
                data_bode.extend(bode_x_axis[:index_max])
                data_y13.extend(M_VL_AF[:index_max])
                data_y14.extend(M_VL_PF[:index_max])
            ################################################################
            
            with dpg.plot(label="Bode Plot", height=400, width=-1):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="x / [Hz]",  tag='bode_fs_axis')
                dpg.add_plot_axis(dpg.mvYAxis, label="amp / [db]", tag='bode_amp_axis')
                dpg.add_line_series(x=list(data_bode),y=list(data_y13), label='bode_amp',  parent='bode_amp_axis', tag='tag_realtime_plot13')
                # create y axis 2
                dpg.add_plot_axis(dpg.mvYAxis, label="degree / [°]", tag='bode_phase_axis')
                dpg.add_line_series(x=list(data_bode),y=list(data_y14), label='bode_phase',  parent='bode_phase_axis', tag='tag_realtime_plot14')
                
                dpg.bind_item_theme("tag_realtime_plot13", "plot_theme_yellow")
                dpg.bind_item_theme("tag_realtime_plot14", "plot_theme_blue")    
                

            
            window_states[button_id] = True
            
            

def _stop_animation(sender, app_data): CONSOLE._pause ^= True

with dpg.window(label="Tutorial", width=900, height=900, tag="__demo_primary_window"):
    dpg.bind_font(default_font)
    with dpg.theme(tag="plot_theme_yellow"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (150, 255, 0), category=dpg.mvThemeCat_Plots)
            # dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, dpg.mvPlotMarker_Diamond, category=dpg.mvThemeCat_Plots)
            # dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 4, category=dpg.mvThemeCat_Plots)

    with dpg.theme(tag="plot_theme_blue"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (0, 199, 140), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, dpg.mvPlotMarker_Square, category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 4, category=dpg.mvThemeCat_Plots)
            
    with dpg.theme(tag="plot_theme_green"):
        with dpg.theme_component(dpg.mvLineSeries):
            dpg.add_theme_color(dpg.mvPlotCol_Line, (153, 51, 250), category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, dpg.mvPlotMarker_Square, category=dpg.mvThemeCat_Plots)
            dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 4, category=dpg.mvThemeCat_Plots)

            
    with dpg.plot(label="Multi Axes Plot 2", height=300, width=-1):
        dpg.add_plot_legend()
        # create x axis
        dpg.add_plot_axis(dpg.mvXAxis, label="x")

        # create y axis 1
        dpg.add_plot_axis(dpg.mvYAxis, label="y1")
        dpg.add_line_series(x, y1, tag="y1 lines", label="y1 lines", parent=dpg.last_item())

        # create y axis 2
        dpg.add_plot_axis(dpg.mvYAxis, label="y2")
        dpg.add_line_series(x, y2, tag="y2 lines",label="y2 stem", parent=dpg.last_item())

        # create y axis 3
        dpg.add_plot_axis(dpg.mvYAxis, label="y3 scatter")
        dpg.add_line_series(x, y3, tag="y3 lines",label="y3", parent=dpg.last_item())
        
        dpg.bind_item_theme("y1 lines", "plot_theme_yellow")
        dpg.bind_item_theme("y2 lines", "plot_theme_blue")
        dpg.bind_item_theme("y3 lines", "plot_theme_green")
        
    with dpg.menu_bar():
        with dpg.menu(label="Themes"):
            dpg.add_menu_item(label="Dark")
            dpg.add_menu_item(label="Light")
            dpg.add_menu_item(label="Classic")
        with dpg.menu(label="Other Themes"):
            dpg.add_menu_item(label="Purple")
            dpg.add_menu_item(label="Gold")
            dpg.add_menu_item(label="Red")
        with dpg.menu(label="Tools"):
            dpg.add_menu_item(label="Wave Scope",callback=lambda: on_wave_scope("Wave Scope"))
            dpg.add_menu_item(label="Bode Scope",callback=lambda: on_bode_scope("Bode Scope"))

dpg.set_primary_window("__demo_primary_window", True)

with dpg.handler_registry():
        def _on_press_mvKey_Control(sender, app_data):
            if dpg.is_key_down(dpg.mvKey_A):
                print("Ctrl + A")
        dpg.add_key_press_handler(dpg.mvKey_Control, callback=_on_press_mvKey_Control)
        dpg.add_key_press_handler(dpg.mvKey_Spacebar, callback=_stop_animation)  


class THE_CONSOLE:
    """ User control over the simulation animation """
    nsamples : int = 1*NUM
    numba__scope_dict: dict = None
    _pause : int = False
    counter: int = 0
    max_freq: int = 500 #HZ
    index_f: int = ceil(max_freq*(nsamples*TSC))  ##HZ -x-axis
    index_bode: int = ceil((T_BODE+5)/(TSC))


if __name__ == '__main__':
    Nile_listen = Listen()
    global CONSOLE
    CONSOLE = THE_CONSOLE()    
    global data_x, data_y, data_y2, data_y3, data_y4, data_y5, data_y6, data_y7, data_y8
    global data_hz, data_y10, data_y11, data_y12
    # Can use collections if you only need the last 100 samples
    data_x = collections.deque([0.0, 0.0], maxlen=CONSOLE.nsamples)
    data_y = collections.deque([0.0, 0.0], maxlen=CONSOLE.nsamples)
    data_y2 = collections.deque([0.0, 0.0], maxlen=CONSOLE.nsamples)    
    data_y3 = collections.deque([0.0, 0.0], maxlen=CONSOLE.nsamples) 
    data_y4 = collections.deque([0.0, 0.0], maxlen=CONSOLE.nsamples) 
    data_y5 = collections.deque([0.0, 0.0], maxlen=CONSOLE.nsamples)
    data_y6 = collections.deque([0.0, 0.0], maxlen=CONSOLE.nsamples)    
    data_y7 = collections.deque([0.0, 0.0], maxlen=CONSOLE.nsamples) 
    data_y8 = collections.deque([0.0, 0.0], maxlen=CONSOLE.nsamples) 
    data_hz = collections.deque([0.0, 0.0],  maxlen=CONSOLE.index_f) 
    data_y10 = collections.deque([0.0, 0.0], maxlen=CONSOLE.index_f) #ref
    data_y20 = collections.deque([0.0, 0.0], maxlen=CONSOLE.index_f) #fdb
    
    data_bode= collections.deque([0.0, 0.0], maxlen=CONSOLE.index_bode) #HZ range
    data_y11 = collections.deque([0.0, 0.0], maxlen=CONSOLE.index_bode) #ref for fft
    data_y12 = collections.deque([0.0, 0.0], maxlen=CONSOLE.index_bode) #fdb for fft
    data_y13 = collections.deque([0.0, 0.0], maxlen=CONSOLE.index_bode) #fdb/ref:amp
    data_y14 = collections.deque([0.0, 0.0], maxlen=CONSOLE.index_bode) #fdb/ref:phase
    data_bode.clear()
    data_y11.clear()
    data_y12.clear()
    data_y13.clear()
    data_y14.clear() 
        
    dpg.create_viewport(title='MOTOR Servo', width=900, height=900, small_icon='0.ico', large_icon='0.ico')

    # show_dem_demo(CONSOLE)
    dpg.setup_dearpygui()
    dpg.show_viewport()    

    dpg.start_dearpygui()    
    dpg.destroy_context()



# import numpy as np
# from scipy.fftpack import fft,ifft
# import matplotlib.pyplot as plt
# import math

# fs = 100000
# N = 16
# n = range(0,N)  
# t = [i/fs for i in n]
# y0 = [np.sin(2*np.pi*(5*(j)))+2*np.sin(2*np.pi*(5*(j)))  for j in t]

# x_qep_dft=fft(y0)

# print(x_qep_dft)

# resolution = fs/N # [Hz]
# Neff = math.ceil(N/2) # number of effective points                     
# x_qep_hat = np.append(x_qep_dft[0]/N, 2*x_qep_dft[1:Neff+1]/N)

# # # Plot DFT for human to read

# plt.figure(1, figsize=(10,4))
# plt.plot(t,y0)
# plt.figure(2, figsize=(10,4))
# plt.plot(np.array(list(range(0, Neff+1)))*resolution, abs(x_qep_hat), '--o', alpha=0.5, label='qep');
# plt.show()
