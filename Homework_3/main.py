from flask import Flask, jsonify, render_template_string
import util

app = Flask(__name__)

# Database connection details
username = 'irv121'
password = 'test'
host = '127.0.0.1'
port = '5432'
database = 'postgres'

@app.route('/api/update_basket_a')
def update_basket_a():
    try:
        # Connect to the database
        cursor, connection = util.connect_to_db(username, password, host, port, database)

        # Execute the insert command
        cursor.execute("INSERT INTO basket_a (a, fruit_a) VALUES (5, 'Cherry');")
        
        # Commit the transaction
        connection.commit()

        # Disconnect from the database
        util.disconnect_from_db(connection, cursor)

        return jsonify({"message": "Success!"}), 200
        
    except Exception as e:
        # Return error message on the client side
        print(f"An error occurred: {e}")
        util.disconnect_from_db(connection, cursor)
        return jsonify({"error": str(e)}), 500


@app.route('/api/unique')

def unique_fruits():
    try:
        cursor, connection = util.connect_to_db(username, password, host, port, database)

        # Fetch fruits that are only in basket_a (not in basket_b)
        cursor.execute("""
            SELECT DISTINCT fruit_a 
            FROM basket_a 
            WHERE fruit_a NOT IN (SELECT fruit_b FROM basket_b);
        """)
        unique_fruits_a = [row[0] for row in cursor.fetchall()]

        # Fetch fruits that are only in basket_b (not in basket_a)
        cursor.execute("""
            SELECT DISTINCT fruit_b 
            FROM basket_b 
            WHERE fruit_b NOT IN (SELECT fruit_a FROM basket_a);
        """)
        unique_fruits_b = [row[0] for row in cursor.fetchall()]

        util.disconnect_from_db(connection, cursor)
        
        # HTML template for displaying unique fruits in an HTML table
        html_template = """
        <html>
            <head><title>Unique Fruits</title></head>
            <body>
                <h2>Unique Fruits in Each Basket</h2>
                <table border="1">
                    <tr>
                        <th>Unique Fruits in Basket A</th>
                        <th>Unique Fruits in Basket B</th>
                    </tr>
                    <tr>
                        <td>
                            <ul>
                                {% for fruit in unique_fruits_a %}
                                    <li>{{ fruit }}</li>
                                {% endfor %}
                            </ul>
                        </td>
                        <td>
                            <ul>
                                {% for fruit in unique_fruits_b %}
                                    <li>{{ fruit }}</li>
                                {% endfor %}
                            </ul>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        """
        
        # Render the HTML template with the unique fruits data
        return render_template_string(html_template, unique_fruits_a=unique_fruits_a, unique_fruits_b=unique_fruits_b)
        
    except Exception as e:
        util.disconnect_from_db(connection, cursor)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Enable debug mode
    app.debug = True
    # Run the app on the local machine IP
    app.run(host='127.0.0.1', port=5000)
