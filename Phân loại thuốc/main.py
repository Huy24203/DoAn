import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

# Load dữ liệu và huấn luyện mô hình
df = pd.read_csv('D:\CNTT\Thuc_hanh\TH TTNT\DoAnCK_1\drug200.csv')

#Xử lý dữ liệu thành kiểu số
s = {'F': 0, 'M': 1}
bp_mapping = {'HIGH': 0, 'NORMAL': 1, 'LOW': 2}
ch = {'HIGH': 0, 'NORMAL': 1}
dr = {'drugA': 0, 'drugB': 1, 'drugC': 2, 'drugX': 3, 'drugY': 4}
features = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']

# #Xử lý dữ liệu trong tập dữ liệu
# df['Sex'] = df['Sex'].map(s)
# df['BP'] = df['BP'].map(bp_mapping)
# df['Cholesterol'] = df['Cholesterol'].map(ch)
# df['Drug'] = df['Drug'].map(dr)
# features = ['Age', 'Sex', 'BP', 'Cholesterol', 'Na_to_K']
# X = df[features]
# y = df['Drug']

# #Chia mô hình thành tập huấn luyện và kiểm tra
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
# model = DecisionTreeClassifier()
# model.fit(X_train, y_train)

# # # Lưu mô hình
# joblib.dump(model, 'decision_tree_model.joblib')

# #Đọc mô hình từ model có sẵn
model = joblib.load('decision_tree_model.joblib')

# Tạo ứng dụng tkinter
app = tk.Tk()
app.title("Dự đoán thuốc")

# Tạo và thiết lập các trường nhập
age_label = ttk.Label(app, text="Tuổi:")
age_label.grid(row=0, column=0, padx=10, pady=10)
age_entry = ttk.Entry(app)
age_entry.grid(row=0, column=1, padx=10, pady=10)

sex_label = ttk.Label(app, text="Giới tính:")
sex_label.grid(row=1, column=0, padx=10, pady=10)
sex_var = tk.StringVar()
sex_combobox = ttk.Combobox(app, textvariable=sex_var, values=["F", "M"])
sex_combobox.grid(row=1, column=1, padx=10, pady=10)

bp_label = ttk.Label(app, text="Huyết áp:")
bp_label.grid(row=2, column=0, padx=10, pady=10)
bp_var = tk.StringVar()
bp_combobox = ttk.Combobox(app, textvariable=bp_var, values=["HIGH", "NORMAL", "LOW"])
bp_combobox.grid(row=2, column=1, padx=10, pady=10)

cholesterol_label = ttk.Label(app, text="Cholesterol:")
cholesterol_label.grid(row=3, column=0, padx=10, pady=10)
cholesterol_var = tk.StringVar()
cholesterol_combobox = ttk.Combobox(app, textvariable=cholesterol_var, values=["HIGH", "NORMAL"])
cholesterol_combobox.grid(row=3, column=1, padx=10, pady=10)

na_to_k_label = ttk.Label(app, text="Na_to_K:")
na_to_k_label.grid(row=4, column=0, padx=10, pady=10)
na_to_k_entry = ttk.Entry(app)
na_to_k_entry.grid(row=4, column=1, padx=10, pady=10)

# Tạo nút để thực hiện dự đoán
def predict_disease():
    # Lấy dữ liệu từ trường nhập
    age = float(age_entry.get())
    sex = sex_var.get()
    bp = bp_var.get()
    cholesterol = cholesterol_var.get()
    na_to_k = float(na_to_k_entry.get())

    # Chuyển đổi giá trị chuỗi sang số
    sex = s[sex]
    bp = bp_mapping[bp]
    cholesterol = ch[cholesterol]

    # Tạo DataFrame với dữ liệu mới
    new_data = pd.DataFrame({'Age': [age], 'Sex': [sex], 'BP': [bp], 'Cholesterol': [cholesterol], 'Na_to_K': [na_to_k]})

    # Dự đoán bệnh sử dụng mô hình đã huấn luyện
    prediction = model.predict(new_data)

    # Ánh xạ kết quả dự đoán với tên drug
    drug_mapping_reverse = {0: 'drugA', 1: 'drugB', 2: 'drugC', 3: 'drugX', 4: 'drugY'}
    predicted_drug = drug_mapping_reverse[prediction[0]]

    # Hiển thị kết quả
    result_label.config(text=f"Kết quả dự đoán: {predicted_drug}")

predict_button = ttk.Button(app, text="Dự đoán", command=predict_disease)
predict_button.grid(row=5, column=0, columnspan=2, pady=20)

# Label để hiển thị kết quả
result_label = ttk.Label(app, text="")
result_label.grid(row=6, column=0, columnspan=2)

# Tỷ lệ dự đoán chính xác
predict_rate = ttk.Label(app, text="")
predict_rate.grid(row=6, column=0, columnspan=2, pady=10)

# Chọn file
file_label = ttk.Label(app, text="Chọn file dữ liệu:")
file_label.grid(row=7, column=0, padx=10, pady=10)

#Input file
file_var = tk.StringVar()
file_entry = ttk.Entry(app, textvariable=file_var, state="readonly")
file_entry.grid(row=7, column=1, padx=10, pady=10)

#Check file
def browse_file():
    file_path = tk.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    file_var.set(file_path)

#Browse file
browse_button = ttk.Button(app, text="Chọn file", command=browse_file)
browse_button.grid(row=7, column=2, pady=10)

#Text widget
data_text = tk.Text(app, height=10, width=60)
data_text.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

#Dự đoán trên file
def predict_from_file():
    file_path = file_var.get()
    if not file_path:
        result_label.config(text="Hãy chọn một file trước.")
        return

    try:
        # Load dữ liệu từ file
        new_data = pd.read_csv(file_path)

        # Chuyển đổi với tập kiểm tra
        sn = {'F': 0, 'M': 1}
        new_data['Sex'] = new_data['Sex'].map(sn)

        bpn = {'HIGH': 0, 'NORMAL': 1, 'LOW': 2}
        new_data['BP'] = new_data['BP'].map(bpn)

        chn = {'HIGH': 0, 'NORMAL': 1}
        new_data['Cholesterol'] = new_data['Cholesterol'].map(chn)

        drn = {'drugA': 0, 'drugB': 1, 'drugC': 2, 'drugX': 3, 'drugY': 4}
        new_data['Drug'] = new_data['Drug'].map(drn)

        X_new = new_data[features]

        # Dự đoán bệnh sử dụng mô hình đã huấn luyện
        predictions = model.predict(X_new)

        # Tính toán tỷ lệ dự đoán chính xác
        accuracy = accuracy_score(y_true=new_data['Drug'], y_pred=predictions)

        # Hiển thị tỷ lệ dự đoán chính xác
        predict_rate.config(text=f"Tỷ lệ dự đoán chính xác: {accuracy * 100:.2f}%")

        # Ánh xạ kết quả dự đoán với tên drug
        drug_mapping_reverse = {0: 'drugA', 1: 'drugB', 2: 'drugC', 3: 'drugX', 4: 'drugY'}
        predicted_drugs = [drug_mapping_reverse[p] for p in predictions]

        # Thêm một cột mới vào DataFrame để chứa kết quả dự đoán
        new_data['Predicted_Drug'] = predicted_drugs

        # Hiển thị dữ liệu đầy đủ
        data_text.delete(1.0, tk.END)  # Xóa nội dung cũ
        data_text.insert(tk.END, "Dữ liệu đầy đủ từ file:\n")
        data_text.insert(tk.END, new_data.to_string(index=False))

    except Exception as e:
        result_label.config(text=f"Lỗi: {str(e)}")


predict_file_button = ttk.Button(app, text="Dự đoán từ file", command=predict_from_file)
predict_file_button.grid(row=8, column=0, columnspan=2, pady=10)


# Chạy ứng dụng
app.mainloop()
