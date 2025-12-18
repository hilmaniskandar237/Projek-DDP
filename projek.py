import streamlit as st
from datetime import datetime

if "bookings" not in st.session_state:
    st.session_state.bookings = []


#menetukan tarif per jam
def tarif_per_jam(jenis):
    if jenis == "Motor":
        return 1000
    elif jenis == "Mobil":
        return 2000
    else:
        return 500

#Menentuan tarif harian
def tarif_harian(jenis):
    if jenis == "Motor":
        return 10000
    elif jenis == "Mobil":
        return 20000
    else:
        return 5000

#Menghitung biaya total
def hitung_biaya(jenis, durasi):
    per_jam = tarif_per_jam(jenis)
    if durasi >= 24:
        hari = durasi // 24
        sisa_jam = durasi % 24
        return (hari * tarif_harian(jenis)) + (sisa_jam * per_jam)
    else:
        return durasi * per_jam


st.sidebar.title("Sistem Parkir")
pilihan = st.sidebar.selectbox(
    "Pilih Halaman:",
    ["beranda", "booking tempat parkir", "aktivasi tempat parkir", "Pembayaran", "dashboard penghasilan"]
)


if pilihan == "beranda":
    st.title("Selamat Datang di Aplikasi Absen Tempat Parkir Online")
    st.write("Aplikasi Ini memudahkan kita untuk parkir kendaraan dengan mudah dan efisien.")
    st.write("fitur-fitur yang tersedia:")
    st.write("- Booking Tempat Parkir")
    st.write("- Aktivasi Tempat Parkir")
    st.write("- Pembayaran")
    st.write("- Dashboard Penghasilan")

    data = {
        "Kendaraan": ["Motor", "Mobil", "Sepeda"],
        "harga parkir per jam (Rp)": [1000, 2000, 500],
    }
    st.table(data)

    st.write("Jika durasi parkir mencapai atau melebihi 24 jam, maka biaya dihitung harian:")
    st.write("- Motor: Rp 10.000")
    st.write("- Mobil: Rp 20.000")
    st.write("- Sepeda: Rp 5.000")

    st.header("Kelompok Anak Buah Pangeran")
    st.text("1. Endih Saputra (0110125065)")
    st.text("2. Hilman Nabil Iskandar (0110125059)")
    st.text("3. Raisha Kamila Zahra (0110125060)")
    st.text("4. Agnia Sunardi (0110125061)")


elif pilihan == "booking tempat parkir":
    st.title("Booking Tempat Parkir")

    with st.form("form_booking"):
        nama = st.text_input("Nama Lengkap")
        jenis = st.selectbox("Jenis Kendaraan", ["Mobil", "Motor", "Sepeda"])
        tempat_parkir = st.selectbox("Pilih Tempat Parkir", [f"Slot {i}" for i in range(1, 21)])
        waktu_masuk = st.time_input("Waktu Masuk")

        if st.form_submit_button("Booking"):
            if any(
                b["Tempat Parkir"] == tempat_parkir and b["Status"] == "Booked"
                for b in st.session_state.bookings
            ):
                st.error("Tempat parkir sudah dibooking.")
            elif nama == "":
                st.error("Nama tidak boleh kosong.")
                
            else:
                data = {
                    "Nama": nama,
                    "Jenis": jenis,
                    "Tempat Parkir": tempat_parkir,
                    "Waktu Masuk": str(waktu_masuk),
                    "Durasi": None,
                    "Tarif per Jam": None,
                    "Biaya Total": None,
                    "Status": "Booked"
                }
                st.session_state.bookings.append(data)
                st.success(f"{tempat_parkir} berhasil dibooking untuk {nama}")


elif pilihan == "aktivasi tempat parkir":
    st.title("Aktivasi Tempat Parkir")

    booked = [a for a in st.session_state.bookings if a["Status"] == "Booked"]

    if not booked:
        st.warning("Belum ada tempat parkir yang dibooking")
    else:
        with st.form("form_aktivasi"):
            tempat_parkir = st.selectbox(
                "Pilih Tempat Parkir",
                [a["Tempat Parkir"] for a in booked]
            )
            durasi = st.number_input("Durasi Parkir (jam)", min_value=1, max_value=168)

            if st.form_submit_button("Aktivasi"):
                for a in st.session_state.bookings:
                    if a["Tempat Parkir"] == tempat_parkir:
                        a["Durasi"] = durasi
                        a["Tarif per Jam"] = tarif_per_jam(a["Jenis"])
                        a["Biaya Total"] = hitung_biaya(a["Jenis"], durasi)
                        a["Status"] = "Aktivated"
                        st.success("Tempat parkir berhasil diaktivasi")
                        break


elif pilihan == "Pembayaran":
    st.title("Pembayaran Parkir")
    # Menampilkan tempat parkir yang sudah diaktivasi
    aktivated = [a for a in st.session_state.bookings if a["Status"] == "Aktivated"]

    # Jika tidak ada yang diaktivasi
    if not aktivated:
        st.warning("Belum ada parkir yang diaktivasi")
    else:
        with st.form("form_pembayaran"):
            tempat_parkir = st.selectbox(
                "Pilih Tempat Parkir",
                [a["Tempat Parkir"] for a in aktivated]
            )
            # untuk Bayar Parkir
            if st.form_submit_button("Bayar"):
                for a in st.session_state.bookings:
                    if a["Tempat Parkir"] == tempat_parkir:
                        a["Status"] = "Paid"
                        st.success(f"Pembayaran Rp {a['Biaya Total']} berhasil")
                        break


elif pilihan == "dashboard penghasilan":
    st.title("Dashboard Penghasilan")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if "login" not in st.session_state:
        st.session_state.login = False

    if st.button("Login"):
        st.session_state.login = (user == "admin" and password == "admin123")

    if st.session_state.login:
        paid = [a for a in st.session_state.bookings if a["Status"] == "Paid"]
        total = sum(a["Biaya Total"] for a in paid)

        st.metric("Total Penghasilan", f"Rp {total}")
        st.table(paid)
    else:
        st.warning("Login sebagai admin")

