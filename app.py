import joblib
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler

# Improved and dynamic CSS
def inject_dynamic_css(score):
    # Choose color based on score
    if score >= 90:
        bg_color = "#e6ffe6"
        border_color = "#28a745"
    elif score >= 80:
        bg_color = "#e6f7ff"
        border_color = "#17a2b8"
    elif score >= 70:
        bg_color = "#fffbe6"
        border_color = "#ffc107"
    elif score >= 60:
        bg_color = "#fff0f0"
        border_color = "#fd7e14"
    else:
        bg_color = "#020000"
        border_color = "#dc3545"

    st.markdown(f"""
    <style>
        /* General Styling */
        .main-header {{
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            font-family: 'Segoe UI', sans-serif;
        }}

        /* Prediction Result Box */
        .prediction-result {{
            font-size: 2.2rem;
            font-weight: bold;
            color: {border_color};
            text-align: center;
            padding: 1.5rem;
            background: linear-gradient(145deg, {bg_color}, #ffffff);
            border-radius: 18px;
            margin: 1.5rem 0;
            border: 3px solid {border_color};
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}

        .prediction-result:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        }}

        /* Input & Results Sections */
        .input-section {{
            background: linear-gradient(90deg, #f8f9fa 60%, #e3f2fd 100%);
            padding: 2rem;
            border-radius: 18px;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .results-section {{
            background: linear-gradient(90deg, #ffffff 60%, #e6ffe6 100%);
            padding: 2rem;
            border-radius: 18px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.09);
            margin: 1rem 0;
        }}

        /* Improve metrics readability */
        .stMetric {{
            font-size: 1.2rem !important;
        }}
        
        .tips-list {{
            font-size: 1.1rem;
            margin-left: 1.2rem;
        }}

        /* ✅ Responsive Styling for Mobile */
        @media (max-width: 768px) {{
            .main-header {{
                font-size: 2rem;
                margin-bottom: 1rem;
            }}
            .prediction-result {{
                font-size: 1.5rem;
                padding: 1rem;
            }}
            .input-section, .results-section {{
                padding: 1.2rem;
            }}
            .stMetric {{
                font-size: 1rem !important;
            }}
        }}

        @media (max-width: 480px) {{
            .main-header {{
                font-size: 1.6rem;
            }}
            .prediction-result {{
                font-size: 1.3rem;
                padding: 0.8rem;
                margin: 1rem 0;
            }}
            .tips-list {{
                font-size: 1rem;
            }}
        }}
    </style>
    """, unsafe_allow_html=True)

class StudentPerformancePredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self._load_model_and_scaler()
    
    def _load_model_and_scaler(self):
        try:
            self.model = joblib.load("model.pkl")
            # Fit StandardScaler with typical value ranges (demo only)
            self.scaler = StandardScaler()
            X_fit = np.array([
                [0, 0, 0, 3, 0],      # min values
                [40, 100, 100, 12, 2] # max values
            ])
            self.scaler.fit(X_fit)
        except Exception as e:
            st.error(f"Error loading model or initializing scaler: {str(e)}")
    
    def predict(self, hours_studied, attendance, previous_scores, sleep_hours, motivation_level):
        """Make prediction based on input features"""
        try:
            input_features = np.array([[hours_studied, attendance, previous_scores, sleep_hours, motivation_level]])
            input_scaled = self.scaler.transform(input_features)
            prediction = self.model.predict(input_scaled)
            return max(0, min(100, prediction[0]))  # Ensure prediction is between 0-100
        except Exception as e:
            st.error(f"Error making prediction: {str(e)}")
            return None
    
# Initialize the predictor
@st.cache_resource
def get_predictor():
    return StudentPerformancePredictor()

def get_performance_tips(hours_studied, attendance, previous_scores, sleep_hours, motivation_level, predicted_score):
    tips = []
    if hours_studied < 15:
        tips.append("📚 **Increase study hours:** Aim for at least 15-20 hours per week for better retention.")
    if attendance < 85:
        tips.append("🎓 **Improve attendance:** Consistent class presence boosts understanding and grades.")
    if sleep_hours < 7:
        tips.append("😴 **Get more sleep:** 7-8 hours nightly helps memory and focus.")
    if motivation_level == "Low":
        tips.append("💪 **Boost motivation:** Set small goals, reward progress, and study with friends.")
    if previous_scores < 75:
        tips.append("📈 **Strengthen basics:** Review previous exam mistakes and clarify concepts.")
    if predicted_score < 60:
        tips.append("🆘 **Seek help:** Consider tutoring, group study, or talking to teachers for guidance.")
    if hours_studied > 30:
        tips.append("⚖️ **Avoid burnout:** Take regular breaks and balance study with relaxation.")
    if sleep_hours > 9:
        tips.append("⏰ **Optimize sleep:** Too much sleep can reduce alertness; 7-8 hours is ideal.")
    if motivation_level == "High" and predicted_score < 80:
        tips.append("🔄 **Channel motivation:** Try new study techniques like active recall or spaced repetition.")
    if not tips:
        tips.append("✅ **Excellent habits!** Keep up your balanced routine for continued success.")
    return tips

def main():
    predictor = get_predictor()
    
    # Main title
    st.markdown('<h1 class="main-header">📚 Student Performance Predictor</h1>', unsafe_allow_html=True)
    
    # Description
    st.markdown("""
    <div style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
        Enter your study habits and academic details to predict your exam performance
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    st.subheader("📝 Enter Your Details")
    
    # Create input form
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            hours_studied = st.number_input(
                "📖 Hours Studied per Week",
                min_value=0.0,
                max_value=40.0,
                value=15.0,
                step=0.5,
                help="Enter the number of hours you study per week"
            )
            
            attendance = st.slider(
                "🎓 Attendance Percentage",
                min_value=0,
                max_value=100,
                value=85,
                help="Your class attendance percentage"
            )
            
            previous_scores = st.number_input(
                "📊 Previous Exam Scores (Average)",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=0.1,
                help="Your average score from previous exams"
            )
        
        with col2:
            sleep_hours = st.slider(
                "😴 Sleep Hours per Night",
                min_value=3,
                max_value=12,
                value=7,
                help="Average hours of sleep you get per night"
            )
            
            motivation_level = st.selectbox(
                "💪 Motivation Level",
                options=["Low", "Medium", "High"],
                index=1,
                help="Rate your current motivation level for studies"
            )
        
        # Center the submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button("🔮 Predict My Score", use_container_width=True, type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Results section
    if submitted:
        # Validate inputs
        if hours_studied < 0 or hours_studied > 40:
            st.error("⚠️ Hours studied should be between 0 and 40 hours per week")
            return
        
        if attendance < 0 or attendance > 100:
            st.error("⚠️ Attendance should be between 0 and 100 percent")
            return
        
        # Map motivation level to numeric
        motivation_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
        motivation_numeric = motivation_mapping[motivation_level]
        
        # Make prediction
        with st.spinner("🤔 Analyzing your performance factors..."):
            predicted_score = predictor.predict(
                hours_studied, attendance, previous_scores, 
                sleep_hours, motivation_numeric
            )
        
        if predicted_score is not None:
            
            # Display prediction with enhanced styling
            st.markdown(
                f'<div class="prediction-result">🎯 Predicted Exam Score: {predicted_score:.1f}/100</div>',
                unsafe_allow_html=True
            )
            
            # Performance interpretation
            if predicted_score >= 90:
                st.success("🌟 **Outstanding Performance Expected!** You're on track for excellent results!")
                recommendation = "Keep up the excellent work! Your study habits are exemplary."
            elif predicted_score >= 80:
                st.success("🎉 **Great Performance Expected!** You're doing very well!")
                recommendation = "You're on the right track! Consider maintaining your current routine."
            elif predicted_score >= 70:
                st.info("📈 **Good Performance Expected.** Room for improvement!")
                recommendation = "Good foundation! Try increasing study hours or improving attendance."
            elif predicted_score >= 60:
                st.warning("⚠️ **Average Performance.** Significant improvement needed.")
                recommendation = "Consider improving your study habits, attendance, and sleep schedule."
            else:
                st.error("📉 **Below Average Performance.** Major improvements required.")
                recommendation = "Focus on increasing study time, improving attendance, and getting adequate sleep."
            
            st.info(f"💡 **Recommendation:** {recommendation}")
            
            # Visualization
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=predicted_score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Predicted Score"},
                delta={'reference': 75, 'position': "top"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "#1f77b4"},
                    'steps': [
                        {'range': [0, 60], 'color': "#ffcccc"},
                        {'range': [60, 70], 'color': "#fff3cd"},
                        {'range': [70, 80], 'color': "#d1ecf1"},
                        {'range': [80, 90], 'color': "#d4edda"},
                        {'range': [90, 100], 'color': "#c3e6cb"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Input summary in a nice format
            st.subheader("📋 Your Input Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📖 Study Hours/Week", f"{hours_studied} hrs")
                st.metric("🎓 Attendance", f"{attendance}%")
            with col2:
                st.metric("📊 Previous Scores", f"{previous_scores:.1f}")
                st.metric("😴 Sleep Hours", f"{sleep_hours} hrs")
            with col3:
                st.metric("💪 Motivation", motivation_level)
            
            # Performance improvement tips
            st.subheader("💡 Tips to Improve Performance")
            
            tips = get_performance_tips(hours_studied, attendance, previous_scores, sleep_hours, motivation_level, predicted_score)
            st.markdown('<ul class="tips-list">', unsafe_allow_html=True)
            for tip in tips:
                st.markdown(f"<li>{tip}</li>", unsafe_allow_html=True)
            st.markdown('</ul>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()


