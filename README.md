# IMDBWEBSCRAB
# IMDb 2024 Data Analysis Project

## 📌 Project Overview
This project is a **data analysis and visualization tool** for IMDb movie data from **2024**. It scrapes IMDb movie information, stores it in **TiDB Cloud**, and visualizes key insights using **Streamlit**.

## 🚀 Features
- **Web Scraping:** Extracts movie data from IMDb
- **TiDB Cloud Database:** Stores and retrieves movie information
- **Streamlit Web App:** Interactive dashboard for data visualization
- **Filters & Analysis:**
  - Filter movies by **genre, rating, votes, and duration**
  - View **top-rated movies**
  - **Genre distribution** insights
  - **Average movie duration by genre**
  - **Rating distribution**
  - **Correlation between ratings and votes**

## 🛠️ Tech Stack
- **Python** (for data scraping and analysis)
- **Selenium & Pandas** (for web scraping)
- **MySQL & TiDB Cloud** (for database management)
- **Streamlit** (for interactive dashboard)
- **Matplotlib & Seaborn** (for data visualization)

## 📂 Project Structure
```
📁 IMDB2024-Analysis
│── 📂 data_scraping/   # Scripts for IMDb data extraction
│── 📂 streamlit_app/   # Streamlit dashboard source code
│── 📂 database/        # SQL scripts for TiDB setup
│── README.md          # Project documentation
│── requirements.txt   # Python dependencies
│── imdb_scraper.py    # IMDb web scraping script
│── streamlit_app.py   # Main Streamlit app
```

## 🔧 Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/IMDB2024-Analysis.git
cd IMDB2024-Analysis
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up TiDB Cloud Connection
- Update the `ssl_ca` path in the `streamlit_app.py` file:
```python
ssl_ca = "path/to/your/ca.pem"
```

### 4️⃣ Run the Streamlit App
```bash
streamlit run streamlit_app.py
```

## 📊 Data Insights
1️⃣ **Top 10 Movies by Ratings** 🎥
2️⃣ **Genre-wise Movie Distribution** 📊
3️⃣ **Correlation Between Ratings & Votes** 🔗
4️⃣ **Movie Duration Trends** ⏳

## 🤝 Contributing
Feel free to submit **issues** and **pull requests**! 🎉

## 📜 License
MIT License. See [LICENSE](LICENSE) for details.

---
🚀 **Built with ❤️ using Python, Streamlit, and TiDB Cloud!**

