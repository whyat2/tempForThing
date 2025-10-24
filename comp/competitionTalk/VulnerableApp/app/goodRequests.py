import os
import mysql.connector
from Config import Config
import random
import string
import time 
from passwordEncryptOrBlock import getUnencryptedPass
from canmodifyProducts import manage_products
from legitimateRequest import add_product
from priceEncrypted import check_price_column_encryption

output_dir = "test_results"
os.makedirs(output_dir, exist_ok=True)

time.sleep(30)
add_product("Item0", 12.5)
add_product("Item01", 12.5)
add_product("Item02", 12.5)

time.sleep(450)
add_product("Item1", 12.5)
getUnencryptedPass("./test_results/getNotHashed.txt")
add_product("Item2", 13.5)

time.sleep(450)
manage_products("./test_results/modifyNonsense.txt")
add_product("Item3", 14.5)

time.sleep(450)
check_price_column_encryption("./test_results/encrypt.txt")

time.sleep(2)
while(True):
    time.sleep(10)