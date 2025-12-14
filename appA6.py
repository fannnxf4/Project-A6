import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io

# Konfigurasi halaman
st.set_page_config(page_title="Rose Diagram Generator", page_icon="🌹", layout="wide")
st.title("🌹 Rose Diagram Generator")
st.markdown("**Input data strike dan dip (minimal 25 data masing-masing) untuk menghasilkan Rose Diagram**")

# Sidebar
st.sidebar.header("📊 Input Data")

# Nama diagram
diagram_name = st.sidebar.text_input("Masukkan nama diagram (opsional):", value="Rose Diagram")

# Ukuran bin
bin_size = st.sidebar.number_input(
    "Nilai Batang Diagram(derajat)",
    min_value=1, max_value=90, value=10, step=1,
    help="Lebar tiap batang pada diagram dalam derajat"
)

# Pilihan colormap
colormap_choice = st.sidebar.selectbox(
    "Pilih Color Map",
    options=['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'coolwarm', 'turbo', 'green_red', 'red_green'],
    index=0
)

# Upload CSV
uploaded_file = st.sidebar.file_uploader("📂 Upload CSV (format: Strike/Dip dalam satu kolom)", type="csv", help="File CSV harus memiliki kolom 'Strike' dan 'Dip'")

# Input Strike dan Dip manual
strike_input = st.sidebar.text_area("Masukkan nilai strike (pisahkan dengan koma atau baris baru):", height=150)
dip_input = st.sidebar.text_area("Masukkan nilai dip (pisahkan dengan koma atau baris baru):", height=150)

# Tombol generate
generate_button = st.sidebar.button("🚀 Generate Diagram", type="primary")

# Fungsi parse input
def parse_input(text):
    if not text.strip():
        return []
    cleaned = text.replace('\n', ',').replace(' ', '')
    return [float(x) for x in cleaned.split(',') if x.strip()]

# Fungsi generate rose diagram
def generate_rose_diagram(strikes, dips, diagram_name, bin_deg, cmap_name):
    strikes = np.array(strikes) % 360
    dips = np.array(dips)
    
    az = strikes % 180
    dips_folded = dips
    
    az_full = np.concatenate([az, az + 180])
    dips_full = np.concatenate([dips_folded, dips_folded])
    
    bins = np.arange(0, 360 + bin_deg, bin_deg)
    bin_centers = (bins[:-1] + bins[1:]) / 2.0
    theta = np.deg2rad(bin_centers)
    width = np.deg2rad(bin_deg)
    
    counts = np.zeros(len(bin_centers))
    dip_means = np.zeros(len(bin_centers))
    
    for i in range(len(bin_centers)):
        idx = (az_full >= bins[i]) & (az_full < bins[i+1])
        counts[i] = np.sum(idx)
        dip_means[i] = np.mean(dips_full[idx]) if counts[i] > 0 else 0
    
    dip_max = dip_means.max()
    dip_norm = dip_means / dip_max if dip_max > 0 else dip_means
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, polar=True)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    
    # Colormap custom
    if cmap_name == 'green_red':
        cmap = mcolors.LinearSegmentedColormap.from_list("green_red", ["green", "yellow", "red"])
    elif cmap_name == 'red_green':
        cmap = mcolors.LinearSegmentedColormap.from_list("red_green", ["red", "yellow", "green"])
    else:
        cmap = plt.cm.get_cmap(cmap_name)
    
    ax.bar(theta, counts, width=width, bottom=0, edgecolor='k', color=cmap(dip_norm))
    
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=dip_means.min(), vmax=dip_means.max()))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, pad=0.1)
    cbar.set_label('Average Dip (°)', fontsize=12)
    
    ax.set_title(f'{diagram_name} (Bin: {bin_deg}°)', fontsize=16, pad=20)
    
    return fig

# Main content
if generate_button:
    # Jika CSV diupload, baca data dari CSV
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            if 'Strike/Dip' not in df.columns:
                st.error("❌ CSV harus memiliki kolom 'Strike/Dip'")
                strikes, dips = [], []
            else:
                split_sd = df['Strike/Dip'].astype(str).str.split('/', expand=True)

                if split_sd.shape[1] != 2:
                    st.error("❌ Format harus Strike/Dip (contoh: 213/45)")
                    strikes, dips = [], []
                else:
                    df['Strike'] = pd.to_numeric(split_sd[0], errors='coerce')
                    df['Dip'] = pd.to_numeric(split_sd[1], errors='coerce')

                    df_complete = df.dropna(subset=['Strike', 'Dip'])

                    strikes = df_complete['Strike'].tolist()
                    dips = df_complete['Dip'].tolist()
        except Exception as e:
            st.error(f"❌ Gagal membaca CSV: {e}")
            strikes, dips = [], []
    else:
        strikes = parse_input(strike_input)
        dips = parse_input(dip_input)
    
    errors = []
    if len(strikes) == 0:
        errors.append("❌ Data strike tidak boleh kosong")
    elif len(strikes) < 25:
        errors.append(f"❌ Data strike minimal 25, saat ini hanya {len(strikes)} data")
    
    if len(dips) == 0:
        errors.append("❌ Data dip tidak boleh kosong")
    elif len(dips) < 25:
        errors.append(f"❌ Data dip minimal 25, saat ini hanya {len(dips)} data")
    
    if len(strikes) != len(dips):
        errors.append(f"❌ Jumlah data strike ({len(strikes)}) dan dip ({len(dips)}) harus sama")
    
    if errors:
        for error in errors:
            st.error(error)
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Jumlah Data Strike", len(strikes))
        col2.metric("Jumlah Data Dip", len(dips))
        col3.metric("Status", "✅ Valid")
        
        with st.spinner("Generating diagram..."):
            fig = generate_rose_diagram(strikes, dips, diagram_name, bin_size, colormap_choice)
            st.pyplot(fig)
            
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=300)
            st.download_button(
                label="📥 Download Diagram PNG",
                data=buf.getvalue(),
                file_name=f"{diagram_name.replace(' ', '_')}.png",
                mime="image/png"
            )
            plt.close(fig)
        
        st.success("✅ Diagram berhasil dihasilkan!")
        
        with st.expander("📋 Preview Data"):
            df_preview = pd.DataFrame({'Strike': strikes, 'Dip': dips})
            st.dataframe(df_preview, use_container_width=True)
            csv = df_preview.to_csv(index=False, sep=';')
            st.download_button(
                label="📥 Download Data sebagai CSV",
                data=csv,
                file_name=f"{diagram_name.replace(' ', '_')}_data.csv",
                mime="text/csv"
            )

else:
    st.info("👈 **Silakan masukkan data di sidebar kiri atau upload CSV**")
    st.markdown("""
    ### 📝 Cara Penggunaan:
    1. Masukkan data **strike** dan **dip** manual atau **upload CSV** (dalam 1 kolom: Strike/Dip)
    2. Masukkan **nama diagram** (opsional)
    3. Atur **ukuran bin** sesuai kebutuhan
    4. Pilih **color map**
    5. Input data secara manual atau melalui file CSV
    6. Klik tombol **Generate Diagram**
    7. Diagram akan muncul di halaman ini
    
    ### 💡 Tips:
    - Data dapat dipisahkan dengan **koma** atau **baris baru**
    - Contoh format: `185, 170, 173, 170` atau `185\\n170\\n173\\n170`
    - Nilai strike biasanya antara 0-360 derajat
    - Nilai dip biasanya antara 0-90 derajat

    """)
