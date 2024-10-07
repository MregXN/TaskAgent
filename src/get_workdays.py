import requests  
import env
from datetime import datetime , timedelta
  
params = {  
    'api_key': env.CALENDARIFIC_API_KEY,  
    'country': env.COUNTRY,
    'year': env.YEAR,
    'type': 'national'
}  

def get_workdys():
    response = requests.get(env.CALENDARIFIC_URL, params=params) 
    result = [] 

    if response.status_code == 200:  
        data = response.json()  
        holidays = data['response']['holidays']  

        holiday_dates = {}
        for holiday in holidays:  
            date_str = holiday['date']['iso']  
            description = holiday['name']  
            holiday_dates[date_str] = description  
        
        year = env.YEAR
        start_date = datetime(year, datetime.now().month , datetime.today().day)  
        end_date = start_date + timedelta(days=30) 
        delta = timedelta(days=1)  
        
        current_date = start_date  
        while current_date <= end_date:  
            date_str = current_date.strftime('%Y-%m-%d')  
            weekday = current_date.weekday()
            weekday_name = current_date.strftime('%A')  
            
            if date_str in holiday_dates:  
                day_type = "Non-working days"  
                description = holiday_dates[date_str]  
                result.append(f"Date: {date_str}, Type: {weekday_name}, {day_type}, {description}")
                current_date += delta
                continue
            elif weekday >= 5: 
                day_type = "Non-working days"  
            else:  
                day_type = "Working days"  
            
            result.append(f"Date: {date_str}, Type: {weekday_name}, {day_type}")
            current_date += delta  
    else:  
        print('Error:', response.status_code, response.text) 

    return "\n".join(result) 

if __name__ == "__main__":
    print(get_workdys())