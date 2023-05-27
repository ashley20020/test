from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__, static_folder='static')

def search_bans(search):
    # Connect to MySQL database
    cnx = mysql.connector.connect(
        host='54.37.204.19',
        user='u77082_RdiYqKREyd',
        password='CVC7qXF^hY+zzEkHcj!Dd^m2',
        database='s77082_Punishments'
    )

    # Retrieve ban data from the "Bans" table and join with the "Players" table based on search
    cursor = cnx.cursor()
    query = "SELECT Bans.Id, Bans.PlayerId, Bans.PunisherId, Bans.BanType, Bans.Reason, Bans.BanCreated, Bans.ExpireDate, Bans.IsUnbanned, Players.SteamName FROM Bans INNER JOIN Players ON Bans.PlayerId = Players.SteamId WHERE Bans.Id LIKE %s OR Players.SteamName LIKE %s"
    cursor.execute(query, (f'%{search}%', f'%{search}%'))
    bans = cursor.fetchall()

    # Close database connection
    cursor.close()
    cnx.close()

    # Process the ban data to display "Currently Banned" or "Currently Unbanned" for the IsUnbanned column
    processed_bans = []
    for ban in bans:
        processed_ban = list(ban)
        if ban[7] == 0:
            processed_ban[7] = "Currently Banned"
        elif ban[7] == 1:
            processed_ban[7] = "Currently Unbanned"
        processed_bans.append(processed_ban)

    return processed_bans

@app.route('/', methods=['GET'])
def show_bans():
    search = request.args.get('search')
    if search:
        bans = search_bans(search)
    else:
        # Connect to MySQL database and retrieve all ban data from the "Bans" table
        cnx = mysql.connector.connect(
            host='54.37.204.19',
            user='u77082_RdiYqKREyd',
            password='CVC7qXF^hY+zzEkHcj!Dd^m2',
            database='s77082_Punishments'
        )
        cursor = cnx.cursor()
        cursor.execute("SELECT Bans.Id, Bans.PlayerId, Bans.PunisherId, Bans.BanType, Bans.Reason, Bans.BanCreated, Bans.ExpireDate, Bans.IsUnbanned, Players.SteamName FROM Bans INNER JOIN Players ON Bans.PlayerId = Players.SteamId")
        bans = cursor.fetchall()
        cursor.close()
        cnx.close()

    return render_template('bans.html', bans=bans)

if __name__ == '__main__':
    app.run()
