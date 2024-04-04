# Created by Axin  2023/9/8

import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

is_paused = False
current_frame = 0


def play_animation():
    global is_paused
    if is_paused:
        ani.event_source.start()
        is_paused = False


def pause_animation():
    global is_paused
    if not is_paused:
        ani.event_source.stop()
        is_paused = True


def update_parameters(*args):
    global current_frame
    try:
        new_frequency1 = float(frequency_var1.get())
        new_frequency2 = float(frequency_var2.get())
        phase_shift1 = float(phase_shift_var1.get())
        amplitude1 = float(amplitude_var1.get())  #振幅
        amplitude2 = float(amplitude_var2.get())
        tension = float(tension_var.get())   #拉力，除以10
        density = float(density_var.get())  #线密度
    except ValueError:
        return

    wave_speed = np.sqrt(tension / density)
    wavelength = (wave_speed / new_frequency1)
    # wavelength_var.set(str(wavelength))  # 更新波长λ的值
    wavelength_var.set(str(round(wavelength, 3)))  # 更新波长λ的值，保留三位小数
    draw_wave(new_frequency1, phase_shift1, amplitude1, new_frequency2, phase_shift1, amplitude2, wavelength)
    animate(current_frame)
    canvas.draw()


def animate(i):
    global current_frame
    current_frame = i
    phase_shift1 = i / 10.0  #这里可以一定程度改变波速
    phase_shift2 = -i / 10.0
    tension = float(tension_var.get()) #在这里实现除以20实现拉力变化
    density = float(density_var.get())
    wave_speed = np.sqrt(tension / density)
    try:
        new_frequency1 = float(frequency_var1.get())
        new_frequency2 = float(frequency_var2.get())
    except ValueError:
        return

    wavelength = (wave_speed / new_frequency1)
    wavelength_var.set(str(round(wavelength, 5)))  # 更新波长λ的值，保留三位小数  # 更新波长λ的值
    draw_wave(new_frequency1, phase_shift1, float(amplitude_var1.get()),
              new_frequency2, phase_shift2, float(amplitude_var2.get()), wavelength, tension)
    white_wave_x_var.set(str((np.sqrt(tension / density) / new_frequency1) * 40)) #在这里乘1000，使得横坐标输出变大


def draw_wave(frequency1, phase_shift1, amplitude1, frequency2, phase_shift2, amplitude2, wavelength, tension):
    plt.style.use('dark_background')
    # plt.rcParams['axes.edgecolor'] = 'black'
    x = np.linspace(0, tension * wavelength * 10, 100000, endpoint=False)
    wave1 = amplitude1 * np.sin(2 * np.pi * frequency1 * x + phase_shift1)
    wave2 = amplitude2 * np.sin(2 * np.pi * frequency2 * x + phase_shift2)
    standing_wave = wave1 + wave2

    plt.clf()

    ax3 = plt.subplot(2, 1, 2, facecolor='black')
    ax3.plot(x, standing_wave, color='white', linewidth=2)
    ax3.grid(True)
    # ax3.set_xlim([0, 40 * tension / (float(density_var.get()) * frequency1)])  # x轴
    ax3.set_xlim([0, 0.01 * tension / (float(density_var.get()) * frequency1)])
    # ax3.set_xlim([0, 0.5])
    ax3.set_ylabel('Amplitude (mm)')
    ax3.set_xticklabels([])  # 清空x轴的刻度标签
    try:
        white_wave_x = float(white_wave_x_var.get())
    except ValueError:
        white_wave_x = 0.5

    # ax3.set_xlim([0, white_wave_x])
    # ax3.set_xlim([0, 5])
    ax3.set_ylim([-2 * abs(amplitude1), 2 * abs(amplitude1)])
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.2, hspace=0.4)

root = tk.Tk()
root.configure(bg='black')

input_frame = tk.Frame(root, bg='black')
input_frame.grid(row=2, column=0)

phase_shift_var1 = tk.StringVar()

frequency_var1 = tk.StringVar()
frequency_var1.set('100')  # 设置输入初始值
frequency_var1.trace("w", update_parameters)
frequency_frame1 = tk.Frame(input_frame, bg='black')
frequency_frame1.pack(side='top', pady=(0, 5))  # 使用pack方法来布局
frequency_label1 = tk.Label(frequency_frame1, text="Wave 1 频率:  ", bg='black', fg='red', font=("Helvetica", 25))
frequency_label1.pack(side='left')
frequency_spinbox1 = tk.Spinbox(frequency_frame1, from_=0, to=100, textvariable=frequency_var1, width=8,
                                font=("Helvetica", 25), increment=1)
frequency_spinbox1.pack(side='left')

amplitude_var1 = tk.StringVar()
amplitude_var1.set('15')
amplitude_var1.trace("w", update_parameters)
amplitude_frame1 = tk.Frame(input_frame, bg='black')
amplitude_frame1.pack(side='top', pady=(5, 10))  # 使用pack方法来布局
amplitude_label1 = tk.Label(amplitude_frame1, text="Wave 1 振幅:  ", bg='black', fg='red', font=("Helvetica", 25))
amplitude_label1.pack(side='left')
amplitude_spinbox1 = tk.Spinbox(amplitude_frame1, from_=0, to=100, textvariable=amplitude_var1, width=8,
                                font=("Helvetica", 25), increment=1)
amplitude_spinbox1.pack(side='left')


frequency_var2 = tk.StringVar()
frequency_var2.set('100')
frequency_frame2 = tk.Frame(input_frame, bg='black')
frequency_frame2.pack(side='top', pady=(0, 10))  # 使用pack方法来布局
frequency_label2 = tk.Label(frequency_frame2, text="Wave 2 频率:  ", bg='black', fg='blue', font=("Helvetica", 25))
frequency_label2.pack(side='left')
frequency_spinbox2 = tk.Spinbox(frequency_frame2, from_=0, to=100, textvariable=frequency_var2, width=8,
                                font=("Helvetica", 25), increment=1)
frequency_spinbox2.pack(side='left')

amplitude_var2 = tk.StringVar()
amplitude_var2.set('15')
amplitude_var2.trace("w", update_parameters)
amplitude_frame2 = tk.Frame(input_frame, bg='black')
amplitude_frame2.pack(side='top', pady=(0, 5))  # 使用pack方法来布局
amplitude_label2 = tk.Label(amplitude_frame2, text="Wave 2 振幅:  ", bg='black', fg='blue', font=("Helvetica", 25))
amplitude_label2.pack(side='left')
amplitude_spinbox2 = tk.Spinbox(amplitude_frame2, from_=0, to=100, textvariable=amplitude_var2, width=8,
                                font=("Helvetica", 25), increment=1)

amplitude_spinbox2.pack(side='left')

white_wave_x_var = tk.StringVar()
white_wave_x_var.set('1')  # 设置初始值
white_wave_x_var.trace("w", update_parameters)  # 当值改变时，调用update_parameters函数


white_wave_x_frame = tk.Frame(input_frame, bg='black')
# white_wave_x_frame.pack(side='top', pady=(0, 5))  # 使用pack方法来布局
white_wave_x_label = tk.Label(white_wave_x_frame, text="    横坐标x:      ", bg='black', fg='white', font=("Helvetica", 25))
white_wave_x_label.pack(side='left')
white_wave_x_spinbox = tk.Spinbox(white_wave_x_frame, from_=0, to=100, textvariable=white_wave_x_var, width=8, font=("Helvetica", 25),increment=0.1)
white_wave_x_spinbox.pack(side='left')

tension_var = tk.StringVar()
tension_var.set('2')  # 设置初始值
tension_var.trace("w", update_parameters)  # 当值改变时，调用update_parameters函数

tension_frame = tk.Frame(input_frame, bg='black')
tension_frame.pack(side='top', pady=(0, 5))  # 使用pack方法来布局
tension_label = tk.Label(tension_frame, text="    拉力T(N):    ", bg='black', fg='white', font=("Helvetica", 25))
tension_label.pack(side='left')
tension_spinbox = tk.Spinbox(tension_frame, from_=0, to=100, textvariable=tension_var, width=8, font=("Helvetica", 25),increment=0.1)
tension_spinbox.pack(side='left')

density_var = tk.StringVar()
density_var.set('0.01')  # 设置初始值
density_var.trace("w", update_parameters)  # 当值改变时，调用update_parameters函数

density_frame = tk.Frame(input_frame, bg='black')
density_frame.pack(side='top', pady=(0, 5))  # 使用pack方法来布局
density_label = tk.Label(density_frame, text="线密度ρ(kg/m):", bg='black', fg='white', font=("Helvetica", 25))
density_label.pack(side='left')
density_spinbox = tk.Spinbox(density_frame, from_=0, to=100, textvariable=density_var, width=8, font=("Helvetica", 25),increment=0.001)
density_spinbox.pack(side='left')

wavelength_var = tk.StringVar()
wavelength_frame = tk.Frame(input_frame, bg='black')
wavelength_frame.pack(side='top', pady=(0, 5))  # 使用pack方法来布局
wavelength_label = tk.Label(wavelength_frame, text="  波长λ(m):     ", bg='black', fg='white', font=("Helvetica", 25))
wavelength_label.pack(side='left')
wavelength_label_value = tk.Label(wavelength_frame, textvariable=wavelength_var, bg='black', fg='white', font=("Helvetica", 25))
wavelength_label_value.pack(side='left')

black_frame = tk.Frame(root, bg='black')
black_frame.grid(row=7, column=0, rowspan=20) #排 行 行跨度 波的位置

fig = plt.figure(2, figsize=(20, 8), facecolor='black')
canvas = FigureCanvasTkAgg(fig, master=black_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.configure(background='black')
canvas_widget.pack()

ani = FuncAnimation(fig, animate, frames=100000, interval=0.01, repeat=True)  # frames 是帧率，interval 是每帧间隔时间

button_frame = tk.Frame(root, bg='black')  # 设置两个按钮之间是黑色的
button_frame.grid(row=8, column=0)
# 新建了一个Frame ，使得两个按钮之间间隔很小
play_button = tk.Button(button_frame, text="播放", command=play_animation,
                        bg="black", fg="white", font=("Helvetica", 20), relief="flat", width=20, height=3)
play_button.pack(side='left', padx=(0, 10))

pause_button = tk.Button(button_frame, text="暂停", command=pause_animation,
                         bg="black", fg="white", font=("Helvetica", 20), relief="flat", width=20, height=3)
pause_button.pack(side='left')

root.mainloop()
