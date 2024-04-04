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


def draw_wave(frequency1, phase_shift1, amplitude1, frequency2, phase_shift2, amplitude2):
    plt.style.use('dark_background')
    plt.rcParams['axes.edgecolor'] = 'black'
    t = np.linspace(-1, 1, 80000,
                    endpoint=False)  # np.linspace(-100, 100,80000, endpoint=False)表示在-100到100之间生成8w个均匀间隔的数字。
    wave1 = amplitude1 * np.sin(2 * np.pi * frequency1 * t + phase_shift1)
    wave2 = -amplitude2 * np.sin(2 * np.pi * frequency2 * t + phase_shift2)
    standing_wave = wave1 + wave2

    # Clear the entire figure
    plt.clf()

    # Create 3 subplots with black background
    ax1 = plt.subplot(2, 2, 1, facecolor='black', )  # 红波在左
    ax2 = plt.subplot(2, 2, 2, facecolor='black')  # 蓝波在右
    ax3 = plt.subplot(2, 1, 2, facecolor='black')  # 白波在下

    ax1.plot(t, wave1, color='red', linewidth=2)  # 红波
    ax1.grid(True)  # True坐标系显示，False是不显示
    ax1.set_xlabel('Wavelength  (m)')
    ax1.set_ylabel('Amplitude (mm)')
    ax1.set_xlim([0, 0.3])  # 0-0.3 是t轴的区间
    ax1.set_ylim([-2 * abs(amplitude1), 2 * abs(amplitude1)])

    ax2.plot(t, wave2, color='blue', linewidth=2)  # 蓝波
    ax2.grid(True)
    ax2.set_xlabel('Wavelength (m)')
    ax2.set_ylabel('Amplitude (mm)')
    ax2.set_xlim([0, 0.3])  # 0-0.3 是t轴的区间
    ax2.set_ylim([-2 * abs(amplitude1), 2 * abs(amplitude1)])

    ax3.plot(t, standing_wave, color='white', linewidth=2)  # 白波（叠加波） linewidth是线的粗细程度
    ax3.grid(True)
    ax3.set_xlabel('Wavelength  (m)')
    ax3.set_ylabel('Amplitude (mm)')
    ax3.set_xlim([0, 0.5])  # 0-0.5 是t轴的区间
    ax3.set_ylim([-2 * abs(amplitude1), 2 * abs(amplitude1)])
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.2, hspace=0.4)  # 调整三个子图之间的间隔


def animate(i):
    global current_frame
    if is_paused:
        return
    current_frame = i

    # 获取输入框的值作为相位偏移值
    try:
        phase_shift1_from_input = float(input_phase_var1.get())
        phase_shift2_from_input = float(input_phase_var2.get())
    except ValueError:
        phase_shift1_from_input = 0
        phase_shift2_from_input = np.pi/2

    phase_shift1 = phase_shift1_from_input + i / 20.0
    phase_shift2 = phase_shift2_from_input - i / 20.0

    # 更新wave参数并重新绘制波形
    update_parameters_with_phase(phase_shift1, phase_shift2)

    # 更新画布
    canvas.draw()


def update_parameters_with_phase(phase_shift1, phase_shift2):
    try:
        frequency1 = float(frequency_var1.get())
        amplitude1 = float(amplitude_var1.get())
        frequency2 = float(frequency_var2.get())
        amplitude2 = float(amplitude_var2.get())
    except ValueError:
        return

    draw_wave(frequency1, phase_shift1, amplitude1, frequency2, phase_shift2, amplitude2)


def update_parameters(*args):
    input_phase_var1 = tk.StringVar()
    input_phase_var2 = tk.StringVar()
    update_parameters_with_phase(float(phase_shift_var1.get()), float(phase_shift_var2.get()))


root = tk.Tk()
root.configure(bg='black')

# image = Image.open(".\\img\\img1.png")
# photo = ImageTk.PhotoImage(image)
# image_label = tk.Label(root, image=photo)
# image_label.grid(row=0, column=0)

input_phase_var1 = tk.StringVar()
input_phase_var1.set('0') # 初始值设为0
input_phase_var2 = tk.StringVar()
input_phase_var2.set('0') # 初始值设为0

frequency_var1 = tk.StringVar()
frequency_var1.set('10')  # 设置输入初始值
frequency_var1.trace("w", update_parameters)
frequency_frame = tk.Frame(root, bg='black')
frequency_frame.grid(row=2, column=0)
frequency_label1 = tk.Label(frequency_frame, text="Wave 1 频率: ", bg='black', fg='red', font=("Helvetica", 25))
frequency_label1.pack(side='left')
frequency_spinbox1 = tk.Spinbox(frequency_frame, from_=0, to=100, textvariable=frequency_var1, width=20,
                                font=("Helvetica", 25),increment=0.1)
frequency_spinbox1.pack(side='left')
# 此代码是无上下按钮的输入框Spinbox，上方是有上下按钮的输入框spinbox

empty_label1 = tk.Label(root, bg='black', height=2)  # 增加2格子的间隔
empty_label1.grid(row=3, column=0)

input_phase_frame1 = tk.Frame(root, bg='black')
input_phase_frame1.grid(row=4, column=0)  # 调整为合适的行号
input_phase_label1 = tk.Label(input_phase_frame1, text="Wave 1 相位: ", bg='black', fg='red', font=("Helvetica", 25))
input_phase_label1.pack(side='left')
input_phase_spinbox1 = tk.Spinbox(input_phase_frame1, from_=-360, to=360, textvariable=input_phase_var1, width=20,
                                  font=("Helvetica", 25),increment=0.1)
input_phase_spinbox1.pack(side='left')

empty_label1 = tk.Label(root, bg='black', height=2)  # 增加2格子的间隔
empty_label1.grid(row=5, column=0)

amplitude_var1 = tk.StringVar()
amplitude_var1.set('10')
amplitude_var1.trace("w", update_parameters)
amplitude_frame = tk.Frame(root, bg='black')
amplitude_frame.grid(row=6, column=0)
amplitude_label1 = tk.Label(amplitude_frame, text="Wave 1 振幅: ", bg='black', fg='red', font=("Helvetica", 25))
amplitude_label1.pack(side='left')
amplitude_spinbox1 = tk.Spinbox(amplitude_frame, from_=0, to=100, textvariable=amplitude_var1, width=20,
                                font=("Helvetica", 25),increment=0.1)
amplitude_spinbox1.pack(side='left')

empty_label1 = tk.Label(root, bg='black', height=2)  # 增加2格子的间隔
empty_label1.grid(row=7, column=0)

frequency_var2 = tk.StringVar()
frequency_var2.set('10')
frequency_frame2 = tk.Frame(root, bg='black')
frequency_frame2.grid(row=8, column=0)
frequency_label2 = tk.Label(frequency_frame2, text="Wave 2 频率: ", bg='black', fg='blue', font=("Helvetica", 25))
frequency_label2.pack(side='left')
frequency_spinbox2 = tk.Spinbox(frequency_frame2, from_=0, to=100, textvariable=frequency_var2, width=20,
                                font=("Helvetica", 25),increment=0.1)
frequency_spinbox2.pack(side='left')

empty_label1 = tk.Label(root, bg='black', height=2)  # 增加2格子的间隔
empty_label1.grid(row=9, column=0)

input_phase_frame2 = tk.Frame(root, bg='black')
input_phase_frame2.grid(row=10, column=0)  # 调整为合适的行号
input_phase_label2 = tk.Label(input_phase_frame2, text="Wave 2 相位: ", bg='black', fg='blue', font=("Helvetica", 25))
input_phase_label2.pack(side='left')
input_phase_spinbox2 = tk.Spinbox(input_phase_frame2, from_=-360, to=360, textvariable=input_phase_var2, width=20,
                                  font=("Helvetica", 25),increment=0.1)
input_phase_spinbox2.pack(side='left')

empty_label1 = tk.Label(root, bg='black', height=2)  # 增加2格子的间隔
empty_label1.grid(row=11, column=0)

amplitude_var2 = tk.StringVar()
amplitude_var2.set('10')
amplitude_var2.trace("w", update_parameters)
amplitude_frame2 = tk.Frame(root, bg='black')
amplitude_frame2.grid(row=12, column=0)
amplitude_label2 = tk.Label(amplitude_frame2, text="Wave 2 振幅: ", bg='black', fg='blue', font=("Helvetica", 25))
amplitude_label2.pack(side='left')
amplitude_spinbox2 = tk.Spinbox(amplitude_frame2, from_=0, to=100, textvariable=amplitude_var2, width=20,
                                font=("Helvetica", 25),increment=0.1)
amplitude_spinbox2.pack(side='left')

empty_label1 = tk.Label(root, bg='black', height=2)  # 增加2格子的间隔
empty_label1.grid(row=13, column=0)

black_frame = tk.Frame(root, bg='black')
black_frame.grid(row=0, column=1, rowspan=14)

fig = plt.figure(2, figsize=(14, 10), facecolor='black')
canvas = FigureCanvasTkAgg(fig, master=black_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.configure(background='black')
canvas_widget.pack()

ani = FuncAnimation(fig, animate, frames=100000, interval=0.01, repeat=True)  # frames 是帧率，interval 是每帧间隔时间

button_frame = tk.Frame(root, bg='black')  # 设置两个按钮之间是黑色的
button_frame.grid(row=14, column=0)

play_button = tk.Button(button_frame, text="播放", command=play_animation,
                        bg="black", fg="white", font=("Helvetica", 20), relief="flat", width=20, height=3)
play_button.pack(side='left', padx=(0, 10))

pause_button = tk.Button(button_frame, text="暂停", command=pause_animation,
                         bg="black", fg="white", font=("Helvetica", 20), relief="flat", width=20, height=3)
pause_button.pack(side='left')
# 新建了一个Frame ，使得两个按钮之间间隔很小
root.mainloop()
