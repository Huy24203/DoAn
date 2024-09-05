import tkinter as tk
from tkinter import ttk
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pickle
df = pd.read_csv('kidney_disease.csv')
df['classification'] = df['classification'].replace(to_replace={'ckd\t':'ckd', 'notckd': 'not ckd'})
df['classification'] = df['classification'].map({'ckd':0, 'not ckd': 1})
df['classification'] = pd.to_numeric(df['classification'], errors = 'coerce')
model=pickle.load(open("Logistic_Regresstion.dat", "rb"))
def predict_and_plot():
    Tuoi = float(Tuoi_entry.get())
    HA = float(HA_entry.get())
    TL = float(TL_entry.get())
    AL = float(AL_entry.get())
    Sugar=float(Sugar_entry.get())
    red_blood_cell=int(red_blood_cell_cb.get())
    pus_cell=int(pus_cell_cb.get())
    pus_cell_clump=int(pus_cell_clump_cb.get())
    vk=int(vk_cb.get())
    bgr=float(blood_glucose_random.get())
    bu=float(blood_urea.get())
    cr=float(creatinine.get())
    na=float(Natri.get())
    ka=float(Kali.get())
    hst=float(HST.get())
    pcv=float(packed_cell_volume.get())
    Trang=float(mt.get())
    Do=float(md.get())
    THA=int(hypertension.get())
    DTD1=int(DTD.get())
    DMV1=int(DMV.get())
    TA1=int(TA.get())
    PN=int(Peda.get())
    TM1=int(TM.get())
    # Dự đoán
    new_data = [[Tuoi, HA, TL, AL, Sugar, red_blood_cell, pus_cell, pus_cell_clump, vk, bgr, bu, cr, na, ka, hst, pcv, Trang, Do, THA, DTD1, DMV1, TA1, PN, TM1]]
    result = model.predict(new_data)
    # Hiển thị kết quả
    if result == 0:
        result_label.config(text="Mắc bệnh thận mãn tính")
    else:
        result_label.config(text="Không mắc bệnh thận")
    
    # Tính tỷ lệ mắc bệnh và không mắc bệnh từ dữ liệu gốc
    num_mắc_bệnh = (df['classification'] == 0).sum()  # Số lượng mẫu mắc bệnh
    num_không_mắc_bệnh = (df['classification'] == 1).sum()  # Số lượng mẫu không mắc bệnh

    # Cập nhật số lượng mẫu mới được dự đoán vào tỷ lệ này
    if result == 0:
        num_mắc_bệnh += 1
    else:
        num_không_mắc_bệnh += 1

    # Tính tổng số mẫu
    total_samples = num_mắc_bệnh + num_không_mắc_bệnh
    
    # Tính tỷ lệ phần trăm
    percent_mắc_bệnh = (num_mắc_bệnh / total_samples) * 100
    percent_không_mắc_bệnh = (num_không_mắc_bệnh / total_samples) * 100

    # Nếu không mắc bệnh, phần trăm mắc bệnh phải là phần còn lại
    if result == 1:
        percent_không_mắc_bệnh = percent_mắc_bệnh
        percent_mắc_bệnh = 100 - percent_không_mắc_bệnh
    

    

    # Vẽ biểu đồ tròn
    labels = ['Mắc bệnh', 'Không mắc bệnh']
    sizes = [percent_mắc_bệnh, percent_không_mắc_bệnh]
    colors = ['#66b3ff', '#ff9999']
    explode = (0.1, 0)

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
           shadow=True, startangle=140)
    ax.set_title('Tỷ lệ người mắc bệnh dựa trên dữ liệu mới')

    # Clear the old plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Embed the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()
    


    
# Tạo giao diện người dùng
window = tk.Tk()
window.title("Ứng dụng dự báo kết quả mắc bệnh thận")
window.minsize(height=600,width=400)
window.resizable(width=True,height=False)



Tuoi_label = tk.Label(window, text="Độ tuổi:").grid(row=1,column=0)
Tuoi_entry = tk.Entry(window,width=20)
Tuoi_entry.grid(row=1,column=1)

# Nhập huyết áp
HA_label = tk.Label(window, text="Huyết áp:").grid(row=2,column=0)
HA_entry = tk.Entry(window,width=20)
HA_entry.grid(row=2,column=1)
# Nhập trọng lượng riêng
TL_label = tk.Label(window, text="Trọng lượng riêng:").grid(row=3,column=0)
TL_entry = tk.Entry(window,width=20)
TL_entry.grid(row=3,column=1)

# Nhập lượng Albumin
AL_label = tk.Label(window, text="Lượng Albumin:").grid(row=4,column=0)
AL_entry = tk.Entry(window,width=20)
AL_entry.grid(row=4,column=1)
# Nhập lượng đường
Sugar_label = tk.Label(window, text="Lượng đường:").grid(row=5,column=0)
Sugar_entry = tk.Entry(window,width=20)
Sugar_entry.grid(row=5,column=1)

# Tế bào máu đỏ
red_blood_cell_label = tk.Label(window, text="Tế bào máu đỏ:").grid(row=6,column=0)
red_blood_cell_cb = ttk.Combobox(window,width=15,values=('0','1'))
red_blood_cell_cb.grid(row=6,column=1)

# Tế bào có mủ
pus_cell_label = tk.Label(window, text="Tế bào mủ như thế nào?").grid(row=7,column=0)
pus_cell_cb = ttk.Combobox(window,width=15,values=('0','1'))
pus_cell_cb.grid(row=7,column=1)

# Khối tế bào mủ
pus_cell_clump_label = tk.Label(window, text="Khối tế bào có mủ không?").grid(row=8,column=0)
pus_cell_clump_cb = ttk.Combobox(window,width=15,values=('0','1'))
pus_cell_clump_cb.grid(row=8,column=1)
#Vi khuẩn
vk_label = tk.Label(window, text="Có vi khuẩn không?").grid(row=9,column=0)
vk_cb = ttk.Combobox(window,width=15,values=('0','1'))
vk_cb.grid(row=9,column=1)
#blood_glucose_random
blood_glucose_random_label = tk.Label(window, text="Lượng glucose ngẫu nhiên trong máu:").grid(row=10,column=0)
blood_glucose_random = tk.Entry(window,width=20)
blood_glucose_random.grid(row=10,column=1)
#blood_urea
blood_urea_label = tk.Label(window, text="Lượng urea trong máu:").grid(row=11,column=0)
blood_urea = tk.Entry(window,width=20)
blood_urea.grid(row=11,column=1)
#Huyết thanh
creatinine_label = tk.Label(window, text="Huyết thanh creatinine:").grid(row=12,column=0)
creatinine = tk.Entry(window,width=20)
creatinine.grid(row=12,column=1)
#Natri
Natri_label = tk.Label(window, text="Lượng Natri:").grid(row=13,column=0)
Natri = tk.Entry(window,width=20)
Natri.grid(row=13,column=1)
#Kali
Kali_label = tk.Label(window, text="Lượng Kali:").grid(row=14,column=0)
Kali = tk.Entry(window,width=20)
Kali.grid(row=14,column=1)

#Huyết sắc tố
HST_label = tk.Label(window, text="Huyết sắc tố:").grid(row=15,column=0)
HST = tk.Entry(window,width=20)
HST.grid(row=15,column=1)
#packed_cell_volume
packed_cell_volume_label = tk.Label(window, text="Packed_cell_volume:").grid(row=16,column=0)
packed_cell_volume = tk.Entry(window,width=20)
packed_cell_volume.grid(row=16,column=1)
#Số lượng tế bào máu trắng
mt_label = tk.Label(window, text="Số lượng tế bào máu trắng: ").grid(row=17,column=0)
mt = tk.Entry(window,width=20)
mt.grid(row=17,column=1)
#Số lượng tế bào máu đỏ
md_label = tk.Label(window, text="Số lượng tế bào máu đỏ: ").grid(row=18,column=0)
md = tk.Entry(window,width=20)
md.grid(row=18,column=1)

hypertension_label = tk.Label(window, text="Có bị tăng huyết áp không? ").grid(row=19,column=0)
hypertension = ttk.Combobox(window,width=15,values=('0','1'))
hypertension.grid(row=19,column=1)
DTD_label = tk.Label(window, text="Có bị đái tháo đường không? ").grid(row=20,column=0)
DTD = ttk.Combobox(window,width=15,values=('0','1'))
DTD.grid(row=20,column=1)
DMV_label = tk.Label(window, text="Có bị động mạch vành không? ").grid(row=21,column=0)
DMV = ttk.Combobox(window,width=15,values=('0','1'))
DMV.grid(row=21,column=1)
TA_label = tk.Label(window, text="Có bị thèm ăn không? ").grid(row=22,column=0)
TA = ttk.Combobox(window,width=15,values=('0','1'))
TA.grid(row=22,column=1)
Peda_label = tk.Label(window, text="Có bị phù nề Peda không? ").grid(row=23,column=0)
Peda = ttk.Combobox(window,width=15,values=('0','1'))
Peda.grid(row=23,column=1)
TM_label = tk.Label(window, text="Có bị thiếu máu không? ").grid(row=24,column=0)
TM = ttk.Combobox(window,width=15,values=('0','1'))
TM.grid(row=24,column=1)


# Button để dự đoán và vẽ biểu đồ
predict_button = tk.Button(window, text="Dự đoán", command=predict_and_plot).grid(row=25)

# Label để hiển thị kết quả
result_label = tk.Label(window, text="")
result_label.grid(row=26)

# Frame chứa biểu đồ
plot_frame = tk.Frame(window)
plot_frame.grid(row=1, column=2, rowspan=26)

window.mainloop()


