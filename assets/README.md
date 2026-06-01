# 🎨 Project Assets & Styling Resources

This directory is designated for graphic layouts, branding assets, custom webfonts, and secondary CSS models that enhance the interface styling.

---

## 🗂️ Asset Directory Contents

### 1. Typography Fonts
*   The application imports the **Outfit** Google WebFont (`https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap`).
*   Outfit is a geometric sans-serif typeface designed for digital screens, providing a clean, modern aesthetic that feels premium.

### 2. Glassmorphism styling (`src/helpers.py`)
*   The premium CSS layout is loaded dynamically into the application from `src/helpers.py` using `load_custom_css()`.
*   This approach avoids static file binding and ensures style resources load reliably, even when running the dashboard in different cloud host containers (e.g. Streamlit Share, Heroku, AWS).

### 3. Branding Logos
*   Place secondary corporate logos or company avatars in this folder as `company_logo.png` if required.
*   They can be loaded directly into the Streamlit sidebar using:
    ```python
    st.sidebar.image("assets/company_logo.png", use_container_width=True)
    ```
