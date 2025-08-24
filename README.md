# 📚 Student Performance Predictor

A sophisticated machine learning web application built with Streamlit that predicts student exam scores based on various performance factors including study habits, attendance, sleep patterns, and motivation levels.

![Student Performance Predictor](https://via.placeholder.com/800x400/1f77b4/ffffff?text=Student+Performance+Predictor)

## 🚀 Features

- **Interactive Web Interface**: Clean, responsive Streamlit interface with dynamic styling
- **Real-time Predictions**: Instant exam score predictions (0-100) based on input parameters
- **Dynamic Visual Feedback**: Color-coded results and interactive gauge charts
- **Personalized Recommendations**: Smart tips based on individual performance factors
- **Input Validation**: Comprehensive error handling and range validation
- **Responsive Design**: Mobile-friendly interface with adaptive styling
- **Performance Insights**: Detailed analysis with improvement suggestions

## 📊 Model Features

The predictor analyzes the following factors:

- **📖 Study Hours per Week** (0-40 hours)
- **🎓 Attendance Percentage** (0-100%)
- **📊 Previous Exam Scores** (0-100)
- **😴 Sleep Hours per Night** (3-12 hours)
- **💪 Motivation Level** (Low/Medium/High)

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Pre-trained model file (`model.pkl`)

## 🛠️ Installation & Setup

### 1. Clone or Download the Project

```bash
# Create a new directory for your project
mkdir student-performance-predictor
cd student-performance-predictor

# Copy the app.py and requirements.txt files to this directory
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Create a `requirements.txt` file:

```
streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
joblib==1.3.2
plotly==5.15.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Prepare Your Model

Ensure you have a `model.pkl` file containing:

```python
# model.pkl should contain a dictionary with:
{
    'model': trained_sklearn_model,
}
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📱 How to Use

### Making Predictions

1. **Enter Student Details:**
   - Set study hours per week (0-40)
   - Adjust attendance percentage (0-100%)
   - Input previous exam scores average
   - Set sleep hours per night (3-12)
   - Select motivation level (Low/Medium/High)

2. **Get Prediction:**
   - Click "🔮 Predict My Score"
   - View predicted exam score with color-coded feedback
   - Review performance interpretation and recommendations

3. **Analyze Results:**
   - Interactive gauge chart showing score visualization
   - Personalized improvement tips
   - Input summary with key metrics


## 🎨 Dynamic Styling Features

The application features adaptive styling based on predicted scores:

- **🟢 Excellent (90-100)**: Green theme with success indicators
- **🔵 Good (80-89)**: Blue theme with positive feedback
- **🟡 Average (70-79)**: Yellow theme with improvement suggestions
- **🟠 Below Average (60-69)**: Orange theme with warnings
- **🔴 Poor (<60)**: Red theme with urgent recommendations


### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t student-predictor .
docker run -p 8501:8501 student-predictor
```

## 📊 File Structure

```
student-performance-predictor/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── model.pkl             # Pre-trained model and scaler
├── README.md             # Project documentation
```

## 📈 Performance Metrics

The application provides insights on:

- **Score Ranges**: Color-coded performance categories
- **Improvement Areas**: Targeted recommendations
- **Study Habits**: Hours and motivation analysis
- **Health Factors**: Sleep and attendance correlation
- **Historical Performance**: Previous scores consideration

## 🚀 Future Enhancements

- [ ] Multiple model algorithms comparison
- [ ] Historical prediction tracking
- [ ] Batch predictions from CSV upload
- [ ] Advanced visualization dashboards
- [ ] User authentication and profiles
- [ ] API endpoints for external integration
- [ ] A/B testing for model improvements

---

**Made with ❤️ using Streamlit and Python**

*Empowering students with data-driven insights for academic success!*
