lst = "cust_fname,cust_lname,cust_email, cust_mobilenumber,cust_accnum,cust_atm_number,cust_atm_pin,cust_acccif,cust_acc_ifsc,cust_acc_activationcode".split(",")

print(lst)

for item in lst:
    print("change " + item + " " +item + " varchar(45)," )