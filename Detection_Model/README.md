# 🛡️ AI-Powered Ransomware Detection System

An advanced **Machine Learning + Deep Learning cybersecurity project** designed to detect ransomware and other malware using **memory forensics data**.

---

## 🚀 Overview

This system provides:

* 📊 Interactive analytics dashboard
* ⚡ Real-time process monitoring
* 🧠 Deep learning-based classification
* 📁 Batch prediction utilities

---

## ✨ Features

### 🔍 1. Memory Threat Analytics Dashboard (`app.py`)

* Built with **Streamlit**
* Upload memory dump CSV files
* Visual insights:

  * 📊 Threat distribution (Pie chart)
  * 📈 Detection counts (Bar chart)
  * 🎯 Confidence metrics
* 📂 Expandable raw logs view

---

### 🛡️ 2. Live Process Monitoring (`live_detector.py`)

* Real-time system process scanning
* Uses **psutil** for process data
* Detects:

  * Ransomware
  * Spyware
  * Trojan
  * Benign processes
* Smart filtering:

  * ✅ System process whitelist
  * 🔇 Heuristic noise reduction
* 🎨 Rich terminal UI using **Rich**

---

### 📈 3. Batch Prediction Tool (`predict.py`)

* Runs inference on dataset samples
* Displays:

  * ✅ Actual vs Predicted class
  * 📊 Confidence scores
  * 📉 Category-wise probabilities

---

### 🧠 4. Model Training Pipeline (`ransomware_nn.py`)

#### 🔧 Preprocessing

* Label Encoding
* Feature Scaling (**StandardScaler**)

#### 🧠 Neural Network

* Dense layers
* Batch Normalization
* Dropout regularization

#### 📦 Outputs

* Trained model (`.keras`)
* Scaler (`.pkl`)
* Encoder (`.pkl`)
* Feature columns (`.pkl`)

---

## 🗂️ Project Structure

```
project-root/
│
├── app.py
├── live_detector.py
├── predict.py
├── ransomware_nn.py
│
├── models/
│   ├── ransomware_model.keras
│   ├── scaler.pkl
│   ├── category_encoder.pkl
│   └── feature_cols.pkl
│
├── datasets/
│   └── Obfuscated-MalMem2022.csv
│
├── plots/
│   ├── accuracy_loss.png
│   ├── confusion_matrix.png
│   └── roc_auc.png
│
└── README.md
```

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

### 🔧 Core Libraries

* streamlit
* pandas
* numpy
* scikit-learn
* tensorflow
* plotly
* psutil
* rich
* matplotlib
* seaborn
* joblib

---

## 🧪 Usage

### 🧠 Train the Model

```bash
python ransomware_nn.py
```

---

### ▶️ Run Dashboard

```bash
streamlit run app.py
```

---

### 🖥️ Run Live Detection

```bash
python live_detector.py
```

---

### 📊 Run Batch Prediction

```bash
python predict.py
```

---

## 📊 Dataset

**Obfuscated-MalMem2022 Dataset**

* Memory-based malware detection dataset
* Categories:

  * Benign
  * Ransomware
  * Spyware
  * Trojan
  * Malware

---

## 🧠 Model Architecture

```
Input Layer
   ↓
Dense (256) + ReLU
   ↓
Batch Normalization
   ↓
Dropout (0.3)
   ↓
Dense (128) + ReLU
   ↓
Softmax Output Layer
```

### ⚙️ Training Configuration

* **Loss Function:** Sparse Categorical Crossentropy
* **Optimizer:** Adam

---

## 📈 Outputs

After training:

* 📉 Accuracy & Loss Curves
* 🔢 Confusion Matrix
* 📊 ROC-AUC Curve

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**.
It is **not a replacement** for enterprise-grade security or antivirus solutions.

---

## 💡 Future Improvements

* 🔄 Real-time memory dump integration
* ☁️ Cloud-based deployment
* 🧠 Transformer-based architectures
* 📡 SIEM integration
* 🛠️ Automated threat response

---

## ⭐ Acknowledgements

* Open-source cybersecurity datasets
* TensorFlow & Scikit-learn communities
* Streamlit for rapid UI development

---

# 📊 Feature Description (Dataset Columns)

This project uses **memory forensics features** extracted from system snapshots.
Each column represents behavioral or structural system properties.

---

## 🧾 Labels

* **Category** → Multi-class classification
* **Class** → Binary classification (Benign vs Malware)

---

## 🧠 Process Features (`pslist.*`)

* `pslist.nproc` → Total running processes
* `pslist.nppid` → Unique parent process IDs
* `pslist.avg_threads` → Avg threads per process
* `pslist.nprocs64bit` → 64-bit processes
* `pslist.avg_handlers` → Avg handles per process

👉 Detects abnormal process/thread behavior

---

## 📚 DLL Features (`dlllist.*`)

* `dlllist.ndlls`
* `dlllist.avg_dlls_per_proc`

👉 Detects suspicious DLL injections

---

## 🧩 Handle Features (`handles.*`)

Includes:

* File, registry, thread, mutex, timer, and more

👉 Ransomware heavily interacts with:

* Files
* Registry
* Synchronization objects

---

## 🧬 Loader Module Features (`ldrmodules.*`)

Detect anomalies in module loading:

* Not in load/init/memory lists
* Average inconsistencies

👉 Strong malware indicators

---

## 💉 Injection Detection (`malfind.*`)

* Memory injections
* Suspicious regions
* Executable memory flags

👉 Critical for advanced malware detection

---

## 👁️ Cross-View Detection (`psxview.*`)

Detect hidden processes via multiple OS views:

* Missing from system structures
* False-positive averages

👉 Helps identify rootkits & stealth malware

---

## 🧱 Modules & Services

### Kernel Modules

* `modules.nmodules`

### Service Scan (`svcscan.*`)

* Services, drivers, active processes

👉 Malware often installs malicious services

---

## 🔁 Callback Features (`callbacks.*`)

* Callback routines
* Anonymous/generic callbacks

👉 Used for persistence and interception

---

## 🧠 Why These Features Matter

These signals help detect:

* 🔐 Ransomware (file & memory abuse)
* 🕵️ Spyware (stealth + monitoring)
* 🧬 Trojans (persistence mechanisms)
* 🛑 Rootkits (hiding techniques)

The model learns patterns across these features to accurately classify threats.