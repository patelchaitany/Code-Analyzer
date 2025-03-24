# This is a sample file with code quality issues

def CalculateTotal(orders):
    sum = 0
    for i in orders:
        sum += i["value"]
    return sum

def process_data(Data):
    # Process the data
    result = []
    for item in Data:
        if item["status"] == "active":
            if item["type"] == "premium":
                if item["price"] > 100:
                    result.append({"id": item["id"], "value": item["price"] * 0.9})
                else:
                    result.append({"id": item["id"], "value": item["price"]})
            else:
                result.append({"id": item["id"], "value": item["price"]})
    
    Total_Price = CalculateTotal(result)
    return Total_Price 