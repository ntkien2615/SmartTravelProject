"""Trang Hồ sơ"""
import streamlit as st
import services.db as db_utils
import time

@st.dialog("Chi tiết lịch trình")
def show_schedule_details(schedule, user_id):
    st.subheader(f"📍 {schedule['destination']}")
    st.caption(f"📅 {schedule['start_time']} – {schedule['end_time']}")
    st.write(f"💰 **Ngân sách:** {schedule['budget']:,} VND")
    
    st.markdown("---")
    st.markdown("#### 📝 Timeline chi tiết")
    
    for item in schedule["timeline"]:
        # Get extended info with defaults
        place = item.get('place', 'Unknown')
        arrive = item.get('arrive', '')
        depart = item.get('depart', '')
        mode = item.get('mode', '')
        travel_cost = item.get('travel_cost', 0)
        entry_fee = item.get('entry_fee', 0)
        
        # Display rich info
        with st.container():
            st.markdown(f"**📍 {place}**")
            st.caption(f"⏰ {arrive} – {depart}")
            
            details = []
            if mode:
                details.append(f"🚗 {mode.title()}")
            if travel_cost > 0:
                details.append(f"💵 Đi lại: {travel_cost:,}đ")
            if entry_fee > 0:
                details.append(f"🎫 Vé: {entry_fee:,}đ")
                
            if details:
                st.markdown(f"<span style='color:gray; font-size:0.9em'>{' | '.join(details)}</span>", unsafe_allow_html=True)
            st.divider()

    if st.button("🗑️ Xóa lịch trình này", key=f"delete_modal_{schedule['id']}", type="primary"):
        if db_utils.delete_schedule(schedule['id'], user_id):
            st.success("Đã xóa lịch trình.")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Lỗi khi xóa lịch trình.")


def page_ho_so():
    """Hiển thị nội dung trang Hồ sơ."""
    st.markdown("<div class='section-title'>Hồ sơ của bạn</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>Xem lại tài khoản và các lịch trình đã lưu.</div>",
        unsafe_allow_html=True,
    )

    if st.session_state.get("current_user"):
        st.success(f"Bạn đang đăng nhập với tài khoản: **{st.session_state['current_user']}**")

        st.markdown("### 👤 Thông tin tài khoản")
        st.write(f"**Email:** {st.session_state['current_user']}")

        st.markdown("### 🗂️ Lịch trình đã lưu")

        user_id = st.session_state.get("user_id")
        
        # Debug info (Temporary)
        # st.write(f"Debug Info: User ID = {user_id} (Type: {type(user_id)})")
        
        if user_id:
            schedules = db_utils.get_user_schedules(user_id)
            
            if not schedules:
                st.info("Bạn chưa có lịch trình nào được lưu. Hãy qua trang **Chức năng** > **Tạo lịch trình gợi ý** để tạo và lưu nhé!")
            else:
                st.write(f"Bạn có **{len(schedules)}** lịch trình đã lưu:")

                for schedule in schedules:
                    with st.container(border=True):
                        col_info, col_btn = st.columns([3, 1])
                        with col_info:
                            st.markdown(f"##### 🗺️ {schedule['destination']}")
                            st.caption(f"📅 {schedule['start_time']} – {schedule['end_time']} | 💰 {schedule['budget']:,} VND")
                        with col_btn:
                            if st.button("👁️ Xem chi tiết", key=f"btn_view_{schedule['id']}", use_container_width=True):
                                show_schedule_details(schedule, user_id)

        st.markdown("---")
        if st.button("Đăng xuất (Log out)"):
            # Delete cookie
            if 'cookie_manager' in st.session_state:
                st.session_state.cookie_manager.delete("user_email", key="delete_logout_cookie")
                
            st.session_state["current_user"] = None
            st.session_state["user_id"] = None
            
            # Wait for cookie deletion to propagate
            time.sleep(1)
            st.rerun()
    else:
        st.error("Bạn cần đăng nhập để xem trang này.")
        st.info("Vui lòng chọn **Sign in / Sign up** từ thanh menu để đăng nhập.")
