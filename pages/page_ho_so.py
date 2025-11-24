"""Trang Hồ sơ"""
import streamlit as st
import db_utils


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
        
        if user_id:
            schedules = db_utils.get_user_schedules(user_id)
            
            if not schedules:
                st.info("Bạn chưa có lịch trình nào được lưu. Hãy qua trang **Chức năng** > **Tìm kiếm nhanh** để tạo và lưu nhé!")
            else:
                st.write(f"Bạn có **{len(schedules)}** lịch trình đã lưu:")

                for schedule in schedules:
                    title = f"Lịch trình: {schedule['destination']} ({schedule['start_time']} – {schedule['end_time']})"

                    with st.expander("📅 " + title):
                        st.write(f"**Điểm đến:** {schedule['destination']}")
                        st.write(f"**Ngân sách:** {schedule['budget']:,} VND")
                        st.markdown("---")
                        st.write("**Timeline chi tiết:**")
                        for item in schedule["timeline"]:
                            st.markdown(
                                f"- **{item['place']}**: {item['arrive']} – {item['depart']}"
                            )
                        st.markdown("---")

                        if st.button("🗑️ Xóa lịch trình này", key=f"delete_{schedule['id']}"):
                            if db_utils.delete_schedule(schedule['id'], user_id):
                                st.success("Đã xóa lịch trình.")
                                st.rerun()
                            else:
                                st.error("Lỗi khi xóa lịch trình.")

        st.markdown("---")
        if st.button("Đăng xuất (Log out)"):
            # Delete cookie
            if 'cookie_manager' in st.session_state:
                st.session_state.cookie_manager.delete("user_email", key="delete_logout_cookie")
                
            st.session_state["current_user"] = None
            st.session_state["user_id"] = None
            st.rerun()
    else:
        st.error("Bạn cần đăng nhập để xem trang này.")
        st.info("Vui lòng chọn **Sign in / Sign up** từ thanh menu để đăng nhập.")
