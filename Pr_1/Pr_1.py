import pandas as pd
import os

os.chdir('C:/Users/User/.atom/ITMO_Work/4_Semestr/MEVD/Pr_1')

take_table_sale = pd.read_csv('./sales_train.csv')
take_table_shops = pd.read_csv('./shops.csv')
take_table_categories = pd.read_csv('./item_categories.csv')
take_table_items = pd.read_csv('./items.csv')

# Поток №1; Вариант 26; Задания 5 и 16

# Задание №5

items_cat_13 = take_table_items[take_table_items['category_id'] == 13]

sales_items_cat_13 = pd.merge(take_table_sale, items_cat_13, on='item_id')
sales_items_cat_13 = sales_items_cat_13[(sales_items_cat_13['date'].str.contains('2013')) | (sales_items_cat_13['date'].str.contains('2015'))]

# самый дешевый товар в каждой категории на каждую дату
cheap_items = sales_items_cat_13.groupby(['category_id', 'date'])[['item_id', 'item_price']].agg({'item_id': 'first', 'item_price': 'min'}).reset_index()

# добавление даты и id в вывод

result_cheap = pd.merge(cheap_items, sales_items_cat_13[['item_id', 'date', 'date_block_num']].drop_duplicates(), on=['item_id', 'date']).min()

print()
print("В 2015 года товар с категорией 13 отсутствовал")
print("Самый дешевый товар в категории 13 в 2013 году:")
print(result_cheap)

# Задание №16
print()
# январь каждого года
sales_jan = take_table_sale[take_table_sale['date'].str.contains('\.01\.', regex=True)]

# Суммарные продажи
sales_by_shop_month = sales_jan.groupby(['date', 'date_block_num', 'shop_id'], as_index=False)['item_cnt_day'].sum()
# print(sales_by_shop_month)
# добавление названия магазина
top_5_by_month = pd.merge(sales_by_shop_month, take_table_shops, on='shop_id')[['date', 'date_block_num', 'shop_id', 'shop_name', 'item_cnt_day']]

res_2013 = top_5_by_month[top_5_by_month['date'].str.contains('.2013', regex=True)]

res_2013_id = res_2013.groupby('shop_id')['item_cnt_day'].sum().nlargest(5).index.to_list()

res_2013_cnt_day = res_2013.groupby('shop_id')['item_cnt_day'].sum().nlargest(5).to_list()




print("Топ-5 магазинов по продажам в январе 2013:")

for i in range(len(res_2013_id)):
    print(f"{i + 1} Магазин {res_2013_id[i]}, продал {res_2013_cnt_day[i]}; {take_table_shops[take_table_shops['shop_id'] == res_2013_id[i]]['shop_name'].values[0]}")

print("----------------------------------")


res_2014 = top_5_by_month[top_5_by_month['date'].str.contains('.2014', regex=True)]

res_2014_id = res_2014.groupby('shop_id')['item_cnt_day'].sum().nlargest(5).index.to_list()

res_2014_cnt_day = res_2014.groupby('shop_id')['item_cnt_day'].sum().nlargest(5).to_list()




print("Топ-5 магазинов по продажам в январе 2014:")

for i in range(len(res_2014_id)):
    print(f"{i + 1} Магазин {res_2014_id[i]}, продал {res_2014_cnt_day[i]}; {take_table_shops[take_table_shops['shop_id'] == res_2014_id[i]]['shop_name'].values[0]}")

print("----------------------------------")

res_2015 = top_5_by_month[top_5_by_month['date'].str.contains('.2015', regex=True)]

res_2015_id = res_2015.groupby('shop_id')['item_cnt_day'].sum().nlargest(5).index.to_list()

res_2015_cnt_day = res_2015.groupby('shop_id')['item_cnt_day'].sum().nlargest(5).to_list()


print("Топ-5 магазинов по продажам в январе 2015:")

for i in range(len(res_2015_id)):
    print(f"{i + 1} Магазин {res_2015_id[i]}, продал {res_2015_cnt_day[i]}; {take_table_shops[take_table_shops['shop_id'] == res_2015_id[i]]['shop_name'].values[0]}")
    
