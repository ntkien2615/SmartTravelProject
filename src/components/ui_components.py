"""UI Components for SmartTravel"""

import streamlit as st


def render_hero_section(title, subtitle, emoji="✈️"):
    """Render a hero section with gradient background."""
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #1E88E5 0%, #26A69A 100%);
            color: white;
            padding: 3rem 2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        ">
            <h1 style="color: white; font-size: 3rem; margin-bottom: 1rem;">
                {title} {emoji}
            </h1>
            <p style="font-size: 1.25rem; opacity: 0.95; margin: 0;">
                {subtitle}
            </p>
        </div>
    """, unsafe_allow_html=True)


def render_feature_card(icon, title, description, col=None):
    """Render a feature card with hover effects."""
    if col:
        col.markdown(f"""
            <div style="
                text-align: center;
                padding: 2rem;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                border: 1px solid #E0E0E0;
                height: 100%;
            " class="feature-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
                <h3 style="color: #1E88E5; margin-bottom: 0.5rem;">{title}</h3>
                <p style="color: #616161; line-height: 1.6;">{description}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="
                text-align: center;
                padding: 2rem;
                background: white;
                border-radius: 12px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                border: 1px solid #E0E0E0;
                height: 100%;
            " class="feature-card">
                <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
                <h3 style="color: #1E88E5; margin-bottom: 0.5rem;">{title}</h3>
                <p style="color: #616161; line-height: 1.6;">{description}</p>
            </div>
        """, unsafe_allow_html=True)


def render_stat_card(label, value, icon="📊", delta=None):
    """Render a statistic card."""
    st.markdown(f"""
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #E0E0E0;
            text-align: center;
        ">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-size: 2rem; font-weight: 600; color: #1E88E5; margin-bottom: 0.25rem;">
                {value}
            </div>
            <div style="color: #757575; font-size: 0.875rem;">
                {label}
            </div>
            {f'<div style="color: #4CAF50; font-size: 0.875rem; margin-top: 0.25rem;">+{delta}</div>' if delta else ''}
        </div>
    """, unsafe_allow_html=True)


def render_location_card(name, address, image_url, on_save=None, on_navigate=None, key_prefix=""):
    """Render a location card with image and actions."""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(image_url, use_container_width=True)
    
    with col2:
        st.markdown(f"### {name}")
        st.caption(f"📍 {address}")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("💾 Lưu", key=f"{key_prefix}_save", use_container_width=True):
                if on_save:
                    on_save()
        with btn_col2:
            if st.button("🗺️ Chỉ đường", key=f"{key_prefix}_nav", use_container_width=True):
                if on_navigate:
                    on_navigate()


def render_section_header(title, subtitle=None, icon=None):
    """Render a section header with optional icon."""
    icon_text = f"{icon} " if icon else ""
    st.markdown(f"""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 style="color: #212121; font-weight: 600; margin-bottom: 0.5rem;">
                {icon_text}{title}
            </h2>
            {f'<p style="color: #757575; font-size: 1rem;">{subtitle}</p>' if subtitle else ''}
        </div>
    """, unsafe_allow_html=True)


def render_info_box(message, type="info"):
    """Render an info box with different styles."""
    colors = {
        "info": {"bg": "#E3F2FD", "border": "#2196F3", "icon": "ℹ️"},
        "success": {"bg": "#E8F5E9", "border": "#4CAF50", "icon": "✅"},
        "warning": {"bg": "#FFF3E0", "border": "#FF9800", "icon": "⚠️"},
        "error": {"bg": "#FFEBEE", "border": "#F44336", "icon": "❌"}
    }
    
    style = colors.get(type, colors["info"])
    
    st.markdown(f"""
        <div style="
            background: {style['bg']};
            border-left: 4px solid {style['border']};
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        ">
            <span style="font-size: 1.2rem; margin-right: 0.5rem;">{style['icon']}</span>
            <span style="color: #424242;">{message}</span>
        </div>
    """, unsafe_allow_html=True)


def render_divider():
    """Render a styled divider."""
    st.markdown("""
        <hr style="
            border: none;
            height: 2px;
            background: linear-gradient(to right, transparent, #E0E0E0, transparent);
            margin: 2rem 0;
        "/>
    """, unsafe_allow_html=True)


def render_badge(text, color="primary"):
    """Render a badge."""
    color_map = {
        "primary": "#1E88E5",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#F44336",
        "secondary": "#757575"
    }
    
    bg_color = color_map.get(color, color_map["primary"])
    
    st.markdown(f"""
        <span style="
            background: {bg_color};
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.875rem;
            font-weight: 500;
            display: inline-block;
        ">
            {text}
        </span>
    """, unsafe_allow_html=True)


def render_loading_spinner(text="Đang xử lý..."):
    """Render a loading state."""
    with st.spinner(text):
        return st.empty()


def render_empty_state(icon, title, description, action_text=None, action_callback=None):
    """Render an empty state."""
    st.markdown(f"""
        <div style="
            text-align: center;
            padding: 3rem 2rem;
            background: white;
            border-radius: 12px;
            border: 2px dashed #E0E0E0;
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">{icon}</div>
            <h3 style="color: #424242; margin-bottom: 0.5rem;">{title}</h3>
            <p style="color: #757575;">{description}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if action_text and action_callback:
        if st.button(action_text, key="empty_state_action"):
            action_callback()
