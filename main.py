import requests
import json

data = {
    "name": "Tanishka Soni",
    "regNo": "0827CI221135",
    "email": "tanishkasoni221237@acropolis.in"
}


init_url = "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
response = requests.post(init_url, json=data)
if response.status_code != 200:
    raise Exception(f"Error in generating webhook: {response.status_code} {response.text}")

response_json = response.json()
webhook_url = response_json["webhookUrl"]
access_token = response_json["accessToken"]


final_sql_query = """
SELECT 
    P.AMOUNT AS SALARY,
    CONCAT(E.FIRST_NAME, ' ', E.LAST_NAME) AS NAME,
    FLOOR(DATEDIFF(CURRENT_DATE, E.DOB) / 365.25) AS AGE,
    D.DEPARTMENT_NAME
FROM 
    PAYMENTS P
JOIN 
    EMPLOYEE E ON P.EMP_ID = E.EMP_ID
JOIN 
    DEPARTMENT D ON E.DEPARTMENT = D.DEPARTMENT_ID
WHERE 
    DAY(P.PAYMENT_TIME) != 1
ORDER BY 
    P.AMOUNT DESC
LIMIT 1;
"""


headers = {
    "Authorization": access_token,
    "Content-Type": "application/json"
}

payload = {
    "finalQuery": final_sql_query.strip()
}

submit_response = requests.post(webhook_url, headers=headers, json=payload)


if submit_response.status_code == 200:
    print("Query submitted successfully!")
else:
    print(f" Submission failed: {submit_response.status_code} {submit_response.text}")
