# 環境建立
1. **建立虛擬環境**  
     `python -m venv <dir_name>`  
     `cd <dir_name>`  
    啟動虛擬環境  
     `Scripts\activate`  
     離開虛擬環境  
     `deactivate`  

2. **安裝環境** 
     `git clone <api_enhancement專案>`
     `cd api_enhancement`
     `pip install -r requirements.txt`  

3. **Run Server**    
     `python manage.py runserver`

4. **API** 
    1. Get __lineItem/UnblendedCost__ grouping by __product/productname__
        - Request method : POST
        - URL : http://127.0.0.1:8000/api/getlineItemUnblendedCost/
        - Input
          | Column | Required |
          | ------ | -------- |
          | lineitem/usageaccountid | true |
        - Request body(sample)
        ```JSON
            {
                "lineitem/usageaccountid": "829432956742"
            }
        ```
        - Response body
        ```JSON
            {
                "result": "Success/Fail",
                "code": "XXXXXX",
                "output": {
                    "{product/productname_A}": "sum(lineitem/unblendedcost)",
                    "{product/productname_B}": "sum(lineitem/unblendedcost)",
                    ...
                }
            }
        ```        
    2. Get daily __lineItem/UsageAmount__ grouping by __product/productname__ 
        - Request method : POST
        - URL : http://127.0.0.1:8000/api/getDailyLineItemUsageAmount/
        - Input
          | Column | Required |
          | ------ | -------- |
          | lineitem/usageaccountid | true |
        - Request body(sample)
        ```JSON
            {
                "lineitem/usageaccountid": "829432956742"
            }
        ```
        - Response body
        ```JSON
            {
                "result": "Success/Fail",
                "code": "XXXXXX",
                "output": {
                    "{product/productname_A}": {
                        "YYYY/MM/01": "sum(lineItem/UsageAmount)",
                        "YYYY/MM/02": "sum(lineItem/UsageAmount)",
                        "YYYY/MM/03": "sum(lineItem/UsageAmount)",
                        ...
                    },
                    "{product/productname_B}": {
                        "YYYY/MM/01": "sum(lineItem/UsageAmount)",
                        "YYYY/MM/02": "sum(lineItem/UsageAmount)",
                        "YYYY/MM/03": "sum(lineItem/UsageAmount)",
                        ...
                    },
                }
            }
        ```  
5. **DB schema**
    Use __local SQLite__

     
> 製作By @gim227
"# api-enhancement" 
