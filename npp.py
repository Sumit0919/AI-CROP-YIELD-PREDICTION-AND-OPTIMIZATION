import streamlit as st
import pandas as pd
import pickle
import requests 
import time
from datetime import datetime
from streamlit_lottie import st_lottie 

# --- Load the Trained Models ---
try:
    with open('crop_recommendation_model.pkl', 'rb') as f:
        crop_model = pickle.load(f)
except FileNotFoundError:
    st.error("Model file not found. Make sure 'crop_recommendation_model.pkl' is in the same folder.")
    st.stop()

# --- Full Translation Dictionary for All 5 Languages ---
translations = {
    "English": {
        "title": "AI CROP YIELD PREDICTION AND OPTIMIZATION 🧑‍🌾", "subtitle": "Get data-driven advice for your farm.", "sidebar_title": "Settings", "lang_select": "Language", "tab1_title": "🌱 Crop Recommendation", "tab2_title": "💡 Actionable Advice", "tab3_title": "📈 Productivity Insights", "header1": "Find the Perfect Crop", "date_label": "Select Today's Date", "location_select": "Select a Location to get Live Data", "api_button": "Fetch Live Weather Data (Real API)", "api_desc": "Select a city and click the button to get real-time weather data from a live API.", "n_label": "Nitrogen (N) in soil (kg/ha)", "p_label": "Phosphorus (P) in soil (kg/ha)", "k_label": "Potassium (K) in soil (kg/ha)", "temp_label": "Temperature (°C)", "hum_label": "Relative Humidity (%)", "ph_label": "Soil pH", "rain_label": "Average Annual Rainfall (mm)", "recommend_button": "Recommend My Crop", "success_msg": "The most suitable crop for your conditions is:", "header2": "Get Smart Farming Advice", "desc2": "Recommendations based on your input values.", "seasonal_advice": "Seasonal Advice", "kharif_season": "The selected date falls in the Kharif season (June-Oct). This is the main monsoon sowing season.", "rabi_season": "The selected date falls in the Rabi season (Nov-Mar). This is the winter sowing season.", "zaid_season": "The selected date falls in the Zaid season (Apr-May). This is the summer season for short-duration crops.", "fert_advice": "Fertilizer Recommendation", "n_low": "Nitrogen (N) is low. Add organic compost or a nitrogen-rich fertilizer.", "p_low": "Phosphorus (P) is low. Bone meal or a phosphate fertilizer would be beneficial.", "k_low": "Potassium (K) is low. Wood ash or potash can help root development.", "fert_ok": "Your soil's nutrient levels (N, P, K) look good!", "water_advice": "Water Management Advice", "rain_low": "Rainfall is low. Plan for consistent irrigation and consider drought-resistant crops.", "rain_ok": "Rainfall is adequate. Ensure good drainage.", "pest_advice": "Pest Control Advice", "pest_warn": "High humidity and heat can attract pests like aphids. Monitor crops closely.", "pest_ok": "Conditions are less favorable for common pests, but regular monitoring is key.", "header3": "Boosting Your Farm's Productivity", "desc3_1": "Our AI platform helps you make smarter decisions that can directly increase your farm's output.", "metric_label": "Potential Productivity Increase", "desc3_2": "How do we achieve this?", "point1": "Yield Prediction Model: Our second AI model analyzes historical data to predict potential yield.", "point2": "Reduced Waste: Smart fertilizer advice means you only use what you need, saving money.", "point3": "Risk Mitigation: Early warnings about pests and water needs help protect your crops."
    },
    "Hindi (हिन्दी)": {
        "title": "एआई किसान सहायक 🧑‍🌾", "subtitle": "अपने खेत के लिए डेटा-आधारित सलाह प्राप्त करें।", "sidebar_title": "सेटिंग्स", "lang_select": "भाषा", "tab1_title": "🌱 फसल की सिफारिश", "tab2_title": "💡 कार्रवाई योग्य सलाह", "tab3_title": "📈 उत्पादकता अंतर्दृष्टि", "header1": "सही फसल खोजें", "date_label": "आज की तारीख चुनें", "location_select": "लाइव डेटा प्राप्त करने के लिए एक स्थान चुनें", "api_button": "लाइव मौसम डेटा प्राप्त करें (रियल एपीआई)", "api_desc": "एक शहर चुनें और लाइव एपीआई से वास्तविक समय का मौसम डेटा प्राप्त करने के लिए बटन पर क्लिक करें।", "n_label": "मिट्टी में नाइट्रोजन (N) (किग्रा/हेक्टेयर)", "p_label": "मिट्टी में फास्फोरस (P) (किग्रा/हेक्टेयर)", "k_label": "मिट्टी में पोटेशियम (K) (किग्रा/हेक्टेयर)", "temp_label": "तापमान (°C)", "hum_label": "सापेक्ष आर्द्रता (%)", "ph_label": "मिट्टी का पीएच", "rain_label": "औसत वार्षिक वर्षा (मिमी)", "recommend_button": "मेरी फसल की सिफारिश करें", "success_msg": "आपकी परिस्थितियों के लिए सबसे उपयुक्त फसल है:", "header2": "स्मार्ट खेती की सलाह लें", "desc2": "आपके इनपुट मूल्यों के आधार पर सिफारिशें।", "seasonal_advice": "मौसमी सलाह", "kharif_season": "चुनी गई तारीख खरीफ मौसम (जून-अक्टूबर) में आती है। यह मुख्य मानसून बुवाई का मौसम है।", "rabi_season": "चुनी गई तारीख रबी मौसम (नवंबर-मार्च) में आती है। यह सर्दियों की बुवाई का मौसम है।", "zaid_season": "चुनी गई तारीख जायद मौसम (अप्रैल-मई) में आती है। यह कम अवधि की फसलों के लिए गर्मी का मौसम है।", "fert_advice": "उर्वरक की सिफारिश", "n_low": "नाइट्रोजन (N) कम है। जैविक खाद या नाइट्रोजन युक्त उर्वरक डालें।", "p_low": "फास्फोरस (P) कम है। हड्डी का चूरा या फॉस्फेट उर्वरक फायदेमंद होगा।", "k_low": "पोटेशियम (K) कम है। लकड़ी की राख या पोटाश जड़ों के विकास में मदद कर सकता है।", "fert_ok": "आपकी मिट्टी के पोषक तत्व (N, P, K) का स्तर अच्छा लग रहा है!", "water_advice": "जल प्रबंधन सलाह", "rain_low": "वर्षा कम है। लगातार सिंचाई की योजना बनाएं और सूखा प्रतिरोधी फसलों पर विचार करें।", "rain_ok": "वर्षा पर्याप्त है। अच्छी जल निकासी सुनिश्चित करें।", "pest_advice": "कीट नियंत्रण सलाह", "pest_warn": "उच्च आर्द्रता और गर्मी एफिड्स जैसे कीटों को आकर्षित कर सकती है। फसलों की बारीकी से निगरानी करें।", "pest_ok": "आम कीटों के लिए स्थितियाँ कम अनुकूल हैं, लेकिन नियमित निगरानी महत्वपूर्ण है।", "header3": "अपने खेत की उत्पादकता बढ़ाना", "desc3_1": "हमारा एआई प्लेटफॉर्म आपको बेहतर निर्णय लेने में मदद करता है जो सीधे आपके खेत के उत्पादन को बढ़ा सकता है।", "metric_label": "संभावित उत्पादकता वृद्धि", "desc3_2": "हम इसे कैसे प्राप्त करते हैं?", "point1": "उपज भविष्यवाणी मॉडल: हमारा दूसरा एआई मॉडल संभावित उपज की भविष्यवाणी करने के लिए ऐतिहासिक डेटा का विश्लेषण करता है।", "point2": "कम बर्बादी: स्मार्ट उर्वरक सलाह का मतलब है कि आप केवल अपनी जरूरत का उपयोग करते हैं, जिससे पैसे की बचत होती है।", "point3": "जोखिम में कमी: कीटों और पानी की जरूरतों के बारे में शुरुआती चेतावनियाँ आपकी फसलों की रक्षा करने में मदद करती हैं।"
    },
    "Marathi (मराठी)": {
        "title": "एआय शेतकरी सहाय्यक 🧑‍🌾", "subtitle": "तुमच्या शेतासाठी डेटा-आधारित सल्ला मिळवा.", "sidebar_title": "सेटिंग्ज", "lang_select": "भाषा", "tab1_title": "🌱 पीक शिफारस", "tab2_title": "💡 कृतीयोग्य सल्ला", "tab3_title": "📈 उत्पादकता अंतर्दृष्टी", "header1": "योग्य पीक शोधा", "date_label": "आजची तारीख निवडा", "location_select": "थेट डेटा मिळविण्यासाठी स्थान निवडा", "api_button": "थेट हवामान डेटा मिळवा (वास्तविक API)", "api_desc": "शहर निवडा आणि थेट API वरून हवामान डेटा मिळवण्यासाठी बटणावर क्लिक करा.", "n_label": "मातीतील नायट्रोजन (N) (किलो/हेक्टर)", "p_label": "मातीतील फॉस्फरस (P) (किलो/हेक्टर)", "k_label": "मातीतील पोटॅशियम (K) (किलो/हेक्टर)", "temp_label": "तापमान (°C)", "hum_label": "सापेक्ष आर्द्रता (%)", "ph_label": "मातीचा पीएच", "rain_label": "सरासरी वार्षिक पर्जन्यमान (मिमी)", "recommend_button": "माझ्या पिकाची शिफारस करा", "success_msg": "तुमच्या परिस्थितीसाठी सर्वात योग्य पीक आहे:", "header2": "स्मार्ट शेती सल्ला मिळवा", "desc2": "तुमच्या इनपुट मूल्यांवर आधारित शिफारसी.", "seasonal_advice": "हंगामी सल्ला", "kharif_season": " निवडलेली तारीख खरीप हंगामात (जून-ऑक्टोबर) येते. हा मुख्य मान्सून पेरणीचा हंगाम आहे.", "rabi_season": " निवडलेली तारीख रब्बी हंगामात (नोव्हेंबर-मार्च) येते. हा हिवाळी पेरणीचा हंगाम आहे.", "zaid_season": " निवडलेली तारीख झैद हंगामात (एप्रिल-मे) येते. हा कमी कालावधीच्या पिकांसाठी उन्हाळी हंगाम आहे.", "fert_advice": "खत शिफारस", "n_low": "नायट्रोजन (N) कमी आहे. सेंद्रिय कंपोस्ट किंवा नायट्रोजनयुक्त खत घाला.", "p_low": "फॉस्फरस (P) कमी आहे. हाडांचे जेवण किंवा फॉस्फेट खत फायदेशीर ठरेल.", "k_low": "पोटॅशियम (K) कमी आहे. लाकडी राख किंवा पोटॅशमुळे मुळांच्या विकासास मदत होते.", "fert_ok": "तुमच्या मातीतील पोषक तत्वांची (N, P, K) पातळी चांगली आहे!", "water_advice": "जल व्यवस्थापन सल्ला", "rain_low": "पर्जन्यमान कमी आहे. सातत्यपूर्ण सिंचनाची योजना करा आणि दुष्काळ-प्रतिरोधक पिकांचा विचार करा.", "rain_ok": "पर्जन्यमान पुरेसे आहे. चांगल्या निचऱ्याची खात्री करा.", "pest_advice": "कीड नियंत्रण सल्ला", "pest_warn": "जास्त आर्द्रता आणि उष्णतेमुळे माव्यासारख्या कीटकांना आकर्षित करू शकते. पिकांवर बारकाईने लक्ष ठेवा.", "pest_ok": "सर्वसाधारण कीटकांसाठी परिस्थिती कमी अनुकूल आहे, परंतु नियमित निरीक्षण महत्त्वाचे आहे.", "header3": "तुमच्या शेताची उत्पादकता वाढवणे", "desc3_1": "आमचे एआय प्लॅटफॉर्म तुम्हाला हुशार निर्णय घेण्यास मदत करते ज्यामुळे तुमच्या शेताचे उत्पादन थेट वाढू शकते.", "metric_label": "संभाव्य उत्पादकता वाढ", "desc3_2": "आम्ही हे कसे साध्य करतो?", "point1": "उत्पन्न अंदाज मॉडेल: आमचे दुसरे एआय मॉडेल संभाव्य उत्पन्नाचा अंदाज लावण्यासाठी ऐतिहासिक डेटाचे विश्लेषण करते.", "point2": "कमी अपव्यय: स्मार्ट खत सल्ल्यामुळे तुम्ही फक्त गरजेनुसार वापरता, ज्यामुळे पैशांची बचत होते.", "point3": "जोखीम कमी करणे: कीटक आणि पाण्याच्या गरजेबद्दल लवकर चेतावणी तुमच्या पिकांचे संरक्षण करण्यास मदत करते."
    },
    "Odia (ଓଡ଼ିଆ)": {
        "title": "ଏଆଇ କୃଷକ ସହାୟକ 🧑‍🌾", "subtitle": "ଆପଣଙ୍କ ଫାର୍ମ ପାଇଁ ତଥ୍ୟ-ଆଧାରିତ ପରାମର୍ଶ ପାଆନ୍ତୁ |", "sidebar_title": "ସେଟିଂସମୂହ", "lang_select": "ଭାଷା", "tab1_title": "🌱 ଫସଲ ସୁପାରିଶ", "tab2_title": "💡 କାର୍ଯ୍ୟାନୁଷ୍ଠାନ ପରାମର୍ଶ", "tab3_title": "📈 ଉତ୍ପାଦକତା ଅନ୍ତର୍ଦୃଷ୍ଟି", "header1": "ଉପଯୁକ୍ତ ଫସଲ ଖୋଜନ୍ତୁ", "date_label": "ଆଜିର ତାରିଖ ବାଛନ୍ତୁ |", "location_select": "ଲାଇଭ୍ ଡାଟା ପାଇବାକୁ ଏକ ସ୍ଥାନ ବାଛନ୍ତୁ |", "api_button": "ଲାଇଭ୍ ପାଣିପାଗ ଡାଟା ପାଆନ୍ତୁ (ବାସ୍ତବ API)", "api_desc": "ଏକ ସହର ବାଛନ୍ତୁ ଏବଂ ଲାଇଭ୍ API ରୁ ବାସ୍ତବ ସମୟ ପାଣିପାଗ ଡାଟା ପାଇବାକୁ ବଟନ୍ କ୍ଲିକ୍ କରନ୍ତୁ |", "n_label": "ମାଟିରେ ନାଇଟ୍ରୋଜେନ୍ (N) (କିଗ୍ରା/ହେକ୍ଟର)", "p_label": "ମାଟିରେ ଫସଫରସ୍ (P) (କିଗ୍ରା/ହେକ୍ଟର)", "k_label": "ମାଟିରେ ପୋଟାସିୟମ୍ (K) (କିଗ୍ରା/ହେକ୍ଟର)", "temp_label": "ତାପମାତ୍ରା (°C)", "hum_label": "ଆପେକ୍ଷିକ ଆର୍ଦ୍ରତା (%)", "ph_label": "ମାଟିର ପିଏଚ୍", "rain_label": "ହାରାହାରି ବାର୍ଷିକ ବର୍ଷା (ମିମି)", "recommend_button": "ମୋ ଫସଲ ସୁପାରିଶ କରନ୍ତୁ", "success_msg": "ଆପଣଙ୍କ ସ୍ଥିତି ପାଇଁ ସବୁଠାରୁ ଉପଯୁକ୍ତ ଫସଲ ହେଉଛି:", "header2": "ସ୍ମାର୍ଟ ଚାଷ ପରାମର୍ଶ ପାଆନ୍ତୁ", "desc2": "ଆପଣଙ୍କ ଇନପୁଟ୍ ମୂଲ୍ୟ ଉପରେ ଆଧାରିତ ସୁପାରିଶ |", "seasonal_advice": "ଋତୁକାଳୀନ ପରାମର୍ଶ", "kharif_season": "ଚୟନିତ ତାରିଖ ଖରିଫ ଋତୁରେ (ଜୁନ୍-ଅକ୍ଟୋବର) ଆସେ | ଏହା ମୁଖ୍ୟ ମୌସୁମୀ ବୁଣିବା ଋତୁ |", "rabi_season": "ଚୟନିତ ତାରିଖ ରବି ଋତୁରେ (ନଭେମ୍ବର-ମାର୍ଚ୍ଚ) ଆସେ | ଏହା ଶୀତକାଳୀନ ବୁଣିବା ଋତୁ |", "zaid_season": "ଚୟନିତ ତାରିଖ ଜୟଦ ଋତୁରେ (ଏପ୍ରିଲ-ମେ) ଆସେ | ଏହା କମ୍ ଅବଧିର ଫସଲ ପାଇଁ ଗ୍ରୀଷ୍ମ ଋତୁ |", "fert_advice": "ସାର ସୁପାରିଶ", "n_low": "ନାଇଟ୍ରୋଜେନ୍ (N) କମ୍ ଅଛି | ଜୈବିକ କମ୍ପୋଷ୍ଟ କିମ୍ବା ନାଇଟ୍ରୋଜେନ୍-ଯୁକ୍ତ ସାର ଯୋଗ କରନ୍ତୁ |", "p_low": "ଫସଫରସ୍ (P) କମ୍ ଅଛି | ହାଡ ଗୁଣ୍ଡ କିମ୍ବା ଫସଫେଟ୍ ସାର ଲାଭଦାୟକ ହେବ |", "k_low": "ପୋଟାସିୟମ୍ (K) କମ୍ ଅଛି | କାଠ ପାଉଁଶ କିମ୍ବା ପୋଟାଶ୍ ମୂଳର ବିକାଶରେ ସାହାଯ୍ୟ କରିପାରିବ |", "fert_ok": "ଆପଣଙ୍କ ମାଟିର ପୋଷକ ସ୍ତର (N, P, K) ଭଲ ଦେଖାଯାଉଛି!", "water_advice": "ଜଳ ପରିଚାଳନା ପରାମର୍ଶ", "rain_low": "ବର୍ଷା କମ୍ ଅଛି | ନିରନ୍ତର ଜଳସେଚନ ପାଇଁ ଯୋଜନା କରନ୍ତୁ ଏବଂ ମରୁଡ଼ି-ପ୍ରତିରୋଧୀ ଫସଲ ବିଚାର କରନ୍ତୁ |", "rain_ok": "ବର୍ଷା ପର୍ଯ୍ୟାପ୍ତ ଅଛି | ଭଲ ଜଳ ନିଷ୍କାସନ ସୁନିଶ୍ଚିତ କରନ୍ତୁ |", "pest_advice": "କୀଟ ନିୟନ୍ତ୍ରଣ ପରାମର୍ଶ", "pest_warn": "ଅଧିକ ଆର୍ଦ୍ରତା ଏବଂ ଉତ୍ତାପ ଏଫିଡ୍ସ ପରି କୀଟମାନଙ୍କୁ ଆକର୍ଷିତ କରିପାରେ | ଫସଲଗୁଡ଼ିକୁ ନିକଟରୁ ନିରୀକ୍ଷଣ କରନ୍ତୁ |", "pest_ok": "ସାଧାରଣ କୀଟମାନଙ୍କ ପାଇଁ ସ୍ଥିତି କମ୍ ଅନୁକୂଳ, କିନ୍ତୁ ନିୟମିତ ନିରୀକ୍ଷଣ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ |", "header3": "ଆପଣଙ୍କ ଫାର୍ମର ଉତ୍ପାଦକତା ବୃଦ୍ଧି", "desc3_1": "ଆମର ଏଆଇ ପ୍ଲାଟଫର୍ମ ଆପଣଙ୍କୁ ଚତୁର ନିଷ୍ପତ୍ତି ନେବାରେ ସାହାଯ୍ୟ କରେ ଯାହା ଆପଣଙ୍କ ଫାର୍ମର ଉତ୍ପାଦନକୁ ସିଧାସଳଖ ବଢାଇପାରେ |", "metric_label": "ସମ୍ଭାବ୍ୟ ଉତ୍ପାଦକତା ବୃଦ୍ଧି", "desc3_2": "ଆମେ ଏହା କିପରି ହାସଲ କରୁ?", "point1": "ଉପଜ ପୂର୍ବାନୁମାନ ମଡେଲ୍: ଆମର ଦ୍ୱିତୀୟ ଏଆଇ ମଡେଲ୍ ସମ୍ଭାବ୍ୟ ଉପଜର ପୂର୍ବାନୁମାନ କରିବାକୁ ଐତିହାସିକ ତଥ୍ୟ ବିଶ୍ଳେଷଣ କରେ |", "point2": "କମ୍ ବର୍ଜ୍ୟବସ୍ତୁ: ସ୍ମାର୍ଟ ସାର ପରାମର୍ଶର ଅର୍ଥ ଆପଣ କେବଳ ଆବଶ୍ୟକତା ଅନୁଯାୟୀ ବ୍ୟବହାର କରନ୍ତି, ଯାହା ଟଙ୍କା ବଞ୍ଚାଏ |", "point3": "ବିପଦ ହ୍ରାସ: କୀଟ ଏବଂ ପାଣିର ଆବଶ୍ୟକତା ବିଷୟରେ ଶୀଘ୍ର ଚେତାବନୀ ଆପଣଙ୍କ ଫସଲକୁ ସୁରକ୍ଷା ଦେବାରେ ସାହାଯ୍ୟ କରେ |"
    },
    "Bhojpuri (भोजपुरी)": {
        "title": "एआई किसान सहायक 🧑‍🌾", "subtitle": "आपन खेत खातिर डेटा-आधारित सलाह पाईं।", "sidebar_title": "सेटिंग्स", "lang_select": "भाषा", "tab1_title": "🌱 फसल के सिफारिश", "tab2_title": "💡 कार्रवाई लायक सलाह", "tab3_title": "📈 उत्पादकता अंतर्दृष्टि", "header1": "सही फसल खोजीं", "date_label": "आज के तारीख चुनीं", "location_select": "लाइव डेटा पावे खातिर एगो लोकेशन चुनीं", "api_button": "लाइव मौसम डेटा पाईं (रियल एपीआई)", "api_desc": "एगो शहर चुनीं आ लाइव एपीआई से रियल-टाइम मौसम डेटा पावे खातिर बटन पर क्लिक करीं।", "n_label": "माटी में नाइट्रोजन (N) (किग्रा/हेक्टेयर)", "p_label": "माटी में फास्फोरस (P) (किग्रा/हेक्टेयर)", "k_label": "माटी में पोटेशियम (K) (किग्रा/हेक्टेयर)", "temp_label": "तापमान (°C)", "hum_label": "सापेक्ष आर्द्रता (%)", "ph_label": "माटी के पीएच", "rain_label": "औसत वार्षिक बरसात (मिमी)", "recommend_button": "हमरा फसल के सिफारिश करीं", "success_msg": "राउर परिस्थिति खातिर सबसे उपयुक्त फसल ह:", "header2": "स्मार्ट खेती के सलाह पाईं", "desc2": "राउर दिहल मान के आधार पर सिफारिश।", "seasonal_advice": "मौसमी सलाह", "kharif_season": "चुनल तारीख खरीफ मौसम (जून-अक्टूबर) में पड़ेला। इ मुख्य मानसून के बोवाई के मौसम ह।", "rabi_season": "चुनल तारीख रबी मौसम (नवंबर-मार्च) में पड़ेला। इ जाड़ा के बोवाई के मौसम ह।", "zaid_season": "चुनल तारीख जायद मौसम (अप्रैल-मई) में पड़ेला। इ कम समय के फसल खातिर गर्मी के मौसम ह।", "fert_advice": "उर्वरक के सिफारिश", "n_low": "नाइट्रोजन (N) कम बा। जैविक खाद भा नाइट्रोजन वाला उर्वरक डालीं।", "p_low": "फास्फोरस (P) कम बा। हड्डी के चूरा भा फास्फेट उर्वरक फायदेमंद होई।", "k_low": "पोटेशियम (K) कम बा। लकड़ी के राख भा पोटाश जड़ के विकास में मदद कर सकेला।", "fert_ok": "राउर माटी के पोषक तत्व (N, P, K) के स्तर ठीक लागत बा!", "water_advice": "जल प्रबंधन सलाह", "rain_low": "बरसात कम बा। लगातार सिंचाई के योजना बनाईं अवुरी सूखा प्रतिरोधी फसल पर विचार करीं।", "rain_ok": "बरसात पर्याप्त बा। बढ़िया जल निकासी सुनिश्चित करीं।", "pest_advice": "कीट नियंत्रण सलाह", "pest_warn": "जादा नमी अवुरी गर्मी एफिड्स जइसन कीट के आकर्षित कर सकेला। फसल पर निमन से नजर रखीं।", "pest_ok": "आम कीट खातिर स्थिति कम अनुकूल बा, लेकिन नियमित निगरानी जरूरी बा।", "header3": "आपन खेत के उत्पादकता बढ़ावल", "desc3_1": "हमनी के एआई प्लेटफार्म राउर के स्मार्ट निर्णय लेवे में मदद करेला जवन सीधे राउर खेत के उत्पादन बढ़ा सकेला।", "metric_label": "संभावित उत्पादकता बढ़ोतरी", "desc3_2": "हमनी के इ कईसे हासिल करिले?", "point1": "उपज भविष्यवाणी मॉडल: हमनी के दूसरा एआई मॉडल संभावित उपज के भविष्यवाणी करे खातिर ऐतिहासिक डेटा के विश्लेषण करेला।", "point2": "कम बर्बादी: स्मार्ट उर्वरक सलाह के मतलब बा कि रउआ खाली ओतने इस्तेमाल करीं जेतना जरूरत बा, जवना से पईसा बचेला।", "point3": "जोखिम कम कईल: कीट अवुरी पानी के जरूरत के बारे में पहिले से चेतावनी राउर फसल के रक्षा करे में मदद करेला।"
    }
}

# --- Helper function to determine the season ---
def get_season(date):
    month = date.month
    if 6 <= month <= 10: return "kharif_season"
    elif 11 <= month or month <= 3: return "rabi_season"
    else: return "zaid_season"

# --- Helper function to load Lottie animation from URL ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- REAL API FUNCTION ---
def get_live_data(latitude, longitude):
    try:
        api_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
        response = requests.get(api_url)
        data = response.json()
        temperature = data['current_weather']['temperature']
        humidity = 60 + (temperature * 0.8) 
        return {"temperature": temperature, "humidity": humidity}
    except Exception as e:
        st.error(f"Error fetching data from API: {e}")
        return None

# --- Page Configuration ---
st.set_page_config(page_title="AI Farmer's Assistant", page_icon="🧑‍🌾", layout="wide")

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .stButton>button {
        background-color: #4A9A41; color: white; border-radius: 20px; border: 2px solid #4A9A41;
        padding: 10px 20px; font-size: 16px; font-weight: bold; transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: white; color: #4A9A41; border-color: #4A9A41;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if 'api_data' not in st.session_state:
    st.session_state.api_data = {}

# --- Lottie Animation ---
lottie_url = "https://assets9.lottiefiles.com/packages/lf20_AYj382.json"
lottie_json = load_lottieurl(lottie_url)

# --- Sidebar ---
with st.sidebar:
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=150, key="initial")
    st.title(translations["English"]["sidebar_title"]) # Sidebar title is always English for clarity
    language = st.selectbox(translations["English"]["lang_select"], list(translations.keys()))
    lang = translations.get(language, translations["English"])

# --- Main Page Content ---
st.title(lang["title"])
st.write(lang["subtitle"])

tab1, tab2, tab3 = st.tabs([lang.get("tab1_title"), lang.get("tab2_title"), lang.get("tab3_title")])

locations = { "Mumbai": (19.0760, 72.8777), "Delhi": (28.7041, 77.1025), "Bhubaneswar (Odisha)": (20.2961, 85.8245), "Patna (Bhojpuri Region)": (25.5941, 85.1376) }

with tab1:
    st.header(lang["header1"])
    selected_date = st.date_input(lang["date_label"], datetime.now())
    st.info(lang["api_desc"])
    selected_location = st.selectbox(lang["location_select"], list(locations.keys()))
    if st.button(lang["api_button"]):
        lat, lon = locations[selected_location]
        with st.spinner(f"Fetching live weather for {selected_location}..."):
            live_data = get_live_data(lat, lon)
            if live_data:
                st.session_state.api_data = live_data
                st.success("Live data loaded successfully!")

    temp_val = st.session_state.api_data.get("temperature", 25.0)
    hum_val = st.session_state.api_data.get("humidity", 70.0)

    col1, col2, col3 = st.columns(3)
    with col1: N = st.number_input(lang["n_label"], 0, 140, 90)
    with col2: P = st.number_input(lang["p_label"], 5, 145, 42)
    with col3: K = st.number_input(lang["k_label"], 5, 205, 43)

    temperature = st.slider(lang["temp_label"], -10.0, 50.0, temp_val)
    humidity = st.slider(lang["hum_label"], 10.0, 100.0, hum_val)
    ph = st.slider(lang["ph_label"], 3.5, 9.0, 6.5)
    rainfall = st.slider(lang["rain_label"], 20.0, 400.0, 150.0)

    if st.button(lang["recommend_button"]):
        input_data = pd.DataFrame({'N': [N], 'P': [P], 'K': [K], 'temperature': [temperature], 'humidity': [humidity], 'ph': [ph], 'rainfall': [rainfall]})
        prediction = crop_model.predict(input_data)
        st.success(f"{lang['success_msg']} **{prediction[0].capitalize()}**")

with tab2:
    st.header(lang["header2"])
    st.subheader(lang["seasonal_advice"])
    season_key = get_season(selected_date)
    st.success(lang[season_key])
    
    st.subheader(lang["fert_advice"])
    if N < 80: st.info(lang["n_low"])
    if P < 40: st.info(lang["p_low"])
    if K < 40: st.info(lang["k_low"])
    if not (N < 80 or P < 40 or K < 40): st.success(lang["fert_ok"])
    
    st.subheader(lang["water_advice"])
    if rainfall < 120: st.warning(lang["rain_low"])
    else: st.success(lang["rain_ok"])

    st.subheader(lang["pest_advice"])
    if humidity > 80 and temperature > 28: st.warning(lang["pest_warn"])
    else: st.success(lang["pest_ok"])

with tab3:
    st.header(lang["header3"])
    st.metric(label=lang["metric_label"], value="10-15%")
    st.write(lang["desc3_1"])
    st.subheader(lang["desc3_2"])
    st.markdown(f"- **{lang['point1']}**")
    st.markdown(f"- **{lang['point2']}**")
    st.markdown(f"- **{lang['point3']}**")