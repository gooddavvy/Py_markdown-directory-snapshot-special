navbar_html = """
    <style>
        /* Hide default sidebar */
        [data-testid="stSidebarNav"] {display: none;}
        
        /* Navbar styling */
        .navbar {
            background-color: #2E86C1;
            overflow: hidden;
            display: flex;
            justify-content: center;
            padding: 10px 0;
        }
        .navbar a {
            color: white;
            padding: 12px 20px;
            text-decoration: none;
            font-size: 18px;
            font-weight: bold;
        }
        .navbar a:hover {
            background-color: #1A5276;
        }
    </style>

    <div class="navbar">
        <a href="/?nav=snapshot" target="_self">📸 Generate Snapshot</a>
        <a href="/?nav=recreation" target="_self">📑 Recreate from Snapshot</a>
    </div>
"""
