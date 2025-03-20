import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress specific warnings related to MySQL connection cleanup
warnings.filterwarnings("ignore", message="Exception ignored in: <function MySQLSocket.__del__ at")

# Database Configuration
config = {
    'user': 'root',
    'password': 'yaronsql',
    'host': 'localhost',
    'database': 'hr',
    'port': 3308,
    'raise_on_warnings': True
}

try:
    # Connect to MySQL and fetch data
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT player_id, first_name, score, game_date, game_time FROM players;")
    data = cursor.fetchall()
    
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['player_id', 'first_name', 'score', 'game_date', 'game_time'])
    df['game_time'] = df['game_time'].astype(str).str.extract(r'(\d{2}:\d{2}:\d{2})')[0]
    df['game_datetime'] = pd.to_datetime(df['game_date'].astype(str) + ' ' + df['game_time'])
    df['hour'] = df['game_datetime'].dt.hour
    
    # A. האם הישגים טובים יותר ביום או בלילה? (גרף לינארי)
    df['time_of_day'] = np.where(df['hour'].between(6, 18), 'Day', 'Night')
    avg_scores = df.groupby(['hour'])['score'].mean()
    
    plt.figure(figsize=(8, 4))
    sns.lineplot(x=avg_scores.index, y=avg_scores.values, marker='o', label='Average Score')
    plt.xlabel("Hour of the Day")
    plt.ylabel("Average Score")
    plt.title("Average Scores Throughout the Day")
    plt.grid()
    plt.legend()
    plt.show()
    
    # B. השוואה בין הישגי שני שחקנים (גרף עמודות)
    player1 = df[df['first_name'] == 'Yaron']
    player2 = df[df['first_name'] == 'Avi']
    
    plt.figure(figsize=(6, 4))
    plt.bar(['Yaron', 'Avi'], [player1['score'].mean(), player2['score'].mean()], color=['red', 'green'])
    plt.xlabel("Players")
    plt.ylabel("Average Score")
    plt.title("Comparison of Two Players' Scores")
    plt.show()
    
    # C. ניתוח שעות המשחק של שחקן מסוים (דיאגרמת עוגה)
    player_name = 'Yaron'
    player_data = df[df['first_name'] == player_name]['hour'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(player_data, labels=player_data.index, autopct='%1.1f%%', colors=plt.cm.Paired.colors)
    plt.title(f"Playing Hours Distribution for {player_name}")
    plt.show()
    
    # D. ממוצע ניקוד לפי יום בשבוע (מפת חום)
    df['weekday'] = df['game_datetime'].dt.day_name()
    avg_score_by_day = df.groupby('weekday')['score'].mean().reset_index()
    avg_score_by_day_pivot = avg_score_by_day.pivot_table(values='score', index='weekday', aggfunc='mean')
    
    plt.figure(figsize=(8, 4))
    sns.heatmap(avg_score_by_day_pivot, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.xlabel("Day of the Week")
    plt.ylabel("Average Score")
    plt.title("Average Score by Day of the Week (Heatmap)")
    plt.show()

except mysql.connector.Error as err:
    print(f"Error during MySQL connection: {err}")

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("MySQL connection closed.")