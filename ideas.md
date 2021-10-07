# Streamlit helpful commands 
1. View app in browser locally: streamlit run my_app.py
2. Stop streamlit server: Ctrl+c


# TAGUP PROJECT DESCRIPTION
To see how you think about large-scale data set visualizations, we have a brief technical challenge detailed here. You are provided with a simulated data set of 2,100 assets around New York City. Data about the assets include:
    - identifier (asset_n)
    - physical location (long, lat)
    - metadata  
    - a hazard (effectively, a failure probability)

Your __goal is to visualize this information effectively__. For context, the user is an asset manager who is responsible for __maximizing the uptime of their equipment fleet__. Failure probabilities (hazard) represent the probability the asset will fail in the next 12 hours.

Storytelling is a bit part of our work; taking complex data/machine learning model ouputs and making it easy to understand. You will be evaluated in part on the clarity of your communication (including data representations, visual design, and supporting documentation).

# Brainstorm 
1. Examine 1 asset (1 row) failure probability over dt
2. Find average failure probability of all assets over time 
3. Find top assets most likely to fail 
4. Create customizable faulty asset viz with total asset number + timestamps as free params 
5. Examine variance of failure to find outliers