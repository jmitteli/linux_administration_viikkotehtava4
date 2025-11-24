from flask import Flask
import mysql.connector

app = Flask(__name__)

@app.route('/')
def home():
    # Yhdistetään MySQL/MariaDB:hen
    conn = mysql.connector.connect(
        host="localhost",
        user="exampleuser",
        password="change_this_strong_password",
        database="exampledb"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")
    db_time = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    lemp_ascii = r"""
██╗       ███████╗ ███╗   ███╗ ██████╗ 
██║       ██╔════╝ ████╗ ████║ ██╔══██╗
██║       █████╗   ██╔████╔██║ ██████╔╝
██║       ██╔══╝   ██║╚██╔╝██║ ██╔═══╝ 
███████╗  ███████╗ ██║ ╚═╝ ██║ ██║     
╚══════╝  ╚══════╝ ╚═╝     ╚═╝ ╚═╝     
"""

    stack_ascii = r"""
 ██████╗  ████████╗  █████╗    ██████╗  ██╗  ██╗
██╔════╝  ╚══██╔══╝ ██╔══██╗  ██╔════╝  ██║ ██╔╝
╚█████╗      ██║    ███████║  ██║       █████╔╝ 
 ╚═══██╗     ██║    ██╔══██║  ██║       ██╔═██╗ 
 █████╔╝     ██║    ██║  ██║  ╚██████╗  ██║  ██╗
 ╚════╝      ╚═╝    ╚═╝  ╚═╝   ╚═════╝  ╚═╝  ╚═╝
"""

    return f"""
    <html>
      <head>
        <title>LEMP-demo</title>
        <style>
          body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f2f2f2;
          }}
          .ascii-lemp {{
            font-family: monospace;
            font-size: 18px;
            font-weight: 900;
            line-height: 1.1;
            white-space: pre;
            margin-top: 24px;
          }}
          .ascii-stack {{
            font-family: monospace;
            font-size: 12px;
            font-weight: 800;
            line-height: 1.1;
            white-space: pre;
            margin-top: 4px;
          }}
        </style>
      </head>
      <body>
        <h1>Welcome to my LEMP-page!</h1>
        <h1>Kotitehtävä 3</h1>
        <p>This page is running LEMP-stack on Nginx + MySQL + Flask!</p>
        <p><strong>MySQL-server time is:</strong> {db_time}</p>
        <p><strong>THIS WAS FUN ENJOY THE ASCII ART!!!!</strong></p>

        <div class="ascii-lemp">{lemp_ascii}</div>
        <div class="ascii-stack">{stack_ascii}</div>
        
        <p>
          <a href="/data-analysis/" style="font-size: 24px;">
            Siirry data-analysis -sivulle
          </a>
        </p>

      </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
