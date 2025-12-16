import streamlit as st
from datetime import datetime

def get_harga_per_jam(jenis):
    if jenis == "Motor":
        return 1000
    elif jenis == "Mobil":
        return 2000
    else:
        return 500

def get_harga_harian(jenis):
    if jenis == "Motor":
        return 10000
    elif jenis == "Mobil":
        return 20000
    else:
        return 5000

def hitung_biaya(durasi, jenis):
    harga_jam = get_harga_per_jam(jenis)
    harga_harian = get_harga_harian(jenis)

    if durasi >= 24:
        hari = durasi // 24
        sisa_jam = durasi % 24
        return (hari * harga_harian) + (sisa_jam * harga_jam)
    else:
        return durasi * harga_jam

def cek_slot_booked(bookings, tempat_parkir):
    return any(
        a["Tempat Parkir"] == tempat_parkir and a["Status"] == "Booked"
        for a in bookings
    )

st.sidebar.title("Sistem Parkir")
pilihan = st.sidebar.selectbox(
    "Pilih Halaman:",
    ["beranda", "booking tempat parkir", "aktivasi tempat parkir", "Pembayaran", "dashboard penghasilan"]
)

if "bookings" not in st.session_state:
    st.session_state.bookings = []

if pilihan == "beranda":
    st.title("Selamat Datang di Sistem Parkir Kami")
    st.write("Aplikasi Ini memudahkan kita untuk parkir kendaraan dengan mudah dan efisien.")

    data = {
        "Kendaraan": ["Motor", "Mobil", "Sepeda"],
        "Harga per Jam (Rp)": [1000, 2000, 500],
    }

    st.table(data)

    st.write("Jika durasi parkir Lebih Dari 24 jam, maka tarif harian berlaku.")
    st.write("- Motor: Rp 10.000")
    st.write("- Mobil: Rp 20.000")
    st.write("- Sepeda: Rp 5.000")

    st.header("Kelompok Anak Buah pangeran")
    st.text("1.Endih Saputra (0110125065)")
    st.text("2.Hilman Nabil Iskandar (0110125059)")
    st.text("3.RAISHA KAMILA ZAHRA (0110125060)")
    st.text("4.AGNIA SUNARDI (0110125061)")

elif pilihan == "booking tempat parkir":
    st.title("Booking Tempat Parkir")

    with st.form("form_booking"):
        nama = st.text_input("Nama Lengkap")
        jenis = st.selectbox("Jenis Kendaraan", ["Mobil", "Motor", "Sepeda"])
        tempat_parkir = st.selectbox("Pilih Tempat Parkir", [f"Slot {i}" for i in range(1, 21)])

        if st.form_submit_button("Booking"):
            if cek_slot_booked(st.session_state.bookings, tempat_parkir):
                st.error("Slot sudah dibooking!")
            elif nama == "":
                st.error("Nama harus diisi!")
            else:
                st.session_state.bookings.append({
                    "Nama": nama,
                    "Jenis": jenis,
                    "Tempat Parkir": tempat_parkir,
                    "Waktu Masuk": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Durasi": None,
                    "Tarif per Jam": None,
                    "Biaya Total": None,
                    "Status": "Booked"
                })
                st.success("Booking berhasil!")
                st.rerun()

elif pilihan == "aktivasi tempat parkir":
    st.title("Aktivasi Tempat Parkir")

    booked_slot = [
        a["Tempat Parkir"]
        for a in st.session_state.bookings
        if a["Status"] == "Booked"
    ]

    if not booked_slot:
        st.info("Belum ada slot yang dibooking")
    else:
        with st.form("form_aktivasi"):
            tempat_parkir = st.selectbox("Pilih Slot", booked_slot)
            durasi = st.number_input("Durasi Parkir (jam)", 1, 168)

            if st.form_submit_button("Aktivasi"):
                for booking in st.session_state.bookings:
                    if booking["Tempat Parkir"] == tempat_parkir:
                        booking["Durasi"] = durasi
                        booking["Tarif per Jam"] = get_harga_per_jam(booking["Jenis"])
                        booking["Biaya Total"] = hitung_biaya(durasi, booking["Jenis"])
                        booking["Status"] = "Aktivated"
                        st.success("Tempat parkir berhasil diaktivasi!")
                        st.rerun()
                        break

elif pilihan == "Pembayaran":
    st.title("Pembayaran Parkir")

    activated_slot = [
        a["Tempat Parkir"]
        for a in st.session_state.bookings
        if a["Status"] == "Aktivated"
    ]

    if not activated_slot:
        st.info("Belum ada parkir yang diaktivasi")
    else:
        with st.form("form_pembayaran"):
            tempat_parkir = st.selectbox("Pilih Slot", activated_slot)

            if st.form_submit_button("Bayar"):
                for booking in st.session_state.bookings:
                    if booking["Tempat Parkir"] == tempat_parkir:
                        booking["Status"] = "Paid"
                        st.success(f"Pembayaran Rp {booking['Biaya Total']} berhasil!")
                        st.rerun()
                        break

elif pilihan == "dashboard penghasilan":
    st.title("Dashboard Admin")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if "login" not in st.session_state:
        st.session_state.login = False

    if st.button("Login"):
        st.session_state.login = (user == "admin" and password == "admin123")
        st.rerun()

    if st.session_state.login:
        paid = [a for a in st.session_state.bookings if a["Status"] == "Paid"]
        total = sum(a["Biaya Total"] for a in paid)

        st.metric("Total Penghasilan", f"Rp {total}")
        st.table(paid)
    else:
        st.warning("Login sebagai admin")

