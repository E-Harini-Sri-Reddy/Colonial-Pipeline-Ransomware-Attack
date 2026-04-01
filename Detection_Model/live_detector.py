import os
import psutil
import pandas as pd
import numpy as np
import joblib
import time
from tensorflow.keras.models import load_model
from rich.console import Console
from rich.table import Table
from rich.live import Live

# Suppress TF warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class LiveProcessGuard:
    def __init__(self):
        # Load the optimized model and preprocessing artifacts
        self.model = load_model("models/ransomware_model.keras")
        self.scaler = joblib.load("models/scaler.pkl")
        self.encoder = joblib.load("models/category_encoder.pkl")
        self.features = joblib.load("models/feature_cols.pkl")
        
        # Whitelist for known system processes
        self.whitelist = [
            "System Idle Process", "System", "Registry", "smss.exe", "csrss.exe", 
            "wininit.exe", "services.exe", "lsass.exe", "svchost.exe", "fontdrvhost.exe", 
            "dwm.exe", "explorer.exe", "Code.exe", "Discord.exe", "chrome.exe", 
            "msedge.exe", "audiodg.exe", "WUDFHost.exe", "LsaIso.exe", "SearchHost.exe"
        ]

    def get_prediction(self, proc_info):
        if proc_info['name'] in self.whitelist:
            return "Safe (System)", 1.0

        try:
            metrics = {col: 0 for col in self.features}
            metrics['pslist.nthreads'] = proc_info.get('num_threads', 0)
            metrics['handles.nhandles'] = proc_info.get('num_handles', 0)
            
            df_in = pd.DataFrame([metrics]).reindex(columns=self.features, fill_value=0)
            scaled = self.scaler.transform(df_in)
            
            probs = self.model.predict(scaled, verbose=0)[0]
            idx = np.argmax(probs)
            label = self.encoder.classes_[idx]
            confidence = probs[idx]

            # Heuristic override for noise reduction
            if label != "Benign" and (proc_info.get('num_handles') or 0) < 150:
                return "Benign (Inert)", 0.98

            return label, confidence
        except:
            return "Unknown", 0.0

    def run_stepped_scan(self):
        console = Console()
        
        # Original table setup
        table = Table(title="🛡️ Shield AI: Live Memory Guard", header_style="bold cyan")
        table.add_column("PID", justify="right", style="dim", width=10)
        table.add_column("Process Name", style="white", width=30)
        table.add_column("Threat Status", justify="center", width=20)
        table.add_column("Confidence", justify="right", width=15)

        console.print("[bold yellow]Starting live scan... Press Ctrl+C to stop.[/bold yellow]")

        try:
            # CRITICAL FIX: vertical_overflow="visible" prevents the "..." truncation
            with Live(table, console=console, refresh_per_second=4, vertical_overflow="visible"):
                all_procs = list(psutil.process_iter(['pid', 'name', 'num_threads', 'num_handles']))
                
                for p in all_procs:
                    try:
                        info = p.info
                        status, conf = self.get_prediction(info)
                        
                        # --- UPDATED COLOR LOGIC ---
                        # Explicit Red for any Malware/Spyware/Trojan/Ransomware
                        if any(m in status for m in ["Spyware", "Ransomware", "Trojan", "Malware"]):
                            color = "red"
                        elif "Safe" in status:
                            color = "blue"
                        else:
                            color = "green"

                        table.add_row(
                            str(info['pid']), 
                            info['name'] or "N/A", 
                            f"[{color}]{status}[/{color}]", 
                            f"{conf*100:.1f}%"
                        )
                        
                        # 1-second interval
                        time.sleep(1) 

                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
            
            console.print("\n[bold green]Scan cycle complete.[/bold green]")

        except KeyboardInterrupt:
            console.print("\n[bold red]Scan interrupted by user. Exiting...[/bold red]")

if __name__ == "__main__":
    guard = LiveProcessGuard()
    guard.run_stepped_scan()