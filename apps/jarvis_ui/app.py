import os
import requests
import streamlit as st
from datetime import date

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.set_page_config(page_title="ipe", layout="wide")
st.title("ipe — Paneller")

with st.expander("Durum & Kısayollar", expanded=False):
    cols = st.columns(4)
    try:
        man = requests.get(f"{API_BASE}/manifest.json", timeout=5).json()
        cols[0].success(f"API OK v{man.get('version','?')}")
    except Exception as e:
        cols[0].error(f"API hata: {e}")

    try:
        comps = requests.get(f"{API_BASE}/api/companies", timeout=5).json()
        cols[1].info(f"{len(comps)} şirket")
    except Exception as e:
        cols[1].warning(f"Şirketler alınamadı: {e}")

    try:
        mh = requests.get("http://mailhog:8025/api/v2/messages", timeout=5).json()
        total = mh.get("total", len(mh.get("items", [])))
        cols[2].info(f"MailHog OK, {total} mesaj")
    except Exception as e:
        cols[2].warning(f"MailHog erişilemedi: {e}")

    cols[3].markdown(
        "[API Docs](http://localhost:8000/docs)  \n"
        "[MailHog](http://localhost:18025)  \n"
        "[UI](http://localhost:8501)"
    )

tab_companies, tab_email, tab_directive, tab_report = st.tabs(
    ["Şirketler", "E-posta Testi", "Yönerge", "Günlük Rapor"]
)

with tab_companies:
    st.subheader("Şirketler (API)")
    try:
        resp = requests.get(f"{API_BASE}/api/companies", timeout=10)
        resp.raise_for_status()
        companies = resp.json()
    except Exception as e:
        companies = []
        st.error(f"API erişim hatası: {e}")

    if companies:
        st.dataframe(companies, use_container_width=True, hide_index=True)
    else:
        st.info("Kayıt yok.")

    st.divider()
    st.markdown("#### Yeni Şirket Ekle")
    with st.form("add_company"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Ad *")
            website = st.text_input("Web sitesi")
        with col2:
            country = st.text_input("Ülke")
            city = st.text_input("Şehir")
        if st.form_submit_button("Ekle"):
            if not name.strip():
                st.warning("Ad zorunlu.")
            else:
                payload = {"name": name.strip()}
                if website.strip():
                    payload["website"] = website.strip()
                if country.strip():
                    payload["country"] = country.strip()
                if city.strip():
                    payload["city"] = city.strip()
                try:
                    r = requests.post(
                        f"{API_BASE}/api/companies", json=payload, timeout=10
                    )
                    r.raise_for_status()
                except Exception as e:
                    st.error(f"Ekleme hatası: {e}")
                else:
                    st.success("Şirket eklendi.")
                    st.rerun()

with tab_email:
    st.subheader("MailHog’a test maili gönder")
    st.caption("MailHog UI: http://localhost:18025")
    with st.form("send_mailhog"):
        to = st.text_input("Alıcı", value="deneme@local")
        subject = st.text_input("Konu", value="MailHog test")
        body = st.text_area("İçerik", value="Merhaba! Bu bir testtir.")
        if st.form_submit_button("Gönder"):
            try:
                r = requests.post(
                    f"{API_BASE}/api/email/test",
                    json={"to": to, "subject": subject, "body": body},
                    timeout=10,
                )
                r.raise_for_status()
            except Exception as e:
                st.error(f"Gönderim hatası: {e}")
            else:
                st.success("Gönderildi. MailHog’dan kontrol edebilirsin.")

with tab_directive:
    st.subheader("Metinden niyet tahmini (Directive)")
    text = st.text_input("Komut / metin", value="Berlin’de 2 km yatak ara")
    if st.button("Gönder"):
        try:
            r = requests.post(
                f"{API_BASE}/api/directive", json={"text": text}, timeout=10
            )
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            st.error(f"İstek hatası: {e}")
        else:
            st.success("Alındı")
            st.json(data)
            msg = data.get("message")
            intent = data.get("intent_guess")
            if msg or intent:
                st.info(f"Mesaj: {msg}\n\nNiyet: **{intent}**")

with tab_report:
    st.subheader("Günlük Rapor")
    use_date = st.toggle("Tarih seç", value=False)
    params = {}
    if use_date:
        d = st.date_input("Tarih", value=date.today(), format="YYYY-MM-DD")
        params["date"] = d.isoformat()

    if st.button("Raporu getir"):
        try:
            r = requests.get(f"{API_BASE}/api/reports/daily", params=params, timeout=15)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            st.error(f"Rapor alınamadı: {e}")
        else:
            if isinstance(data, list):
                st.dataframe(data, use_container_width=True, hide_index=True)
            elif isinstance(data, dict) and any(
                isinstance(v, list) for v in data.values()
            ):
                for k, v in data.items():
                    if isinstance(v, list):
                        st.markdown(f"**{k}**")
                        st.dataframe(v, use_container_width=True, hide_index=True)
            else:
                st.json(data)
