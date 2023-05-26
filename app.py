from flask import Flask, render_template, request
from datetime import datetime, timedelta
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'user': 'u77082_RdiYqKREydj',
    'password': 'CVC7qXF^hY+zzEkHcj!Dd^m2',
    'host': '54.37.204.19',
    'database': 's77082_Punishments'
}

# Route for displaying bans
@app.route('/bans')
def display_bans():
    steamid = request.args.get('steamid')  # Get the SteamID from the query parameter

    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if steamid:
        # Query to retrieve bans for the specified SteamID
        query = "SELECT b.BanId, b.PlayerId, p.PlayerName, b.PunisherId, b.BanReason, b.BanDuration, b.BanCreated " \
                "FROM Bans AS b " \
                "JOIN Players AS p ON b.PlayerId = p.PlayerId " \
                "WHERE b.PlayerId = %s"
        cursor.execute(query, (steamid,))
    else:
        # Query to retrieve all bans and player names
        query = "SELECT b.BanId, b.PlayerId, p.PlayerName, b.PunisherId, b.BanReason, b.BanDuration, b.BanCreated " \
                "FROM Bans AS b " \
                "JOIN Players AS p ON b.PlayerId = p.PlayerId"
        cursor.execute(query)

    # Fetch all ban details from the result set
    bans = cursor.fetchall()

    # Get today's date
    today = datetime.now().date()

    # Count bans that occurred today
    bans_today = sum(1 for ban in bans if ban[6].date() == today)

    # Close the database connection
    cursor.close()
    conn.close()

    # Render the template with ban details, the SteamID, and bans_today count
    return render_template('bans.html', bans=bans, steamid=steamid, bans_today=bans_today)


# Route for displaying punishments
@app.route('/punishments')
def display_punishments():
    steamid = request.args.get('steamid')  # Get the SteamID from the query parameter

    # Connect to MySQL
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if steamid:
        # Query to retrieve punishments for the specified SteamID
        query = "SELECT p.PunishmentId, p.PlayerId, pl.PlayerName, p.PunisherId, p.Type, p.Reason, p.CreateDate " \
                "FROM Punishments AS p " \
                "JOIN Players AS pl ON p.PlayerId = pl.PlayerId " \
                "WHERE p.PlayerId = %s"
        cursor.execute(query, (steamid,))
    else:
        # Query to retrieve all punishments and player names
        query = "SELECT p.PunishmentId, p.PlayerId, pl.PlayerName, p.PunisherId, p.Type, p.Reason, p.CreateDate " \
                "FROM Punishments AS p " \
                "JOIN Players AS pl ON p.PlayerId = pl.PlayerId"
        cursor.execute(query)

    # Fetch all punishment details from the result set
    punishments = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Render the template with punishment details, the SteamID, and an empty count
    return render_template('punish.html', punishments=punishments, steamid=steamid)


if __name__ == '__main__':
    app.run(host='syntalebans.info')
